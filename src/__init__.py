# 集美大学各省录取分数分析(学号尾数为2，3同学完成)
# 分析文件‘集美大学各省录取分数.xlsx’，完成：
# 1）集美大学2015-2018年间不同省份在本一批的平均分数，柱状图展示排名前10的省份，
# 2）分析福建省这3年各批次成绩情况，使用折线图展示结果，并预测2019年录取成绩（数据不够，可前往集美大学招生办获取更多数据）,
# 3）分析其他省份数据。有精力同学可以研究热力图，地图方式绘制所有省份数据情况。
import xlrd
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen, quote
import requests,csv
import pandas as pd #导入这些库后边都要用到
from pyecharts import Line,Bar,Pie
import json
from werkzeug.utils import redirect
from flask import Flask, jsonify, render_template, request, url_for

app = Flask(__name__)

#设置中文乱码
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

def main():
    # 列表数据相加求平均
    def sum_list(items):
        sum_numbers = 0
        count = 0
        for x in items:
            sum_numbers += x
            count += 1
        return int(sum_numbers / count)

    def removeNull(alist):
        for i in alist:
            if i == '':
                alist.remove(i)
        return alist

        # 查找相应批次和专业，算平均数
    def batch(batch_bactch, bacth_class):
        for e in province_dict:
            sum = 0
            count = 0
            for grade_list_row in grade_list:
                if e == grade_list_row[0]:
                    if batch_bactch in grade_list_row[1] and bacth_class in grade_list_row[2]:
                        sum += int(grade_list_row[6])
                        count += 1
            if count >= 1:
                province_dict[e] = int(sum / count)
            else:
                province_dict[e] = sum
        return province_dict
    #字典的前十key values
    def topTenKey(dict_order):
        count = 0
        order=[]
        for key in dict_order.keys():
            count+=1
            if count>10:
                break
            else:
                order.append(key)
        return order
    def topTenValue(dict_order):
        count = 0
        order=[]
        for key in dict_order.values():
            count+=1
            if count>10:
                break
            else:
                order.append(key)
        return order
    def tenYear(province_dict,year):
        # 将前十的省份和平均数存进列表
        print(year)
        province_dict_keys = []
        province_dict_values = []
        for province in province_dict:
            sum=0
            count=0
            for i in grade_list:
                if "本一批" in i[1] and 2015 == i[7] and province in i[0]:
                    sum+=i[3]
                    count+=1
            if count >= 1:
                province_dict[province] = int(sum / count)
            else:
                province_dict[province] = sum
        for k in list(province_dict.keys()):
            if not province_dict[k]:
                del province_dict[k]
        province_dict = dict(sorted(province_dict.items(), key=lambda x: x[1], reverse=True))
        province_dict_keys = topTenKey(province_dict)
        province_dict_values=topTenValue(province_dict)
        print(province_dict_keys,province_dict_values)
        bar = Bar("柱状图", "%s本一批的平均分数"%year)
        bar.add("平均录取分数", province_dict_keys, province_dict_values, mark_line=["average"], mark_point=["max", "min"])
        # 生成本地文件（默认为.html文件）
        bar.render('./templates/ten.html')
        province_dict=[]
    def otherProvince1(otherProvince):
        print(otherProvince)
        #省份全部数据
        grade_other=[]
        #省份的批次分类
        grade_batch=[]
        #各批次成绩
        batch_grade=[]
        #提取相应省份
        for grade_list_row in grade_list:
            if grade_list_row[0] ==otherProvince:
                grade_other.append(grade_list_row)
        print(grade_other)
        #提取相应省份的批次
        for batch in grade_other:
            if batch[1] not in grade_batch:
                grade_batch.append(batch[1])
        print(grade_batch)
        #计算各批次成绩
        for batch in grade_batch:
            list1=[]
            for grade_list_row in grade_other:
                if batch==grade_list_row[1]:
                    list1.append(grade_list_row[6])
            batch_grade.append(sum_list(list1))
            print(batch_grade)
        print(batch_grade)
        line = Line("折线图","%s批次情况分析"%otherProvince)
        line.add("", grade_batch, batch_grade, is_label_show=True)
        line.render('./templates/otherProvince.html')

    excel_path="..\\grade.xlsx"
    #打开文件，获取excel文件的workbook（工作簿）对象
    excel=xlrd.open_workbook(excel_path,encoding_override="utf-8")
    # 返回所有Sheet对象的list
    all_sheet=excel.sheets()
    #循环遍历每个sheet对象存储表中所有数据
    grade_list=[]
    # 将文件中数据存进grade_list
    for sheet in all_sheet:
        for each_row in range(sheet.nrows):#循环打印每一行
            grade_list.append(sheet.row_values(each_row))
    # 删除列表['省份', '批次', '科类', '省控线', '最高分', '最低分', '平均分', '年份']
    grade_list.pop(0)
    grade_list=removeNull(grade_list)
    #省份列表
    province_list=[]
    province_dict={ }  #省份字典
    # 提取省份
    for grade_list_row in grade_list:
        if grade_list_row[0] not in province_list:
            province_list.append(grade_list_row[0])
    province_list=removeNull(province_list)
    province_dict=dict.fromkeys(province_list)  #将省份列表添加到字典中
    #存储福建省3年的成绩
    grade_fujian=[]
    #存储福建省批次
    grade_batch=[]

    #分析福建省这3年各批次成绩情况，使用折线图展示结果，并预测2019年录取成绩
    for grade_list_row in grade_list:
        if grade_list_row[0] =="福建":
            grade_fujian.append(grade_list_row)
    #福建省批次
    for batch in grade_fujian:
        if batch[1] not in grade_batch:
            grade_batch.append(batch[1])
    batch_grade=[]
    for batch in grade_batch:
        list1=[]
        for grade_list_row in grade_fujian:
            if batch==grade_list_row[1]:
                list1.append(grade_list_row[6])
        batch_grade.append(sum_list(list1))
    # //设置主标题与副标题，标题设置居中，设置宽度为900
    pie = Pie("饼状图", "福建省这3年各批次成绩情况",title_pos='top',width=900)
    # //加入数据，设置坐标位置为【25，50】，上方的colums选项取消显示
    pie.add("降水量", grade_batch, batch_grade ,center=[40,50],is_legend_show=False,is_label_show=True)
    # //保存图表
    pie.render('./templates/pie_batch.html')

    @app.route("/index")
    def index():
        return render_template("Base.html")

    @app.route("/ten")
    def ten():
        return render_template("ten.html")

    @app.route("/pie_batch")
    def pie_batch():
        return render_template("pie_batch.html")

    @app.route("/otherProvince")
    def otherProvince():
        return render_template("otherProvince.html")

    @app.route('/test',methods=['POST'])
    def testGet():
        year = request.form.get('year')
        tenYear(province_dict,int(year))
        print("执行get")
        return render_template("Base.html")

    @app.route('/test1',methods=['POST'])
    def testGet1():
        otherProvince = request.form.get('otherProvince')
        otherProvince1(str(otherProvince))
        print("执行get1")
        return render_template("Base.html")
if __name__ == '__main__':
    main()
    app.run(host='127.0.0.1', port=8080, debug=True)