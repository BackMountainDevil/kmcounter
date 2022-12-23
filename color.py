import json

def getColor(x,min,max):
    return hex(int(65535 + (x-min) * ((16646145) / (max-min))))

kmdataFile = "kmdata2.json"  # 默认保存的数据文件
colorFile = "kcolor.json"

try:  # 读取文件中 的数据
    dataFile = open(kmdataFile, "r")
    kmdata = json.load(dataFile)
    dataFile.close()
    print("load kmdata from  ", kmdataFile)

    kmax=max(kmdata.items(), key = lambda x: x[1])
    kmin=min(kmdata.items(), key = lambda x: x[1])
    print(kmax,type(kmax),kmin,type(kmdata))

    kcdata={}   # 存储颜色数据
    for k,v in kmdata.items():
        kcdata[k.upper()]=getColor(v, kmin[1], kmax[1])

    dataFile = open(colorFile, "w") # 颜色数据保存到文件
    json.dump(kcdata, dataFile)
    dataFile.close()
    print("kcolor has been saved to ", colorFile)
except FileNotFoundError:
    print("kmdata file not found  ", kmdataFile)
except Exception as ex: # 其它未知错误，比如 JSONDecodeError
    print("Exception:", repr(ex))
