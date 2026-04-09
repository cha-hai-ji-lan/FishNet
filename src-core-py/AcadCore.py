import math
import re
import win32com.client as win32

from typeInfoConfig import (
    config,
    listTOFloatVT as l2F,
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
        self.cycles = 0  # 续剪 循环次数
        self.shears: dict = {"N": 0, "T": 0, "B": 0}  # 边旁 起剪 续剪 落剪参数
        self.eye_shears: dict = {"N": 0, "T": 0, "B": 0}  # 宕眼 起剪 续剪 落剪参数
        self.param = base_param  # 参数对象
        self.template_path = None  # 模板路径
        self.part_obj = None  # 部件对象
        self.s_pos = []  # 存储坐标组
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

            print("--break-lnk-AutoCAD-free-resource")

        except Exception as e:
            print(f"--free-resource-err--{str(e)}")
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
            print(f"--file-save-in--{file_path}")
            return True
        except Exception as e:
            print(f"--file-save-err--{str(e)}")
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
        except Exception as e:
            print(f"--load-line-type-err--{str(e)}")

    def _set_text_style(self) -> None:
        """
        配置绘图使用的字体

        :return: None
        """
        try:
            self._active_text_style()
        except Exception as e:
            print(f"--set-text-style-warn1--{str(e)}")
            try:
                self._active_text_style("汉仪长仿宋体", "长仿宋体")
            except Exception as e:
                print(f"--set-text-style-warn2--{str(e)}")
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
            print(f"--has-undo--{steps}--step-opr")
            return True
        except Exception as e:
            print(f"--undo-err--{str(e)}")
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
            print(f"--has-redo-{steps}--step-opr")
            return True
        except Exception as e:
            print(f"--redo-err--{str(e)}")
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
        except Exception as e:
            print(f"-clean-err--{str(e)}")


class AcadDxf(ACADBase):
    """
    AutoCAD DXF数据处理
    """

    def __init__(self):
        super().__init__()
        self.cache = {}  # 坐标缓存记录
        self.has_draw_first_segment = False  # 是否绘制了网身第一段

    def get_all_entities(self) -> list:
        """
        获取模型空间中所有绘制的元素（实体对象）

        :return: 包含所有实体对象的列表
        """
        try:
            entities = []
            for entity in self.msp:
                entities.append(entity)
            print(f"--find--{len(entities)}--entities")
            return entities
        except Exception as e:
            print(f"--get-entities-err--{str(e)}")
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
            print(f"--find--{len(entities)}--{entity_type}")
            return entities
        except Exception as e:
            print(f"--get-entities-err--{str(e)}")
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
            print(f"--get-entity-info-err--{str(e)}")
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

            print(f"--count--{count_dict}")
            return count_dict
        except Exception as e:
            print(f"--count-entities-err--{str(e)}")
            return {}

    @staticmethod
    def mid_val(pos_val1: float, pos_val2: float) -> float:
        """
        坐标两单值 ,之间的中点值
        :param pos_val1: 坐标单值1
        :param pos_val2: 坐标单值2
        :return: float: mid_val
        """
        return (pos_val1 + pos_val2) / 2

    def mid_pos(self, pos_list1: list, pos_list2: list) -> list:
        """
        坐标两列表之间的中点值
        :param pos_list1:  坐标列表1
        :param pos_list2:  坐标列表2
        :return:
        """
        temp: list = []
        for i in range(len(pos_list1)):
            temp.append(self.mid_val(pos_list1[i], pos_list2[i]))
        return temp

    def pos_write_to_adoc(self, pos_list: list, close_flag: bool = True):
        """
        AutoCAD上绘制多段线
        绘制结束后可选
        1.聚焦绘图
        2.闭合回路
        :param pos_list:
        :param close_flag:
        :return:
        """
        rectangle = self.msp.AddLightWeightPolyline(l2F(pos_list))
        if self.cfg["backUpMode"] == "single-step":
            self.doc.SendCommand("_.UNDO\n_MARK\n")  # 撤销标记
        if self.cfg["focusDraw"]:
            self.focus_interface()  # 聚焦
        if close_flag:
            rectangle.Closed = True
        print(self.msp.Count)

    def mk_txt(self, content: str, position: list, word_height: float = 0,
               insert_mode: int = 0, label_offset: list | None = None, rotary: tuple = (0, []),
               mirror=(0, [])):
        """
        进行文本标注
        :param content: 标注内容
        :param position: 标注位置
        :param word_height: 标注字高
        :param insert_mode: 标注模式
         0：左下对齐\n   1：中下对齐\n
         2：右下对齐\n   3：正中对齐\n
         4：中心对齐\n   5：顶部居中对齐\n
         6：左上对齐\n   7：中上对齐\n
         8：右上对齐\n   9：左中对齐\n
         10：中心对齐\n  11：右中对齐\n
         12：左下对齐\n
        :param label_offset: 标注偏移量 -- 默认不偏移
        [
        arg 1 : 偏移的距离 mm
        rag 2 ： 偏移的方向 1：上偏  2：下偏  3：左偏  4：右偏
        ]
        :param rotary: 是否旋转文字
        0：不旋转
        1：按剪裁斜率缺角度旋转  --常用
        2：按剪裁斜率 补角 度旋转  --不常用
        []: 包含模块 高度 和 右侧两点距离用于计算 tan值
        :param mirror: 是否将标注镜像 传入 带有 模式 与一个坐标向量的元组例如 (1,[10, 10])
        0：不镜像
        1：镜像但不删除原文字对象
        2：镜像并且删除原文字对象
        :return:
        """
        if len(position) == 2:
            position.append(0)
        if word_height == 0:  # 如果字高为0，则使用默认表格字高
            word_height = self.cfg["sheetTextHeight"]
        if label_offset is not None:
            if label_offset[1] == 1:
                position[1] += label_offset[0]
            elif label_offset[1] == 2:
                position[1] -= label_offset[0]
            elif label_offset[1] == 3:
                position[0] -= label_offset[0]
            elif label_offset[1] == 4:
                position[0] += label_offset[0]
        # 设置文本插入点
        insert_pos = l2F(position)
        text_obj = self.msp.AddText(content, insert_pos, word_height)
        text_obj.Height = word_height
        text_obj.Alignment = insert_mode
        text_obj.TextAlignmentPoint = insert_pos
        match rotary[0]:
            case 1:  # 按剪裁斜率缺角度旋转
                radians = 0
                if isinstance(rotary[1], list):
                    radians = math.atan(rotary[1][0] / rotary[1][1])
                elif isinstance(rotary[1], float):
                    radians = rotary[1]
                rotation_angle = math.radians(90 - radians)
                text_obj.Rotate(insert_pos, rotation_angle)
            case 2:  # 按剪裁斜率补 角度旋转
                radians = 0
                if isinstance(rotary[1], list):
                    radians = math.atan(rotary[1][0] / rotary[1][1])
                elif isinstance(rotary[1], float):
                    radians = rotary[1]
                rotation_angle = math.radians(90 + radians)
                text_obj.Rotate(insert_pos, rotation_angle)
            case 3:  # 按剪裁斜率补 角度 翻转旋转
                radians = 0
                if isinstance(rotary[1], list):
                    radians = math.atan(rotary[1][0] / rotary[1][1])
                elif isinstance(rotary[1], float):
                    radians = rotary[1]
                rotation_angle = math.radians(90 + radians + 180)
                text_obj.Rotate(insert_pos, rotation_angle)
            case _:
                pass

        match mirror[0]:  # Copy的时候，要注意不要出现浅拷贝问题。
            case 1:  # 镜像文字对象但不删除原文字对象
                if len(mirror[1]) == 2:
                    mirror[1].append(0)
                mid_temp: list = mirror[1][:]
                mid_temp[1] += 10
                text_obj.Mirror(l2F(mirror[1]), l2F(mid_temp))
            case 2:  # 镜像文字对象后删除原文字对象
                if len(mirror[1]) == 2:
                    mirror[1].append(0)
                mid_temp: list = mirror[1][:]
                mid_temp[1] += 10
                text_obj.Mirror(l2F(mirror[1]), l2F(mid_temp))
                text_obj.Delete()
            case _:
                pass

    def mmk_txt(self, content: str | list, position: list, word_height: float = 0,
                insert_mode: int = 0, label_offset: list | None = None, rotary: tuple = (0, []),
                mirror=(0, [])):
        if type(content) is str:
            self.mk_txt(content, position, word_height, insert_mode, label_offset, rotary, mirror)
        elif type(content) is list:
            temp_x_pos = 0
            loop = -1
            for i in content:
                if loop == -1:
                    loop += 1
                    if isinstance(i, str):
                        self.mk_txt(i, position, word_height, insert_mode, label_offset, rotary, mirror)
                        temp_x_pos = position[0]
                        position[1] -= word_height
                    elif isinstance(i, list):
                        line_loop = -1
                        for one_piece in i:
                            if line_loop == -1:

                                self.mk_txt(one_piece, position, word_height, insert_mode, label_offset, rotary,
                                            mirror)
                                line_loop = len(one_piece)
                                temp_x_pos = position[0]
                            else:
                                self.mk_txt(one_piece, position, word_height, insert_mode,
                                            [line_loop * 2, label_offset[1]], rotary,
                                            mirror)
                                line_loop = len(one_piece)
                        position[1] -= word_height
                else:
                    if isinstance(i, str):
                        position[0] = temp_x_pos
                        self.mk_txt(i, position, word_height, insert_mode, None, rotary, mirror)
                        position[1] -= word_height
                    elif isinstance(i, list):
                        line_loop = -1
                        for one_piece in i:
                            if line_loop == -1:
                                position[0] = temp_x_pos
                                self.mk_txt(one_piece, position, word_height, insert_mode,
                                            None, rotary,
                                            mirror)
                                line_loop = len(one_piece)
                            else:
                                self.mk_txt(one_piece, position, word_height, insert_mode,
                                            [line_loop * 2, label_offset[1]], rotary, mirror)
                                line_loop = len(one_piece)
                        position[1] -= word_height

    def me_mk_txt(self, content: str | list, position: list, word_height: float = None,
                  insert_mode: int = 0, label_offset: list | None = None, rotary: tuple = (0, []),
                  mirror=(0, [])):
        if type(content) is str:
            self.mk_txt(content, position, word_height, insert_mode, label_offset, rotary, mirror)
        elif type(content) is list:
            temp_x_pos = 0
            loop = -1
            for i in content:
                if loop == -1:
                    loop += 1
                    if isinstance(i, str):
                        self.mk_txt(i, position, word_height, insert_mode, label_offset, rotary, mirror)
                        temp_x_pos = position[0]
                        position[1] -= word_height + self.cfg["annotationOffset"]
                    elif isinstance(i, list):
                        line_loop = -1
                        for one_piece in i:
                            if line_loop == -1:

                                self.mk_txt(one_piece, position, word_height, insert_mode, label_offset, rotary,
                                            mirror)
                                line_loop = len(one_piece)
                                temp_x_pos = position[0]
                            else:
                                self.mk_txt(one_piece, position, word_height, insert_mode,
                                            [line_loop * 2, label_offset[1]], rotary,
                                            mirror)
                                line_loop = len(one_piece)
                        position[1] -= word_height + self.cfg["annotationOffset"]
                else:
                    if isinstance(i, str):
                        position[0] = temp_x_pos
                        self.mk_txt(i, position, word_height, insert_mode, None, rotary, mirror)
                        position[1] -= word_height + self.cfg["annotationOffset"]
                    elif isinstance(i, list):
                        line_loop = -1
                        for one_piece in i:
                            if line_loop == -1:
                                position[0] = temp_x_pos
                                self.mk_txt(one_piece, position, word_height, insert_mode,
                                            None, rotary,
                                            mirror)
                                line_loop = len(one_piece)
                            else:
                                self.mk_txt(one_piece, position, word_height, insert_mode,
                                            [line_loop * 2, label_offset[1]], rotary, mirror)
                                line_loop = len(one_piece)
                        position[1] -= word_height + self.cfg["annotationOffset"]
            self.cache["eyeSlopePosMark"][0] = position
            self.cache["eyeSlopePosMark"][1] -= 2 * self.cfg["sheetTextHeight"]

    def refresh_pos(self) -> None:
        """
        刷新坐标,用于缓存上一段坐标数据,并且清空上一段坐标组数据
        :return: None
        """
        self.cache["eyeSlopePosMark"] = []
        self.cache["preSegment"] = self.s_pos
        self.s_pos = []  # 清空s_pos

    def focus_interface(self) -> None:
        """
        聚焦界面绘图元素
        :return:
        """
        self.doc.SendCommand("_.REGEN\n")  # 下划线确保命令识别，\n表示回车执行 刷新界面
        self.doc.SendCommand("_.ZOOM E\n")  # 下划线确保命令识别，\n表示回车执行 刷新界面


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
        # 封装核心参数
        self.ORI = None  # 原点坐标
        self.ZX = None  # 经过全局缩放后并横向缩放标尺值
        self.ZY = None  # 经过全局缩放后并纵向缩放标尺值

    def collate_param(self, arg) -> None:
        """
        整理参数,用于把传来的参数规整成可用的参数类型
        :return: None
        """
        print(f"-arg-org-st--{arg}--{type(arg)}")
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
                    single_param = [float(x) for x in re.findall(r'\d+\.\d+|\d+', single_param)]
            self.i_arg.append(single_param)
        print(self.i_arg)

    def confirm_the_clipping_slope__two(self) -> None:
        """
        通过比率计算拖网剪裁斜率
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
                    print("-null-slope")
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
                        print("-null-slope")
                elif tmp_slope2 == 2:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.slope = cut_slope["3-2"]["3"]["0.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 1.5:
                        self.slope = cut_slope["3-2"]["3"]["1.5"][:]
                    elif self.i_arg[1] % tmp_slope1 <= 2.5:
                        self.slope = cut_slope["3-2"]["3"]["2.5"][:]
                    else:
                        self.slope = ["null"]
                        print("-null-slope")
                else:
                    print("-shear-slope-support-err")
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
                        print("-null-slope")

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
                        print("-null-slope")
                else:
                    print("-shear-slope-support-err")
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
                        print("-null-slope")
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
                        print("-null-slope")
                else:
                    print("-shear-slope-support-err")
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
                        print("-null-slope")
                else:
                    print("-shear-slope-support-err")

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
                        print("-null-slope")
                else:
                    print("-shear-slope-support-err")

    def confirm_the_eye_clipping_slope__two(self) -> None:
        tmp_slope1 = self.i_arg[-2][0]
        tmp_slope2 = self.i_arg[-2][-1]
        match tmp_slope1:
            case 1:
                if tmp_slope2 == 1:
                    self.eye_slope = eye_cut_slope["1-1"]["1"]["NAN"][:]
                elif tmp_slope2 == 2:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.eye_slope = eye_cut_slope["1-2"]["1"]["0.5"][:]
                    else:
                        self.eye_slope = ["null"]
                        print("-null-eye-slope")
                elif tmp_slope2 == 3:
                    if self.i_arg[1] % tmp_slope1 <= 0.5:
                        self.eye_slope = eye_cut_slope["1-3"]["1"]["0.5"][:]
                    else:
                        self.eye_slope = ["null"]
                        print("-null-eye-slope")
                else:
                    print("-shear-slope-support-err")

            case 2:
                if self.i_arg[1] % tmp_slope1 <= 0.5:
                    self.eye_slope = eye_cut_slope["2-3"]["2"]["0.5"][:]
                elif self.i_arg[1] % tmp_slope1 <= 1.5:
                    self.eye_slope = eye_cut_slope["2-3"]["2"]["1.5"][:]
                else:
                    self.eye_slope = ["null"]
                    print("-null-eye-slope")

    def calculate_the_ratio(self):
        # 计算起剪数据
        print(self.slope)
        if isinstance(self.slope[0], str):
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.slope[0])]
            if "N" in self.slope[0]:
                self.shears["N"] += number_list[0]
            if "T" in self.slope[0]:
                self.shears["T"] += number_list[0]
            if "B" in self.slope[0]:
                self.shears["B"] += number_list[1] / 2
                self.shears["N"] += number_list[1] / 2
        elif isinstance(self.slope[0], list):
            for cut_slope_obj in self.slope[0]:
                if isinstance(cut_slope_obj, str):
                    number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', cut_slope_obj)]
                    if "N" in cut_slope_obj:
                        self.shears["N"] += number_list[0]
                    if "T" in cut_slope_obj:
                        self.shears["T"] += number_list[0]
                    if "B" in cut_slope_obj:
                        self.shears["B"] += number_list[1] / 2
                        self.shears["N"] += number_list[1] / 2
        # 计算落剪数据
        if isinstance(self.slope[2], str) and len(self.slope[2]) > 2:
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.slope[2])]
            if "N" in self.slope[2]:
                self.shears["N"] += number_list[0]
            if "T" in self.slope[2]:
                self.shears["T"] += number_list[0]
            if "B" in self.slope[2]:
                self.shears["B"] += number_list[1] / 2
                self.shears["N"] += number_list[1] / 2
        elif isinstance(self.slope[2], str) and len(self.slope[2]) <= 2:
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.slope[2])]
            if "N" in self.slope[2]:
                self.shears["N"] += number_list[0]
            if "T" in self.slope[2]:
                self.shears["T"] += number_list[0]
            if "B" in self.slope[2]:
                self.shears["B"] += number_list[0] / 2
                self.shears["N"] += number_list[0] / 2
        elif isinstance(self.slope[2], list):
            for cut_slope_obj in self.slope[2]:
                if isinstance(cut_slope_obj, str):
                    number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', cut_slope_obj)]
                    if "N" in cut_slope_obj:
                        self.shears["N"] += number_list[0]
                    if "T" in cut_slope_obj:
                        self.shears["T"] += number_list[0]
                    if "B" in cut_slope_obj:
                        self.shears["B"] += number_list[1] / 2
                        self.shears["N"] += number_list[1] / 2
                    self.cycles += 1
        # 计算续剪数据
        cycles_total_len = self.i_arg[1] - self.shears["N"]  # 续剪数据总长度
        # 如果剪数据为字符串，并且续剪标志字符长度大于2 (例如 1N2B)，则计算续剪数据
        if isinstance(self.slope[1], str) and len(self.slope[1]) > 2:

            self.cycles = 0
            temp_one_cycles_len = 0
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.slope[1])]
            while True:
                if "N" in self.slope[1]:
                    self.shears["N"] += number_list[0]
                    temp_one_cycles_len += number_list[0]
                if "T" in self.slope[1]:
                    self.shears["T"] += number_list[0]
                if "B" in self.slope[1]:
                    self.shears["B"] += number_list[1] / 2
                    self.shears["N"] += number_list[1] / 2
                    temp_one_cycles_len += number_list[1] / 2
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break

            self.slope[1] += F"({self.cycles})"
            self.cycles = 0
        # 如果剪数据为字符串，并且续剪标志字符长度小于2 (例如 1N)，则计算续剪数据
        elif isinstance(self.slope[1], str) and len(self.slope[1]) <= 2:
            self.cycles = 0
            temp_one_cycles_len = 0
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.slope[1])]
            while True:
                if "N" in self.slope[1]:
                    self.shears["N"] += number_list[0]
                    temp_one_cycles_len += number_list[0]
                if "T" in self.slope[1]:
                    self.shears["T"] += number_list[0]
                if "B" in self.slope[1]:
                    self.shears["B"] += number_list[0] / 2
                    self.shears["N"] += number_list[0] / 2
                    temp_one_cycles_len += number_list[0] / 2
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
                        number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', cut_slope_obj)]
                        if "N" in cut_slope_obj:
                            self.shears["N"] += number_list[0]
                            temp_one_cycles_len += number_list[0]
                        if "T" in cut_slope_obj:
                            self.shears["T"] += number_list[0]
                        if "B" in cut_slope_obj:
                            self.shears["B"] += number_list[1] / 2
                            self.shears["N"] += number_list[1] / 2
                            temp_one_cycles_len += number_list[1] / 2.
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break
            self.slope[1][-1] += F"({self.cycles})"

    def calculate_the_eye_ratio(self):
        if isinstance(self.eye_slope[0], str):
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.eye_slope[0])]
            if "N" in self.eye_slope[0]:
                self.eye_shears["N"] += number_list[0]
            if "T" in self.eye_slope[0]:
                self.eye_shears["T"] += number_list[0]
            if "B" in self.eye_slope[0]:
                self.eye_shears["B"] += number_list[1] / 2
                self.eye_shears["N"] += number_list[1] / 2
        else:
            print("-eye-shears-err")
        if isinstance(self.eye_slope[2], str) and len(self.eye_slope[2]) > 2:
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.eye_slope[2])]
            if "N" in self.eye_slope[2]:
                self.eye_shears["N"] += number_list[0]
            if "T" in self.eye_slope[2]:
                self.eye_shears["T"] += number_list[0]
            if "B" in self.eye_slope[2]:
                self.eye_shears["B"] += number_list[1] / 2
                self.eye_shears["N"] += number_list[1] / 2
        elif isinstance(self.eye_slope[2], str) and len(self.eye_slope[2]) <= 2:
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.eye_slope[2])]
            if "N" in self.eye_slope[2]:
                self.eye_shears["N"] += number_list[0]
            if "T" in self.eye_slope[2]:
                self.eye_shears["T"] += number_list[0]
            if "B" in self.eye_slope[2]:
                self.eye_shears["B"] += number_list[0] / 2
                self.eye_shears["N"] += number_list[0] / 2
        else:
            print("-eye-shears-err")
        cycles_total_len = (self.i_arg[1]
                            - self.eye_shears["N"])
        if isinstance(self.eye_slope[1], str) and len(self.eye_slope[1]) > 2:
            self.cycles = 0
            temp_one_cycles_len = 0
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.eye_slope[1])]
            while True:
                if "N" in self.eye_slope[1]:
                    self.eye_shears["N"] += number_list[0]
                    temp_one_cycles_len += number_list[0]
                if "T" in self.eye_slope[1]:
                    self.eye_shears["T"] += number_list[0]
                if "B" in self.eye_slope[1]:
                    self.eye_shears["B"] += (number_list[1] / 2)
                    self.eye_shears["N"] += (number_list[1] / 2)
                    temp_one_cycles_len += (number_list[1] / 2)
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break
            if self.eye_slope[1] == self.eye_slope[-1]:
                self.cycles += 1
                del self.eye_slope[-1]
            self.eye_slope[1] += F"({self.cycles})"
            self.cycles = 0
        elif isinstance(self.eye_slope[1], str) and len(self.eye_slope[1]) <= 2:
            self.cycles = 0
            temp_one_cycles_len = 0
            number_list = [float(x) for x in re.findall(r'\d+\.\d+|\d+', self.eye_slope[1])]
            while True:
                if "N" in self.eye_slope[1]:
                    self.eye_shears["N"] += number_list[0]
                    temp_one_cycles_len += number_list[0]
                if "T" in self.eye_slope[1]:
                    self.eye_shears["T"] += number_list[0]
                if "B" in self.eye_slope[1]:
                    self.eye_shears["B"] += (number_list[0] / 2)
                    self.eye_shears["N"] += (number_list[0] / 2)
                    temp_one_cycles_len += (number_list[0] / 2)
                self.cycles += 1
                if temp_one_cycles_len >= cycles_total_len:
                    break
            if self.eye_slope[1] == self.eye_slope[-1]:
                self.cycles += 1
                del self.eye_slope[-1]
            self.eye_slope[1] += F"({self.cycles})"
            self.cycles = 0
        else:
            print("-eye-shears-err")

    def ori_mir(self, pos_val, mirror_type="x"):
        """
        坐标单值 关于原点的镜像
        :param pos_val: 坐标单值
        :param mirror_type: 镜像类型 x/y
        :return:
        """
        if mirror_type == "x":
            return self.ORI[0] * 2 - pos_val
        else:
            return self.ORI[1] * 2 - pos_val

    def ori_p_mir(self, pos):
        return [self.ori_mir(pos[0]), self.ori_mir(pos[1], "y")]

    @staticmethod
    def s(val1, val2):
        """
        获取间隔值即两值的距离
        :param val1: 值1
        :param val2: 值2
        :return: 两值的距离
        """
        return abs(val1 - val2)

    def draw_sheet_two(self, left_sheet=True):
        """
        绘制两片式拖网左侧表格
        :param left_sheet:
        :return:
        """
        pr = self.cache["preSegment"]  # pr: pos_record的前一段线段坐标点集
        # self.doc.ActiveLayer.Linetype = "ByLayer"
        if left_sheet:
            # 表格注释起始点
            mark_start_pos = [
                self.ORI[0] - (1.5 * self.cfg["tableOffset"]),
                self.mid_val(pr[1], pr[7])
            ]
            self.mk_txt(
                self.i_arg[0],
                mark_start_pos[:],
                0, 1,
                [self.cfg["sheetTextHeight"] / 2, 2]
            )
            if self.part_obj == "tl" and self.i_arg[-1][0] == self.i_arg[-1][1]:
                self.mk_txt(
                    "2a",
                    [mark_start_pos[0], pr[3]],
                    0, 1,
                    [self.cfg["textHeight"], 1]

                )
                line1 = self.msp.AddLightWeightPolyline(l2F([
                    pr[4] + (0.5 * self.cfg["tableOffset"]),
                    pr[5],  # 0
                    pr[4] + (0.5 * self.cfg["tableOffset"]),
                    pr[5] + abs(pr[1] - pr[3]) / 3 * 2,  # 1
                    pr[4] + (0.5 * self.cfg["tableOffset"]),
                    pr[5] + abs(pr[1] - pr[3]),  # 2
                    pr[4] + (0.4 * self.cfg["tableOffset"]),
                    pr[5] + abs(pr[1] - pr[3]),  # 3
                    pr[4] + (0.6 * self.cfg["tableOffset"]),
                    pr[5] + abs(pr[1] - pr[3]),  # 4
                ]))
                line1.SetWidth(1, 2.0, 0.1)
                self.mk_txt("长度1",
                            [
                                pr[4] + (0.5 * self.cfg["tableOffset"]),
                                pr[5] + abs(pr[1] - pr[3])
                            ],
                            self.cfg["sheetTextHeight"],
                            1)
            mark_start_pos[0] -= 0.25 * self.cfg["tableOffset"]
            self.mk_txt(
                self.cfg["material"],
                mark_start_pos[:],
                self.cfg["sheetTextHeight"],
                1,
                [self.cfg["sheetTextHeight"] / 2, 2]
            )
            if self.part_obj == "tl" and self.i_arg[-1][0] != self.i_arg[-1][1]:
                self.mk_txt(
                    "MAT",
                    [mark_start_pos[0], pr[1]],
                    self.cfg["sheetTextHeight"],
                    1,
                    [self.cfg["textHeight"], 1]

                )
            mark_start_pos[0] -= 0.25 * self.cfg["tableOffset"]
            self.mk_txt(
                f"{abs(pr[1] - pr[3]) / 10:.3f}",
                mark_start_pos[:],
                self.cfg["sheetTextHeight"],
                1,
                [self.cfg["sheetTextHeight"] / 2, 2]
            )
            if self.part_obj == "tl" and self.i_arg[-1][0] == self.i_arg[-1][1]:
                self.mk_txt(
                    "NL",
                    [mark_start_pos[0], pr[1]],
                    self.cfg["sheetTextHeight"],
                    1,
                    [self.cfg["textHeight"], 1]
                )
            mark_start_pos[0] -= 0.25 * self.cfg["tableOffset"]
            self.mk_txt(
                self.i_arg[1],
                mark_start_pos[:],
                self.cfg["sheetTextHeight"],
                1,
                [self.cfg["sheetTextHeight"] / 2, 2]
            )
            if self.part_obj == "tl" and self.i_arg[-1][0] == self.i_arg[-1][1]:
                point = self.msp.AddPoint(l2F(
                    [mark_start_pos[0], pr[1] + self.cfg["textHeight"], 0]))
                point.Rotate(l2F(
                    [mark_start_pos[0], pr[1] + self.cfg["textHeight"], 0]),
                    35)
                self.doc.SetVariable("PDMODE", 65)
                self.doc.SetVariable("PDSIZE", self.cfg["textHeight"])

            self.doc.ActiveLayer.Linetype = "Continuous"
            ori_layer = self.doc.ActiveLayer
            dot_layer = self.doc.Layers.Add("DottedLineLayer")
            self.doc.ActiveLayer = dot_layer
            self.doc.ActiveLayer.Linetype = "ACAD_ISO04W100"
            self.msp.AddLightWeightPolyline(l2F([
                pr[0] - (0.5 * self.cfg["tableOffset"]),
                pr[1],
                self.ORI[0] - (2.25 * self.cfg["tableOffset"]),
                pr[1]
            ]))
            if self.i_arg[-1][0] == self.i_arg[-1][1]:
                self.msp.AddLightWeightPolyline(l2F([
                    pr[6] - (0.5 * self.cfg["tableOffset"]),
                    pr[7],
                    self.ORI[0] - (2.25 * self.cfg["tableOffset"]),
                    pr[7]
                ]))
            self.doc.ActiveLayer = ori_layer
            self.msp.AddLightWeightPolyline(l2F([
                self.ORI[0] - (2.125 * self.cfg["tableOffset"]),
                pr[1],
                self.ORI[0] - (2.125 * self.cfg["tableOffset"]),
                pr[7],
            ]))
            if self.part_obj == "tl" and self.i_arg[-2][0] != self.i_arg[-2][-1]:
                if not self.cache["eyeSlopePosMark"]:
                    self.cache["eyeSlopePosMark"] = [
                        self.ORI[0] + (1.75 * self.cfg["tableOffset"]),
                        self.ORI[1] - self.cfg["sheetTextHeight"]
                    ]
                self.eye_slope.insert(0, self.i_arg[-2])
                self.eye_slope.insert(0, "上袖")
                self.me_mk_txt(
                    self.eye_slope,
                    self.cache["eyeSlopePosMark"],
                    self.cfg["textHeight"],
                    9,
                )
            else:
                mark_start_pos = [
                    self.ORI[0] + (1.5 * self.cfg["tableOffset"]),
                    abs(pr[1] - pr[3])
                ]
            self.mk_txt(
                self.cfg["material"],
                mark_start_pos[:],
                self.cfg["sheetTextHeight"],
                1,
                [self.cfg["sheetTextHeight"] / 2, 2]
            )
            if self.part_obj == "tr" and self.i_arg[-1][0] == self.i_arg[-1][1]:
                self.mk_txt(
                    "MAT",
                    [mark_start_pos[0], pr[1]],
                    self.cfg["sheetTextHeight"],
                    1,
                    [self.cfg["textHeight"], 1]

                )
            line1 = self.msp.AddLightWeightPolyline(l2F([
                pr[2] - (0.5 * self.cfg["tableOffset"]),
                pr[3],  # 0
                pr[2] - (0.5 * self.cfg["tableOffset"]),
                pr[3] - ((abs(pr[1] - pr[3]) / 3) * 2),  # 1
                pr[2] - (0.5 * self.cfg["tableOffset"]),
                pr[3] - abs(pr[1] - pr[3]),  # 2
                pr[2] - (0.4 * self.cfg["tableOffset"]),
                pr[3] - abs(pr[1] - pr[3]),  # 3
                pr[2] - (0.6 * self.cfg["tableOffset"]),
                pr[3] - abs(pr[1] - pr[3]),  # 4
            ]))
            line1.SetWidth(1, 2.0, 0.1)
            self.mk_txt("长度2",
                        [
                            pr[2] - (0.5 * self.cfg["tableOffset"]),
                            pr[3] - abs(pr[1] - pr[3])
                        ],
                        self.cfg["sheetTextHeight"],
                        7)
            mark_start_pos[0] += 0.25 * self.cfg["tableOffset"]
            self.mk_txt(
                abs(pr[1] - pr[3]) / 10,
                mark_start_pos[:],
                self.cfg["sheetTextHeight"],
                1,
                [self.cfg["sheetTextHeight"] / 2, 2]
            )
            if self.part_obj == "tr" and self.i_arg[-1][0] == self.i_arg[-1][1]:
                self.mk_txt(
                    "NL",
                    [mark_start_pos[0], pr[1]],
                    self.cfg["sheetTextHeight"],
                    1,
                    [self.cfg["textHeight"], 1]
                )
            mark_start_pos[0] += 0.25 * self.cfg["tableOffset"]
            self.mk_txt(
                self.i_arg[1],
                mark_start_pos[:],
                self.cfg["sheetTextHeight"],
                1,
                [self.cfg["sheetTextHeight"] / 2, 2]
            )
            if self.part_obj == "tr" and self.i_arg[-1][0] == self.i_arg[-1][1]:
                point = self.msp.AddPoint(l2F(
                    [mark_start_pos[0], pr[1] + self.cfg["textHeight"], 0]))
                point.Rotate(l2F(
                    [mark_start_pos[0], pr[1] + self.cfg["textHeight"], 0]),
                    35)
            self.doc.SetVariable("PDMODE", 65)
            self.doc.SetVariable("PDSIZE", self.cfg["textHeight"])

            self.doc.ActiveLayer.Linetype = "Continuous"
            ori_layer = self.doc.ActiveLayer
            dot_layer = self.doc.Layers.Add("DottedLineLayer")
            self.doc.ActiveLayer = dot_layer
            self.doc.ActiveLayer.Linetype = "ACAD_ISO04W100"
            self.msp.AddLightWeightPolyline(l2F([
                pr[2] + (0.5 * self.cfg["tableOffset"]),
                pr[3],
                self.ORI[0] + (2.25 * self.cfg["tableOffset"]),
                pr[3]
            ]))
            if self.has_draw_first_segment:
                self.msp.AddLightWeightPolyline(l2F([
                    pr[4] + (0.5 * self.cfg["tableOffset"]),
                    pr[5],
                    self.ORI[0] + (2.25 * self.cfg["tableOffset"]),
                    pr[5]
                ]))
            self.doc.ActiveLayer = ori_layer
            self.msp.AddLightWeightPolyline(l2F([
                self.ORI[0] + (1.875 * self.cfg["tableOffset"]),
                pr[1],
                self.ORI[0] + (1.875 * self.cfg["tableOffset"]),
                pr[7],
            ]))
            if self.part_obj == "tr" and self.i_arg[-2][0] != self.i_arg[-2][-1]:
                if not self.cache["eyeSlopePosMark"]:
                    self.cache["eyeSlopePosMark"] = [
                        self.ORI[0] + (1.75 * self.cfg["tableOffset"]),
                        self.ORI[1] - self.cfg["sheetTextHeight"]
                    ]
                self.eye_slope.insert(0, self.i_arg[-2])
                self.eye_slope.insert(0, "下袖")
                self.me_mk_txt(
                    self.eye_slope,
                    self.cache["eyeSlopePosMark"],
                    self.cfg["textHeight"],
                    9,
                )

    def set_core_config_encapsulation(self):
        self.ORI = self.cfg["originPosition"]
        self.ZX = self.cfg["zoom"] * self.cfg["scaleX"]  # 经过全局缩放后并横向缩放标尺值
        self.ZY = self.cfg["zoom"] * self.cfg["scaleY"]  # 经过全局缩放后并纵向缩放标尺值


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

        except Exception as e:  # 无活动CAD实例则启动启动一个新的
            print(f"--connect-err-{str(e)}")
            # 如果没有运行的实例，则创建一个新的实例
            print("-fail-connect-cad")
            print("-try-crate-cad")
            try:
                self.cad = win32.Dispatch("AutoCAD.Application")
                self.cad.Visible = True  # 使 AutoCAD 可见
                print("-fin-crate-cad")  # 成功创建CAD实例
            except Exception as e:  # 无法创建新的CAD实例应当重启后尝试
                print(f"--create-cad-err-{str(e)}")  # 创建CAD实例失败
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
        except Exception as e:  # 如果没有打开文档 则创建一个
            print(f"--get-doc-err-{str(e)}")  # 如果没有打开文档 则创建一个
            self.doc = self.cad.Documents.Add(self.template_path)
        self.ven = self.cad.Application.Version[0:2]
        self.oc = self.cad.Application.GetInterfaceObject(F"AutoCAD.AcCmColor.{self.ven}")
        self.msp = self.doc.ModelSpace
        self.doc.Application.Visible = True
        self.load_line_type("ACAD_ISO04W100")  # 加载线型

    def draw_two_piece_body(self, arg) -> None:
        """
        绘制两片式网身
        self.i_arg index
        0:  网身目大 
        1:  网身纵向目数 
        2:  网身横向目数
        3:  边旁剪裁斜率
        :return: None
        """
        self.part_obj = "tb"  # 网身 two-body
        self.doc.StartUndoMark()
        self.collate_param(arg[0])
        self.confirm_the_clipping_slope__two()
        self.calculate_the_ratio()
        # 计算裁剪后的横向目数
        mesh_len = self.i_arg[2] - self.shears["T"] - self.shears["B"] * 2
        if not self.has_draw_first_segment:
            self.s_pos.extend([
                self.ORI[0]
                - (self.i_arg[0]  # 目大参数
                   * self.i_arg[2]  # 横向目数
                   * self.ZX  # X尺寸比例缩放
                   * 0.5  # 取长度一半
                   ), self.ORI[1]])
            self.s_pos.extend([self.ori_mir(self.s_pos[0]), self.s_pos[1]])
            self.s_pos.extend([
                self.ORI[0]
                + (mesh_len / 2),
                self.s_pos[3]
                - (self.i_arg[0] * self.i_arg[1] * self.ZY)
            ])
            self.s_pos.extend([self.ori_mir(self.s_pos[4]), self.s_pos[5]])
            print(self.s_pos)
            self.pos_write_to_adoc(self.s_pos)
            self.cache["netBody"] = self.s_pos

            self.refresh_pos()  # 刷新坐标
            self.has_draw_first_segment = True
        else:
            self.s_pos.extend(self.cache["preSegment"][6:])
            self.s_pos.extend(self.cache["preSegment"][4:6])
            self.s_pos.extend([
                self.ORI[0]
                + (mesh_len / 2),
                self.s_pos[3]
                - (self.i_arg[0] * self.i_arg[1] * self.ZY)
            ])
            self.s_pos.extend([self.ori_mir(self.s_pos[4]), self.s_pos[5]])
            print(self.s_pos)
            self.pos_write_to_adoc(self.s_pos)  # 绘制CAD线段
            self.refresh_pos()  # 刷新坐标
        self.doc.EndUndoMark()
