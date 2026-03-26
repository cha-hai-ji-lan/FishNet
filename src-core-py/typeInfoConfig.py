import pythoncom  # 引入COM操作模块
import win32com.client as win32  # 引入win32com模块


# 将坐标点浮点数转化为可识别的COM中的一种数组或8 字节浮点数数据类型
def coordinateToArrOrFloatVT(x_coord, y_coord, z_coord=0):
    return win32.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x_coord, y_coord, z_coord))


# 将列表转化为可识别的COM中的一种数组或数据类型
def listTOFloatVT(list_ori):
    return win32.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list_ori)


# 将字符串转化为可识别的COM中的一种字符串数据类型
def sentenceTOStringVT(str_ori):
    return win32.VARIANT(pythoncom.VT_BSTR, str_ori)
