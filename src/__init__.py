# 集美大学各省录取分数分析(学号尾数为2，3同学完成)
# 分析文件‘集美大学各省录取分数.xlsx’，完成：
# 1）集美大学2015-2018年间不同省份在本一批的平均分数，柱状图展示排名前10的省份，
# 2）分析福建省这3年各批次成绩情况，使用折线图展示结果，并预测2019年录取成绩（数据不够，可前往集美大学招生办获取更多数据）,
# 3）分析其他省份数据。有精力同学可以研究热力图，地图方式绘制所有省份数据情况。
import xlrd
import matplotlib.pyplot as plt
import numpy as np
import json
from urllib.request import urlopen, quote
import requests,csv
import pandas as pd #导入这些库后边都要用到
from src.baseFunction import getlnglat
from src.baseFunction import sum_list
from src.baseFunction import point_pr
#设置中文乱码
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
excel_path="..\\grade.xlsx"
#打开文件，获取excel文件的workbook（工作簿）对象
excel=xlrd.open_workbook(excel_path,encoding_override="utf-8")
# 返回所有Sheet对象的list
all_sheet=excel.sheets()
#循环遍历每个sheet对象存储表中所有数据
grade_list=[]
#列表分类名称
grade_sort=[]
#省份列表
province_list=[]
#计数
count=0
#平均数和
sum = 0
#将前十的省份和平均数存进列表
province_dict_keys=[]
province_dict_values=[]

province_dict={ }  #省份字典

