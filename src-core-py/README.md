# AcadCore
---

## ACAD :[Example]:

> AcadCore 用于直接操作CAD绘制图形

### function:

- [connectCAD](#connectCAD)
- [draw_two_piece_body](#draw_two_piece_body)

#### connectCAD

> 用于连接到 AutoCAD
>
> 如果 当前无打开的CAD则启动创建Auto CAD的实例并创建连接
>

#### draw_two_piece_body

> 用于绘制网身
> 
> 获取CLI传递进来的前四位固定,后续位不定长参数
> 
> **注意**
> 
> 网身以及网袖的剪裁斜率方案都源自于
> 
> AB 全斜边 || AN: 直边 斜边 || N全直边 || B: 1:1
> 

**绘画可能出现的情况**

1. 第一段不为网囊
2. 第一段为网囊
3. 第二段以及后续段为网囊
> **注意：**
> 1. 第二段及其后续段为网囊且前一段为网囊
>   > 按比例缩放图例的 point1 以及 point2的位置
>   > 
>   > **收到的新的一段必须有横向目数**
> 2. 第二段及其后续段为网囊且前一段不为网囊
>   > point1 以及 point2的位置继承前一段的point4 以及 point3的位置
## Config :[CoreParam]:

> 配置文件字典
>
> |       key        |  info  | defaultValue |
> |:----------------:|:------:|:------------:|
> | annotationOffset |  注释偏移  |      2       |
> | sheetTextHeight  | 表格文字高度 |      7       |
> |     material     |   材质   |     PA6      |
> |  originPosition  |  原点位置  |   100,100    |
> |      scaleX      |  X缩放   |     0.5      |
> |      scaleY      |  Y缩放   |      1       |
> |   tableOffset    |  表格偏移  |     100      |
> |    textHeight    |  文字高度  |     2.5      |
> |       zoom       |   缩放   |     0.01     |
>

**注意：**

originPosition : 这里的原点指的是中心对称线所在的点

## arg :[userinputParam]:

> 用户输入参数
>
> **规范**
>
> 1.输入参数将以 Vector 形式传递给后端
>
> 2.输入核心参数顺序起始必须以**网身目大 ,网身纵向目数 ,网身横向目数, ?(用于上袖下袖第一段)缝合目数**的顺序作为起始
>
> 3.核心末尾参数必须以 **宕眼剪裁斜率**,**边旁剪裁斜率**的顺序结尾
> 
> 4.辅助参数 "-cfg-wireDiameter" => ?线径规格
>

## undo 撤回操作

```python
self.doc.SendCommand("_.UNDO\n_MARK\n")  # 撤销标记
self.doc.SendCommand("_.UNDO\n_BACK\n")  # 撤销
self.doc.StartUndoMark()  # 原子操作开始标记
self.doc.EndUndoMark()  # 原子操作结束标记
# 回退一步（即回退 StartUndoMark/EndUndoMark 之间的所有操作）
self.doc.SendCommand("_.UNDO\n1\n")
# 或者使用 COM API
self.doc.Undo(1)  # 参数表示撤销步
# ✅ 正确：重做一步
self.doc.SendCommand("_.REDO\n")
# ✅ 正确：重做多步
self.doc.SendCommand("_.REDO\n3\n")
```

## cache :[inlineParam]:

> 缓存参数
>
>   |       key       |     info     |
>   |:---------------:|:------------:|
>   |     netBody     |   网身段1四点坐标   |
>   |     netBody     |   网身段1四点坐标   |
>   |   preSegment    |    前一段点坐标    |
>   | eyeSlopePosMark | 宕眼剪裁斜率标注位置坐标 |
> 

## 注 :[INFO]:

### 常见公制尺寸
**1.8mm、2.5mm、3.5mm、5mm、7mm、10mm、14mm、20mm**