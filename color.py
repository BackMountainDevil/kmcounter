"""
将统计数据转换为热力图
键盘数据来自 http://www.keyboard-layout-editor.com/
"""
import json


def getColor(x, min, max):
    return hex(int(65535 + (x - min) * ((16646145) / (max - min))))


kmdataFile = "kmdata2.json"  # 默认保存的数据文件
colorFile = "kcolor.json"

try:  # 读取文件中 的数据
    dataFile = open(kmdataFile, "r")
    kmdata = json.load(dataFile)
    dataFile.close()
    print("load kmdata from  ", kmdataFile)

    kmax = max(kmdata.items(), key=lambda x: x[1])
    kmin = min(kmdata.items(), key=lambda x: x[1])
    print(kmax, type(kmax), kmin, type(kmdata))

    kcdata = {}  # 存储颜色数据
    ksum = 0  # 总按键次数：所有按键一共被按下了多少次
    knum = 0  # 按键总数：有多少个按键
    for k, v in kmdata.items():  # 合并大小写数据在一起
        ksum = ksum + v
        if len(k) == 1 and k.upper() not in kcdata:
            kcdata[k.upper()] = v  # getColor(v, kmin[1], kmax[1])
        elif len(k) == 1:  # 将a~z A~Z 大小写的数据合并在一起
            kcdata[k.upper()] = kcdata[k.upper()] + v  # getColor(v, kmin[1], kmax[1])
        else:
            kcdata[k] = v  # getColor(v, kmin[1], kmax[1])
    print("总按键次数: ", ksum)

    for k, v in kcdata.items():  # 次数转颜色
        knum = knum + 1
        kcdata[k] = getColor(v, kmin[1], kmax[1])
    print("按键总数: ", knum)
    print("平均数: ", ksum / knum)

    dataFile = open(colorFile, "w")  # 颜色数据保存到文件
    json.dump(kcdata, dataFile)
    dataFile.close()
    print("kcolor has been saved to ", colorFile)
except FileNotFoundError:
    print("kmdata file not found  ", kmdataFile)
except Exception as ex:  # 其它未知错误，比如 JSONDecodeError
    print("Exception:", repr(ex))
