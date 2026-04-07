import asyncio
import json
import re

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
        self.slope = []  # 剪裁斜率
        self.eye_slope = []  # 宕眼剪裁斜率
        self.param = base_param  # 参数对象
        self.template_path = None  # 模板路径
        self.s_pos = [None] * 12  # 存储四点坐标组
        self.i_arg = []  # 用户输入的一组参数

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

class AcadTool(AcadDxf):
    """
    AutoCAD 工具类

    用于控制Acad绘图时特殊封装参数计算
    """

    def __init__(self):
        super().__init__()

    def collate_param(self, arg: str) -> None:
        """
        整理参数,用于把传来的参数规整成可用的参数类型
        :return: None
        """
        result = arg.split(",")
        for single_param in result:
            if single_param in ["", "null", None]:
                single_param = None
            elif single_param in [True, "True", "true"]:
                single_param = True
            elif single_param in [False, "False", "false"]:
                single_param = False
            else:
                try:
                    single_param = float(single_param)
                except ValueError:
                    single_param = re.findall(r'\d+\.\d+|\d+', single_param)
            self.i_arg.append(single_param)
        pass

    def confirm_the_clipping_slope__two(self) -> None:
        """
        通过比率计算拖网剪裁斜率
        :param args: 用户输入参数
        :return:
        """
        tmp_slope1 = self.i_arg[-1][0]
        tmp_slope2 = self.i_arg[-1][-1]
        self.slope = []
        match tmp_slope1:
            case 1:
                self.slope = cut_slope["1-1"]["1"]["NAN"][:]
            case 2:
                if self.i_arg[1] % tmp_slope1 <= 0.5:
                    self.slope = cut_slope["2-1"]["2"]["0.5"][:]
                elif self.i_arg[1] % tmp_slope1 <= 1.5:
                    self.slope = cut_slope["2-1"]["2"]["1.5"][:]
                else:
                    self.slope = ["null"]
            case 3:
                if tmp_slope2 == 1:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["3-1"]["3"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["3-1"]["3"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["3-1"]["3"]["2.5"][:]
                    else:
                        self.slope = ["null"]
                elif tmp_slope2 == 2:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["3-2"]["3"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["3-2"]["3"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["3-2"]["3"]["2.5"][:]
                    else:
                        self.slope = ["null"]
                else:
                    print("暂不支持该剪切斜率")
            case 4:
                if tmp_slope2 == 1:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["4-1"]["4"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["4-1"]["4"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["4-1"]["4"]["2.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 3.5:
                        self.slope = cut_slope["4-1"]["4"]["3.5"][:]
                    else:
                        self.slope = ["null"]

                elif tmp_slope2 == 3:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["4-3"]["4"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["4-3"]["4"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["4-3"]["4"]["2.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 3.5:
                        self.slope = cut_slope["4-3"]["4"]["3.5"][:]
                    else:
                        self.slope = ["null"]
                else:
                    print("暂不支持该剪切斜率")
            case 5:
                if tmp_slope2 == 1:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["5-1"]["5"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["5-1"]["5"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["5-1"]["5"]["2.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 3.5:
                        self.slope = cut_slope["5-1"]["5"]["3.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 4.5:
                        self.slope = cut_slope["5-1"]["5"]["4.5"][:]
                    else:
                        self.slope = ["null"]
                elif tmp_slope2 == 3:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["5-3"]["5"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["5-3"]["5"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["5-3"]["5"]["2.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 3.5:
                        self.slope = cut_slope["5-3"]["5"]["3.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 4.5:
                        self.slope = cut_slope["5-3"]["5"]["4.5"][:]
                    else:
                        self.slope = ["null"]
            case 7:
                if tmp_slope2 == 1:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["7-1"]["7"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["7-1"]["7"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["7-1"]["7"]["2.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 3.5:
                        self.slope = cut_slope["7-1"]["7"]["3.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 4.5:
                        self.slope = cut_slope["7-1"]["7"]["4.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 5.5:
                        self.slope = cut_slope["7-1"]["7"]["5.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 6.5:
                        self.slope = cut_slope["7-1"]["7"]["6.5"][:]
                    else:
                        self.slope = ["null"]

            case 8:
                if tmp_slope2 == 1:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["8-1"]["8"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["8-1"]["8"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["8-1"]["8"]["2.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 3.5:
                        self.slope = cut_slope["8-1"]["8"]["3.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 4.5:
                        self.slope = cut_slope["8-1"]["8"]["4.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 5.5:
                        self.slope = cut_slope["8-1"]["8"]["5.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 6.5:
                        self.slope = cut_slope["8-1"]["8"]["6.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 7.5:
                        self.slope = cut_slope["8-1"]["8"]["7.5"][:]
                    else:
                        self.slope = ["null"]

    def confirm_the_eye_clipping_slope__two(self, args: dict = None) -> None:
        tmp_slope1 = int(args["EyeCuttingSlope"][0])
        tmp_slope2 = int(args["EyeCuttingSlope"][-1])
        match tmp_slope1:
            case 1:
                if tmp_slope2 == 1:
                    self.eye_cutting_slope_data = eye_cut_slope["1-1"]["1"]["NAN"][:]
                elif tmp_slope2 == 2:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.eye_cutting_slope_data = eye_cut_slope["1-2"]["1"]["0.5"][:]
                    else:
                        self.eye_cutting_slope_data = ["null"]
                        print("self.eye_cutting_slope_data = ['null']")
                elif tmp_slope2 == 3:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.eye_cutting_slope_data = eye_cut_slope["1-3"]["1"]["0.5"][:]
                    else:
                        self.eye_cutting_slope_data = ["null"]
                        print("self.eye_cutting_slope_data = ['null']")

            case 2:
                if self.i_arg[1] % tmp_slope1 <= 0.5:
                    self.eye_cutting_slope_data = eye_cut_slope["2-3"]["2"]["0.5"][:]
                elif self.i_arg[1] % tmp_slope1 <= 1.5:
                    self.eye_cutting_slope_data = eye_cut_slope["2-3"]["2"]["1.5"][:]
                else:
                    self.eye_cutting_slope_data = ["null"]
                    print("self.eye_cutting_slope_data = ['null']")

    def calculate_the_ratio(self, args):
        # 计算起剪数据
        if isinstance(self.slope[0], str):
            number_list = re.findall(r'\d+\.\d+|\d+', self.slope[0])
            if "N" in self.slope[0]:
                self.cut_start_to_end_dict["N"] += float(number_list[0])
            if "T" in self.slope[0]:
                self.cut_start_to_end_dict["T"] += float(number_list[0])
            if "B" in self.slope[0]:
                self.cut_start_to_end_dict["B"] += float(number_list[1]) / 2
                self.cut_start_to_end_dict["N"] += float(number_list[1]) / 2
        elif isinstance(self.slope[0], list):
            for cut_slope_obj in self.slope[0]:
                if isinstance(cut_slope_obj, str):
                    number_list = re.findall(r'\d+\.\d+|\d+', cut_slope_obj)
                    if "N" in cut_slope_obj:
                        self.cut_start_to_end_dict["N"] += float(number_list[0])
                    if "T" in cut_slope_obj:
                        self.cut_start_to_end_dict["T"] += float(number_list[0])
                    if "B" in cut_slope_obj:
                        self.cut_start_to_end_dict["B"] += float(number_list[1]) / 2
                        self.cut_start_to_end_dict["N"] += float(number_list[1]) / 2
        # 计算落剪数据
        if isinstance(self.slope[2], str) and len(self.slope[2]) > 2:
            number_list = re.findall(r'\d+\.\d+|\d+', self.slope[2])
            if "N" in self.slope[2]:
                self.cut_start_to_end_dict["N"] += float(number_list[0])
            if "T" in self.slope[2]:
                self.cut_start_to_end_dict["T"] += float(number_list[0])
            if "B" in self.slope[2]:
                self.cut_start_to_end_dict["B"] += float(number_list[1]) / 2
                self.cut_start_to_end_dict["N"] += float(number_list[1]) / 2
        elif isinstance(self.slope[2], str) and len(self.slope[2]) <= 2:
            number_list = re.findall(r'\d+\.\d+|\d+', self.slope[2])
            if "N" in self.slope[2]:
                self.cut_start_to_end_dict["N"] += float(number_list[0])
            if "T" in self.slope[2]:
                self.cut_start_to_end_dict["T"] += float(number_list[0])
            if "B" in self.slope[2]:
                self.cut_start_to_end_dict["B"] += float(number_list[0]) / 2
                self.cut_start_to_end_dict["N"] += float(number_list[0]) / 2
        elif isinstance(self.slope[2], list):
            for cut_slope_obj in self.slope[2]:
                if isinstance(cut_slope_obj, str):
                    number_list = re.findall(r'\d+\.\d+|\d+', cut_slope_obj)
                    if "N" in cut_slope_obj:
                        self.cut_start_to_end_dict["N"] += float(number_list[0])
                    if "T" in cut_slope_obj:
                        self.cut_start_to_end_dict["T"] += float(number_list[0])
                    if "B" in cut_slope_obj:
                        self.cut_start_to_end_dict["B"] += float(number_list[1]) / 2
                        self.cut_start_to_end_dict["N"] += float(number_list[1]) / 2
                    self.cycles += 1
        # 计算续剪数据
        cycles_total_len = (self.i_arg[1]
                            - self.cut_start_to_end_dict["N"])
        if isinstance(self.slope[1], str) and len(self.slope[1]) > 2:
            self.cycles = 0
            temp_one_cycles_len = 0
            number_list = re.findall(r'\d+\.\d+|\d+', self.slope[1])
            while True:
                if "N" in self.slope[1]:
                    self.cut_start_to_end_dict["N"] += float(number_list[0])
                    temp_one_cycles_len += float(number_list[0])
                if "T" in self.slope[1]:
                    self.cut_start_to_end_dict["T"] += float(number_list[0])
                if "B" in self.slope[1]:
                    self.cut_start_to_end_dict["B"] += (float(number_list[1]) / 2)
                    self.cut_start_to_end_dict["N"] += (float(number_list[1]) / 2)
                    temp_one_cycles_len += (float(number_list[1]) / 2)
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break

            self.slope[1] += F"({self.cycles})"
            self.cycles = 0
        elif isinstance(self.slope[1], str) and len(self.slope[1]) <= 2:
            self.cycles = 0
            temp_one_cycles_len = 0
            number_list = re.findall(r'\d+\.\d+|\d+', self.slope[1])
            while True:
                if "N" in self.slope[1]:
                    self.cut_start_to_end_dict["N"] += float(number_list[0])
                    temp_one_cycles_len += float(number_list[0])
                if "T" in self.slope[1]:
                    self.cut_start_to_end_dict["T"] += float(number_list[0])
                if "B" in self.slope[1]:
                    self.cut_start_to_end_dict["B"] += (float(number_list[0]) / 2)
                    self.cut_start_to_end_dict["N"] += (float(number_list[0]) / 2)
                    temp_one_cycles_len += (float(number_list[0]) / 2)
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break
            self.slope[1] += F"({self.cycles})"
            self.cycles = 0
        elif isinstance(self.slope[1], list):
            self.cycles = 0
            temp_one_cycles_len = 0
            while True:
                for cut_slope_obj in self.slope[1]:
                    if isinstance(cut_slope_obj, str):
                        number_list = re.findall(r'\d+\.\d+|\d+', cut_slope_obj)
                        if "N" in cut_slope_obj:
                            self.cut_start_to_end_dict["N"] += float(number_list[0])
                            temp_one_cycles_len += float(number_list[0])
                        if "T" in cut_slope_obj:
                            self.cut_start_to_end_dict["T"] += float(number_list[0])
                        if "B" in cut_slope_obj:
                            self.cut_start_to_end_dict["B"] += float(number_list[1]) / 2
                            self.cut_start_to_end_dict["N"] += float(number_list[1]) / 2
                            temp_one_cycles_len += float(number_list[1]) / 2.
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break
            self.slope[1][-1] += F"({self.cycles})"

    def calculate_the_eye_ratio(self, args):
        if isinstance(self.eye_cutting_slope_data[0], str):
            number_list = re.findall(r'\d+\.\d+|\d+', self.eye_cutting_slope_data[0])
            if "N" in self.eye_cutting_slope_data[0]:
                self.eye_cut_start_to_end_dict["N"] += float(number_list[0])
            if "T" in self.eye_cutting_slope_data[0]:
                self.eye_cut_start_to_end_dict["T"] += float(number_list[0])
            if "B" in self.eye_cutting_slope_data[0]:
                self.eye_cut_start_to_end_dict["B"] += float(number_list[1]) / 2
                self.eye_cut_start_to_end_dict["N"] += float(number_list[1]) / 2
        else:
            print("宕眼剪裁斜率参数错误1")
        if isinstance(self.eye_cutting_slope_data[2], str) and len(self.eye_cutting_slope_data[2]) > 2:
            number_list = re.findall(r'\d+\.\d+|\d+', self.eye_cutting_slope_data[2])
            if "N" in self.eye_cutting_slope_data[2]:
                self.eye_cut_start_to_end_dict["N"] += float(number_list[0])
            if "T" in self.eye_cutting_slope_data[2]:
                self.eye_cut_start_to_end_dict["T"] += float(number_list[0])
            if "B" in self.eye_cutting_slope_data[2]:
                self.eye_cut_start_to_end_dict["B"] += float(number_list[1]) / 2
                self.eye_cut_start_to_end_dict["N"] += float(number_list[1]) / 2
        elif isinstance(self.eye_cutting_slope_data[2], str) and len(self.eye_cutting_slope_data[2]) <= 2:
            number_list = re.findall(r'\d+\.\d+|\d+', self.eye_cutting_slope_data[2])
            if "N" in self.eye_cutting_slope_data[2]:
                self.eye_cut_start_to_end_dict["N"] += float(number_list[0])
            if "T" in self.eye_cutting_slope_data[2]:
                self.eye_cut_start_to_end_dict["T"] += float(number_list[0])
            if "B" in self.eye_cutting_slope_data[2]:
                self.eye_cut_start_to_end_dict["B"] += float(number_list[0]) / 2
                self.eye_cut_start_to_end_dict["N"] += float(number_list[0]) / 2
        else:
            print("宕眼剪裁斜率参数错误2")
        cycles_total_len = (self.i_arg[1]
                            - self.eye_cut_start_to_end_dict["N"])
        if isinstance(self.eye_cutting_slope_data[1], str) and len(self.eye_cutting_slope_data[1]) > 2:
            self.cycles = 0
            temp_one_cycles_len = 0
            number_list = re.findall(r'\d+\.\d+|\d+', self.eye_cutting_slope_data[1])
            while True:
                if "N" in self.eye_cutting_slope_data[1]:
                    self.eye_cut_start_to_end_dict["N"] += float(number_list[0])
                    temp_one_cycles_len += float(number_list[0])
                if "T" in self.eye_cutting_slope_data[1]:
                    self.eye_cut_start_to_end_dict["T"] += float(number_list[0])
                if "B" in self.eye_cutting_slope_data[1]:
                    self.eye_cut_start_to_end_dict["B"] += (float(number_list[1]) / 2)
                    self.eye_cut_start_to_end_dict["N"] += (float(number_list[1]) / 2)
                    temp_one_cycles_len += (float(number_list[1]) / 2)
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break
            if self.eye_cutting_slope_data[1] == self.eye_cutting_slope_data[-1]:
                self.cycles += 1
                del self.eye_cutting_slope_data[-1]
            self.eye_cutting_slope_data[1] += F"({self.cycles})"
            self.cycles = 0
        elif isinstance(self.eye_cutting_slope_data[1], str) and len(self.eye_cutting_slope_data[1]) <= 2:
            self.cycles = 0
            temp_one_cycles_len = 0
            number_list = re.findall(r'\d+\.\d+|\d+', self.eye_cutting_slope_data[1])
            while True:
                if "N" in self.eye_cutting_slope_data[1]:
                    self.eye_cut_start_to_end_dict["N"] += float(number_list[0])
                    temp_one_cycles_len += float(number_list[0])
                if "T" in self.eye_cutting_slope_data[1]:
                    self.eye_cut_start_to_end_dict["T"] += float(number_list[0])
                if "B" in self.eye_cutting_slope_data[1]:
                    self.eye_cut_start_to_end_dict["B"] += (float(number_list[0]) / 2)
                    self.eye_cut_start_to_end_dict["N"] += (float(number_list[0]) / 2)
                    temp_one_cycles_len += (float(number_list[0]) / 2)
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break
            if self.eye_cutting_slope_data[1] == self.eye_cutting_slope_data[-1]:
                self.cycles += 1
                del self.eye_cutting_slope_data[-1]
            self.eye_cutting_slope_data[1] += F"({self.cycles})"
            self.cycles = 0
        else:
            print("宕眼剪裁斜率参数错误3")


class ACAD(AcadTool):
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

    def draw_two_piece_body(self, arg, *args, **kwargs) -> None:
        """
        绘制两片式网身
        :return: None
        """
        self.collate_param(arg)
        self.confirm_the_clipping_slope__two(arg)
        pass