def main():

    #查找相应批次和专业，算平均数
    def batch(batch_bactch,bacth_class):
        sum=0
        count=0
        for e in province_dict:
            for grade_list_row in grade_list:
                if e==grade_list_row[0]:
                    if batch_bactch in grade_list_row[1] and bacth_class in grade_list_row[2]:
                        sum += grade_list_row[6]
                        count += 1
            if count >= 1:
                province_dict[e]=int(sum/count)
            else:
                province_dict[e]=sum
            sum=0
            count=0
        return province_dict

    # 将文件中数据存进grade_list
    for sheet in all_sheet:
        for each_row in range(sheet.nrows):#循环打印每一行
            grade_list.append(sheet.row_values(each_row))
    # 将表头说明放入grade_sort
    grade_sort=grade_list[0]
    # 删除列表['省份', '批次', '科类', '省控线', '最高分', '最低分', '平均分', '年份']
    grade_list.pop(0)

    # 提取省份
    for grade_list_row in grade_list:
        for e in range(len(grade_list_row)):
            if grade_list_row[0] not in province_list:
                province_list.append(grade_list_row[0])
    province_dict=dict.fromkeys(province_list)  #将省份列表添加到字典中
    #查找本一批，算平均数
    province_dict1=batch('本一批','')
    #排序
    province_dict_order=sorted(province_dict1.items(),key=lambda x:x[1],reverse=True)
    #将前十的省份和平均数存进列表
    for e in province_dict_order[:10]:
        province_dict_keys.append(e[0])
        province_dict_values.append(e[1])
    #绘图
    plt.figure()
    plt.bar(x=province_dict_keys,height=province_dict_values,alpha=0.8)
    for x,y in enumerate(province_dict_values):
        plt.text(x, y, '%s' % y, ha='center', va='bottom')
    #设置标题
    plt.title("排名前10的省份")
    # 为两条坐标轴设置名称
    plt.xlabel("省份")
    plt.ylabel("平均分")
    #图片的显示及存储
    log = datetime.datetime.now().strftime('%Y-%m-%d')
    # plt.savefig('./logging/%s_all_a.jpg' % log)   #图片的存储
    # plt.close()   #关闭matplotlib

    #存储福建省3年的成绩
    grade_fujian=[]
    #存储福建省批次
    grade_batch=[]
    #存储福建省批次年份
    grade_year=["2016","2017","2018","2019"]
    grade=[]
    grade1=[]
    grade2=[]
    grade3=[]
    grade4=[]
    grade5=[]
    grade6=[]
    grade7=[]
    grade8=[]
    #3文史变量
    grade1_1=[]
    grade2_2=[]
    grade3_3=[]
    grade4_4=[]
    grade5_5=[]
    grade7_7=[]
    #分析福建省这3年各批次成绩情况，使用折线图展示结果，并预测2019年录取成绩
    #提取福建省
    for grade_list_row in grade_list:
        if grade_list_row[0] in "福建省":
            grade_fujian.append(grade_list_row)
    for e in grade_fujian:
        if '提前批航海类' in e[1] and e[2] in '理工':
            grade.append(e[6])
        elif '师范类(面向全省)' in e[1] and e[2] in '理工':
            grade1.append(e[6])
        elif '师范类(面向厦门)' in e[1] and e[2] in '理工':
            grade2.append(e[6])
        elif '农村专项计划' in e[1] and e[2] in '理工':
            grade3.append(e[6])
        elif '本一批'==e[1] and e[2] in '理工':
            grade4.append(e[6])
        elif '本一批(面向厦门)'==e[1] and e[2] in '理工':
            grade5.append(e[6])
        elif '闽台合作' in e[1] and e[2] in '理工':
            grade6.append(e[6])
        elif '预科批' in e[1] and e[2] in '理工':
            grade7.append(e[6])
        elif '师范类(面向全省)' in e[1] and e[2] in '文史':
            grade1_1.append(e[6])
        elif '师范类(面向厦门)' in e[1] and e[2] in '文史':
            grade2_2.append(e[6])
        elif '农村专项计划' in e[1] and e[2] in '文史':
            grade3_3.append(e[6])
        elif '本一批'==e[1] and e[2] in '文史':
            grade4_4.append(e[6])
        elif '本一批(面向厦门)'==e[1] and e[2] in '文史':
            grade5_5.append(e[6])
        elif '预科批' in e[1] and e[2] in '文史':
            grade7_7.append(e[6])
    #求2019年的录取分数理工
    grade.append(sum_list(grade))
    grade1.append(sum_list(grade1))
    grade2.append(sum_list(grade2))
    grade3.append(sum_list(grade3))
    grade4.append(sum_list(grade4))
    grade5.append(sum_list(grade5))
    grade6.append(sum_list(grade6))
    grade7.append(sum_list(grade7))
    #文史
    grade1_1.append(sum_list(grade1_1))
    grade2_2.append(sum_list(grade2_2))
    grade3_3.append(sum_list(grade3_3))
    grade4_4.append(sum_list(grade4_4))
    grade5_5.append(sum_list(grade5_5))
    grade7_7.append(sum_list(grade7_7))
    #折线图
    plt.figure()
    plt.plot(grade_year,grade,'ro-', color='#4169E1', alpha=0.8, label='提前批航海类（理工）')
    plt.plot(grade_year,grade1,'ro-', color='#FFFA12', alpha=0.8, label='师范类(面向全省)（理工）')
    plt.plot(grade_year,grade2,'ro-', color='#78FF1D', alpha=0.8, label='师范类(面向厦门)（理工）')
    plt.plot(grade_year,grade3,'ro-', color='#1CFFB7', alpha=0.8, label='农村专项计划（理工）')
    plt.plot(grade_year,grade4,'ro-', color='#1BE9FF', alpha=0.8, label='本一批（理工）')
    plt.plot(grade_year,grade5,'ro-', color='#1F98FF', alpha=0.8, label='本一批(面向厦门)（理工）')
    plt.plot(grade_year,grade6,'ro-', color='#2237FF', alpha=0.8, label='闽台合作（理工）')
    plt.plot(grade_year,grade7,'ro-', color='#BA6BFF', alpha=0.8, label='预科批（理工）') #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    for y in [grade,grade1,grade2,grade3,grade4,grade5,grade6,grade7]:
        for x,yy in zip(grade_year,y):
            plt.text(x, yy+1,str(yy), ha='center', va='bottom', fontsize=7)
    plt.xlabel("年份") #X轴标签
    plt.ylabel("分数线") #Y轴标签
    plt.title("福建省这3年理工各批次成绩情况") #标题
    # plt.savefig('./logging/%s_all_b.jpg' % log)   #图片的存储

    plt.figure()
    plt.plot(grade_year,grade1_1,'ro-', color='#FFFA12', alpha=0.8, label='师范类(面向全省)（文史）')
    plt.plot(grade_year,grade2_2,'ro-', color='#78FF1D', alpha=0.8, label='师范类(面向厦门)（文史）')
    plt.plot(grade_year,grade3_3,'ro-', color='#1CFFB7', alpha=0.8, label='农村专项计划（文史）')
    plt.plot(grade_year,grade4_4,'ro-', color='#1BE9FF', alpha=0.8, label='本一批（文史）')
    plt.plot(grade_year,grade5_5,'ro-', color='#1F98FF', alpha=0.8, label='本一批(面向厦门)（文史）')
    plt.plot(grade_year,grade7_7,'ro-', color='#BA6BFF', alpha=0.8, label='预科批（文史）') #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    for y in [grade1_1,grade2_2,grade3_3,grade4_4,grade5_5,grade7_7]:
        for x,yy in zip(grade_year,y):
            plt.text(x, yy+1,str(yy), ha='center', va='bottom', fontsize=7)
    plt.xlabel("年份") #X轴标签
    plt.ylabel("分数线") #Y轴标签
    plt.title("福建省这3年文史各批次成绩情况") #标题
    # plt.savefig('./logging/%s_all_c.jpg' % log)   #图片的存储
    #显示图示
    plt.legend()
    plt.show()

    gr=batch('本一批','理工')
    gr=sorted(gr.items(),key=lambda x:x[1],reverse=True)
    file = open(r'../point.json','w') #建立json数据文件
    point_pr(gr,file)

    gr1=batch('本一批','')
    gr1=sorted(gr1.items(),key=lambda x:x[1],reverse=True)
    file = open(r'../point1.json','w') #建立json数据文件
    point_pr(gr1,file)

    # gr2=batch('','')
    gr2=province_dict
    sum=0
    count=0
    for e in province_dict:
        for grade_list_row in grade_list:
            if grade_list_row[0]=='':
                continue
            if e==grade_list_row[0]:
                sum =sum+ grade_list_row[6]
        gr2[e]=sum
        sum=0
    gr2=sorted(gr2.items(),key=lambda x:x[1],reverse=True)
    file = open(r'../point2.json','w') #建立json数据文件
    for line in gr2:
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
if __name__=='__main__':
    main()