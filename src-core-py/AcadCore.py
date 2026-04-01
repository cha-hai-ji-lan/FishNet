import asyncio
import pywintypes
import win32com.client as win32

from typeInfoConfig import (
    config
)
from staticParam import cut_slope, eye_cut_slope, base_param


class ACADBase:
    def __init__(self):
        self.cad = None  # CAD对象
        self.doc = None  # 当前文档
        self.ven = None  # CAD版本
        self.oc = None  # 颜色对象
        self.msp = None  # 模型空间
        self.cfg = None  # 配置对象
        self.slope = cut_slope  # 剪裁斜率
        self.eye_slope = eye_cut_slope  # 宕眼剪裁斜率
        self.param = base_param  # 参数对象
        self.template_path = None  # 模板路径
        self.s_pos = [None] * 12

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出时清理 AutoCAD COM 对象

        :param exc_type: 异常类型
        :param exc_val: 异常值
        :param exc_tb: 异常追踪信息
        :return: None
        """
        try:
            if config["FIN_SAVE_DOC"] and self.doc and self.doc.Saved is False:  # 保存文档
                # 保存并关闭文档（如果需要）
                self.doc.Save()  # 如果需要自动保存，取消注释
            if config["FIN_CLOSE_DOC"] and self.doc:  # 关闭文档
                self.doc.Close(False)  # 不保存关闭
            if config["FIN_QUIT_CAD"] and self.cad:  # 退出关闭 AutoCAD
                # 退出 AutoCAD 应用程序
                self.cad.Quit()
            # 释放 COM 对象引用
            self.doc = None
            self.cad = None
            self.msp = None
            self.oc = None

            print("AutoCAD 连接已断开，资源已释放")

        except Exception as e:
            print(f"清理 AutoCAD 资源时出错：{str(e)}")
            raise

    def _save_document(self, file_path: str) -> bool:
        """
        保存当前文档到指定路径

        :param file_path: 文件保存路径（包含文件名和 .dwg 扩展名）
        :return: 保存是否成功
        """
        try:
            if not file_path.lower().endswith('.dwg'):
                file_path += '.dwg'

            self.doc.SaveAs(file_path)
            print(f"文档已保存到：{file_path}")
            return True
        except pywintypes.com_error as e:
            print(f"保存文档失败：{str(e)}")
            return False
        except Exception as e:
            print(f"保存文档时发生意外错误：{str(e)}")
            return False

    def save_as(self, file_path: str) -> bool:
        """
        另存为文档（save_document 的别名）

        :param file_path: 文件保存路径（包含文件名和 .dwg 扩展名）
        :return: 保存是否成功
        """
        return self._save_document(file_path)

    def load_line_type(self, line_style: str) -> None:
        """
        加载线形
        ACAD_ISO04W100 : 线型
        acadiso.lin : 模板
        :return: None
        """
        try:
            self.doc.Linetypes.Load(line_style, "acadiso.lin")
        except pywintypes.com_error:
            pass

    def _set_text_style(self) -> None:
        """
        配置绘图使用的字体

        :return: None
        """
        try:
            self._active_text_style()
        except pywintypes.com_error:
            try:
                self._active_text_style("汉仪长仿宋体", "长仿宋体")
            except pywintypes.com_error:
                self._active_text_style("仿宋", "仿宋体")

    def _active_text_style(self, font_name="长仿宋体（工程制图用）", style_name="长仿宋体") -> None:
        """
        创建新样式并设置字体
        :param font_name:  设备字体名称
        :param style_name:  活动文档字体显示名称
        :return:
        """
        new_text_style = self.doc.TextStyles.Add(style_name)
        new_text_style.SetFont(font_name, False, True, 1, 0 or 0)  # CharSet=0, PitchAndFamily=1
        # 激活新样式
        self.doc.ActiveTextStyle = self.doc.TextStyles.Item(style_name)
        self.doc.Regen(True)  # 刷新文档显示更改

    def undo(self, steps: int = 1) -> bool:
        """
        撤销指定的操作步骤数
        撤销限制：AutoCAD 的撤销步数受系统变量 UNDOCTL 和 UINDO 限制

        :param steps: 要撤销的步数，默认为 1 步
        :return: 撤销是否成功
        """
        try:
            for _ in range(steps):
                self.doc.Undo()
            print(f"已成功撤销 {steps} 步操作")
            return True
        except pywintypes.com_error as e:
            print(f"撤销操作失败：{str(e)}")
            return False
        except Exception as e:
            print(f"撤销时发生意外错误：{str(e)}")
            return False

    def redo(self, steps: int = 1) -> bool:
        """
        重做指定的操作步骤数

        :param steps: 要重做的步数，默认为 1 步
        :return: 重做是否成功
        """
        try:
            for _ in range(steps):
                self.doc.Redo()
            print(f"已成功重做 {steps} 步操作")
            return True
        except pywintypes.com_error as e:
            print(f"重做操作失败：{str(e)}")
            return False
        except Exception as e:
            print(f"重做时发生意外错误：{str(e)}")
            return False

    def clean_model(self):
        """
        清除模型空间中的所有对象
        :return:
        """
        # 获取模型空间中的所有对象
        try:
            self.doc.SendCommand(f"_.AI_SELALL\n")
            self.doc.SendCommand(f"_.ERASE\n")
        except pywintypes.com_error as _:
            print("-clean-err")


class AcadDxf(ACADBase):
    """
    AutoCAD DXF数据处理
    """

    def get_all_entities(self) -> list:
        """
        获取模型空间中所有绘制的元素（实体对象）

        :return: 包含所有实体对象的列表
        """
        try:
            entities = []
            for entity in self.msp:
                entities.append(entity)
            print(f"共找到 {len(entities)} 个实体对象")
            return entities
        except Exception as e:
            print(f"获取实体对象时出错：{str(e)}")
            return []

    def get_entities_by_type(self, entity_type: str) -> list:
        """
        根据类型获取模型空间中的实体对象

        :param entity_type: 实体类型名称（如 'Line', 'Circle', 'Text' 等）
        :return: 符合条件的实体对象列表
        """
        try:
            entities = []
            for entity in self.msp:
                if entity.ObjectName == entity_type:
                    entities.append(entity)
            print(f"共找到 {len(entities)} 个 '{entity_type}' 类型的对象")
            return entities
        except Exception as e:
            print(f"获取实体对象时出错：{str(e)}")
            return []

    @staticmethod
    def get_entity_info(entity) -> dict:
        """
        获取单个实体的详细信息
        AcDbLine - 直线
        AcDbCircle - 圆
        AcDbArc - 圆弧
        AcDbPolyline - 多段线
        AcDbText - 文字
        AcDbMText - 多行文字
        AcDbBlockReference - 块引用
        AcDbDimension - 标注

        :param entity: 实体对象
        :return: 包含实体信息的字典
        """
        try:
            info = {
                'ObjectName': entity.ObjectName,
                'Handle': entity.Handle,
                'Layer': entity.Layer,
                'Color': entity.Color,
                'Linetype': entity.Linetype,
            }

            # 根据类型添加特定属性
            if entity.ObjectName == 'AcDbLine':
                info['StartPoint'] = entity.StartPoint
                info['EndPoint'] = entity.EndPoint
                info['Length'] = entity.Length
            elif entity.ObjectName == 'AcDbCircle':
                info['Center'] = entity.Center
                info['Radius'] = entity.Radius
                info['Area'] = entity.Area
            elif entity.ObjectName == 'AcDbText':
                info['TextString'] = entity.TextString
                info['Height'] = entity.Height
                info['InsertionPoint'] = entity.InsertionPoint

            return info
        except Exception as e:
            print(f"获取实体信息时出错：{str(e)}")
            return {}

    def count_entities(self) -> dict:
        """
        统计模型空间中各类型实体的数量

        :return: 包含各类型实体数量的字典
        """
        try:
            count_dict = {}
            for entity in self.msp:
                obj_name = entity.ObjectName
                count_dict[obj_name] = count_dict.get(obj_name, 0) + 1

            print(f"实体统计结果：{count_dict}")
            return count_dict
        except Exception as e:
            print(f"统计实体时出错：{str(e)}")
            return {}


# # 创建 CAD 实例
# acad = ACAD()
#
# # 1. 获取所有实体
# all_entities = acad.get_all_entities()
# print(f"总实体数：{len(all_entities)}")
#
# # 2. 按类型获取实体
# lines = acad.get_entities_by_type('AcDbLine')
# circles = acad.get_entities_by_type('AcDbCircle')
# texts = acad.get_entities_by_type('AcDbText')
#
# # 3. 统计各类型实体数量
# counts = acad.count_entities()
# print(counts)
#
# # 4. 获取单个实体的详细信息
# if all_entities:
#     first_entity = all_entities[0]
#     info = acad.get_entity_info(first_entity)
#     print(info)
class ACAD(AcadDxf):
    def __init__(self):
        super().__init__()
        print("-start-cad")
        self.connectCAD()
        print("-finish-start-cad")

    def connectCAD(self) -> None:
        """
        连接到 AutoCAD
        如果失败就创建AutoCAD实例
        :return: None
        """
        try:  # 尝试获得当前活动的CAD实例
            print("-try-connect-cad")
            self.cad = win32.GetActiveObject("AutoCAD.Application")
            print("-fin-connect-cad")

        except pywintypes.com_error:  # 无活动CAD实例则启动启动一个新的
            # 如果没有运行的实例，则创建一个新的实例
            print("-fail-connect-cad")
            print("-try-crate-cad")
            try:
                self.cad = win32.Dispatch("AutoCAD.Application")
                self.cad.Visible = True  # 使 AutoCAD 可见
                print("-fin-crate-cad")  # 成功创建CAD实例
            except pywintypes.com_error:  # 无法创建新的CAD实例应当重启后尝试
                print("-fail-crate-cad")  # 创建CAD实例失败

        # 现在 acad 变量包含对 AutoCAD 应用程序对象的引用
        pref = self.cad.Preferences
        # 获取文件设置
        files = pref.Files
        registry_data = str(files).split(";")
        self.template_path = (registry_data[0]
                              .replace("Roaming", "Local")
                              .replace("support", "Template")
                              + r"\acadiso.dwt")
        try:  # 获取当前文档
            self.doc = self.cad.ActiveDocument
        except pywintypes.com_error:  # 如果没有打开文档 则创建一个
            self.doc = self.cad.Documents.Add(self.template_path)
        self.ven = self.cad.Application.Version[0:2]
        self.oc = self.cad.Application.GetInterfaceObject(F"AutoCAD.AcCmColor.{self.ven}")
        self.msp = self.doc.ModelSpace
        self.doc.Application.Visible = True
        self.load_line_type("ACAD_ISO04W100")  # 加载线型

    def draw_two_piece_body(self, args: list) -> None:
        """
        绘制两片式网身
        :return: None
        """
        pass
