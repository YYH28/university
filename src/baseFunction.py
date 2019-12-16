import xlrd
import matplotlib.pyplot as plt
import numpy as np
import json
from urllib.request import urlopen, quote
import requests,csv
import pandas as pd #导入这些库后边都要用到

#获取经纬度
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = '8atpMUyuexdbuYFU838ejPvSPnWYZoks'
    add = quote(address) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    return temp
#列表数据相加求平均
def sum_list(items):
    sum_numbers = 0
    count=0
    for x in items:
        sum_numbers += x
        count+=1
    return float(sum_numbers/count)

def point_pr(gr,file):
#每个省份的经纬度
    for line in gr:
        # line是个list，取得所有需要的值
        b = line[0] #将第一列city读取出来并清除不需要字符
        if b == '西藏' or b == '':
            continue
        c= line[1]#将第二列price读取出来并清除不需要字符
        lng = getlnglat(b)['result']['location']['lng'] #采用构造的函数来获取经度
        lat = getlnglat(b)['result']['location']['lat'] #获取纬度
        str_temp = '{"lat":' + str(lat) + ',"lng":' + str(lng) + ',"count":' + str(c) +'},'
        # print(str_temp) #也可以通过打印出来，把数据copy到百度热力地图api的相应位置上
        file.write(str_temp) #写入文档
    file.close()