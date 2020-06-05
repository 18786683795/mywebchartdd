#coding: utf-8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.core import serializers
import datetime
import json
import pymysql
import pandas as pd

#conn_SY = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")
#conn_FL = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")
#conn_SD = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")
#conn_CO = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")

conn_SY = pymysql.connect(host="127.0.0.1",user="root",password="root",database="keen_its",charset="utf8")
conn_FL = pymysql.connect(host="127.0.0.1",user="root",password="root",database="keen_its",charset="utf8")
conn_SD = pymysql.connect(host="127.0.0.1",user="root",password="root",database="keen_its",charset="utf8")
conn_CO = pymysql.connect(host="127.0.0.1",user="root",password="root",database="keen_its",charset="utf8")

#ll
def Pie_Bar(dat):
    Xdat = [i['name'] for i in dat]
    Ydat = [i['value'] for i in dat]
    data_br = [Xdat,Ydat]
    return data_br
	
	
def getflow(data,rq):
    flow_h = []
    flow_t = []
    flow_z = []
    flow_w = []
    flow_p = []
    for qy in set(data['regional']):
        data2 = data[data['regional']==qy]
        datah = [qy,rq,[str(x) for x in list(data2[data2.columns[3:]].sum())]]
        flow_h.append(datah)

        datat = {'date':rq,'values':{'name':qy,'value':str(list(data2.sum(axis=1))[0])}}
#        datat = {'code':200,'msg':'success!','data':{'date':rq,'values':{'name':qy,'value':str(list(data2.sum(axis=1))[0])}}}
        flowt = []
        flowt.append(datat)
        for i in flowt:
            flow_t.append(i['values'])
            
        dataz = {'date':rq,'values':{'name':qy,'value':str(list(data2[['time7','time8','time9']].sum(axis=1))[0])}}
        flowz = []
        flowz.append(dataz)
        for i in flowz:
            flow_z.append(i['values'])
            
        dataw = {'date':rq,'values':{'name':qy,'value':str(list(data2[['time17','time18','time19']].sum(axis=1))[0])}}
        floww = []
        floww.append(dataw)
        for i in floww:
            flow_w.append(i['values'])
                    
        datap = {'date':rq,'values':{'name':qy,'value':str(list(data2[data2.columns[9:23]].sum(axis=1))[0])}}
        flowp = []
        flowp.append(datap)
        for i in flowp:
            flow_p.append(i['values'])
    
    flow_t = Pie_Bar(flow_t)
    flow_z = Pie_Bar(flow_z)
    flow_w = Pie_Bar(flow_w)
    flow_p = Pie_Bar(flow_p)
                    
    return {'code':200,'msg':'success!','data':[flow_h,flow_t,flow_z,flow_w,flow_p]}  #加入响应信息，把返回数据封装成列表
	
	
def getsp_co(data,rq):
    flow_h = []
    flow_t = []
    flow_z = []
    flow_w = []
    flow_p = []
    for qy in set(data['regional']):
        data2 = data[data['regional']==qy]
        datah = [qy,rq,[str(x) for x in list(data2[data2.columns[3:]].mean())]]
        flow_h.append(datah)

        datat = {'date':rq,'values':{'name':qy,'value':str(list(round(data2.mean(axis=1),2))[0])}}
        flowt = []
        flowt.append(datat)
        for i in flowt:
            flow_t.append(i['values'])
            
        dataz = {'date':rq,'values':{'name':qy,'value':str(list(round(data2[['time7','time8','time9']].mean(axis=1),2))[0])}}
        flowz = []
        flowz.append(dataz)
        for i in flowz:
            flow_z.append(i['values'])
            
        dataw = {'date':rq,'values':{'name':qy,'value':str(list(round(data2[['time17','time18','time19']].mean(axis=1),2))[0])}}
        floww = []
        floww.append(dataw)
        for i in floww:
            flow_w.append(i['values'])
                    
        datap = {'date':rq,'values':{'name':qy,'value':str(list(round(data2[data2.columns[9:23]].mean(axis=1),2))[0])}}
        flowp = []
        flowp.append(datap)
        for i in flowp:
            flow_p.append(i['values'])

    flow_t = Pie_Bar(flow_t)
    flow_z = Pie_Bar(flow_z)
    flow_w = Pie_Bar(flow_w)
    flow_p = Pie_Bar(flow_p)

    return {'code':200,'msg':'success!','data':[flow_h,flow_t,flow_z,flow_w,flow_p]}
	
#flow
def ajax_flows(request):
    try:
        homedate = request.GET.get("date",'')
        homeregional = request.GET.get("regional",'')
        a1 = homedate[:10]
        a = homedate[:8]+homedate[9] #构造前端传来的日期格式
        print(homedate[:8]+homedate[9])
        print(request.GET)
        #a='2019-12-01'
        b = homeregional
        dat = pd.read_sql('select * from t_regional_hour_flow where date = "'+a+'" and regional = "'+b+'"',conn_FL) #区域和时间作为参数
        data = getflow(dat,a)
        #print(data)
        return HttpResponse(json.dumps(data), content_type='application/json')	
    except Exception as e:
        print(e)
        return HttpResponse('参数错误!')

	
#sp
def ajax_speeds(request):
    try:
        homedate = request.POST.get("date",'')
        homeregional = request.POST.get("regional",'')
        a1 = homedate[:10]
        a = homedate[:8]+homedate[9] #构造前端传来的日期格式
        #a='2019-12-01'
        b = homeregional
        dat = pd.read_sql('select * from t_regional_hour_speed where date = "'+a+'" and regional = "'+b+'"',conn_SD) #区域和时间作为参数
        data = getsp_co(dat,a)
        return HttpResponse(json.dumps(data), content_type='application/json')	
    except Exception as e:
        print(e)
        return HttpResponse('参数错误!')
#co
def ajax_congests(request):
    try:
        homedate = request.GET.get("date",'')
        homeregional = request.GET.get("regional",'')
        a1 = homedate[:10]
        a = homedate[:8]+homedate[9] #构造前端传来的日期格式
        #a='2019-12-01'
        b = homeregional
        dat = pd.read_sql('select * from t_regional_hour_congestion where date = "'+a+'" and regional = "'+b+'"',conn_CO) #区域和时间作为参数
        data = getsp_co(dat,a)
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse('参数错误!')

def getFlowData(request):
    return render(request,'flowdata.html')

def getSpeedData(request):
    return render(request,'speeddata.html')

def getCongestData(request):
    return render(request,'congestdata.html')	
	
	
	
#shouye
def get_paramers(request):
    homedate = request.GET.get("date",'')
    homeregional = request.GET.get("regional",'')
    a1 = homedate[:10]
    a = homedate[:8]+homedate[9]  #构造前端传来的日期格式
    #print(request.GET)
    #print(a)
    #a='2019-12-01'
    b = homeregional
    return a
	
def getshouye(request,a):
    dataf = pd.read_sql('select * from t_regional_hour_flow where date = "'+a+'"',conn_SY)
    contextf1 = int(dataf[dataf.columns[3:]].mean().sum())
    contextf = [a,contextf1]

    datas = pd.read_sql('select * from t_regional_hour_speed where date = "'+a+'"',conn_SY)
    contexts1 = round(datas[datas.columns[3:]].mean().mean(),2)
    contexts = [a,contexts1]

    datac = pd.read_sql('select * from t_regional_hour_congestion where date = "'+a+'"',conn_SY)
    contextc1 = round(datac[datac.columns[3:]].mean().mean(),2)
    contextc = [a,contextc1]
 
    return {'code':200,'msg':'success!','data':[a,contextf,contexts,contextc]}

def getshouyes(request):
    try:
        homedate = request.GET.get("date",'')
        a = homedate[:8]+homedate[9] #构造前端传来的日期格式
        import json
        shouyes = getshouye(request,a)
        return  HttpResponse(json.dumps(shouyes), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse('参数错误!')

def getShouyeData(request):
    return render(request,'index.html')	
	


	
#########报告接口##报告接口#####报告接口########报告接口####报告接口#################################################################################################################
    
#新添加的用于报表的文件
import os
from django.http import StreamingHttpResponse
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm, Inches, Pt
from datetime import datetime

path_name = "E:/GZ/Django/Django_API-1/DJangoDRF/mywebchartdd/"


#加载前端下载页面
#def home(request):
#    """Renders the home page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/index.html',
#        {
#            'title':'Home Page',
#            'year':datetime.now().year,
#        }
#    )



# 流方式读取文件
def read_file(file_name, size):
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break


#def delete_docx_file(filepath):
#    if os.path.exists(filepath):
#        files = os.listdir(filepath)
#        for file in files:
#            if file != "template.docx":
#                os.remove(os.path.join(filepath, file))
                
            
#直接生成图片
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

#使用pyecharts画图，需要启用浏览器生成图片会很慢
#def bar_chart() -> Bar:
#    c = (
#        Bar()
#        .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
#        .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
#        .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
#        .reversal_axis()
#        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
#        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-测试渲染图片"))
#    )
#    return c
#
#make_snapshot(snapshot, bar_chart().render(), img_name)


#使用matplotlib画图
import numpy as np
import matplotlib.pyplot as plt

def plt_fc(img_name):
    t = np.arange(0, 69, 1)
    plt.plot(t, t, 'r', t, t**2, 'b')
    label = ['t', 't**2']
    plt.legend(label, loc='upper left')
    plt.savefig(img_name)
    #plt.show()


'''
#报告生成接口
img_name = path_name+datetime.now().strftime("%Y-%m-%d")+".png"
report_name = path_name+datetime.now().strftime("%Y-%m-%d")+".docx"
#@api_view(['GET'])
def generatereport0(request):
    filename = report_name        # 所生成的word文档需要以.docx结尾，文档格式需要
    filepath = path_name
    template_path = os.getcwd() + '/test.docx'  #加载模板文件
    template = DocxTemplate(template_path)
    if os.path.exists(img_name) == False:  #判断下面代码使用的图片是否存在，不存在则调用函数生成
        plt_fc()
    context = {'text': '哈哈哈，来啦',
           't1':'燕子',
            't2':'杨柳',
            't3':'桃花',
            't4':'针尖',
            't5':'头涔涔',
            't6':'泪潸潸',
            't7':'茫茫然',
            't8':'伶伶俐俐',
            'picture1': InlineImage(template, img_name, width=Mm(80), height=Mm(60)),}

    user_labels = ['姓名', '年龄', '性别', '入学日期']
    context['user_labels'] = user_labels
    user_dict1 = {'number': 1, 'cols': ['林小熊', '27', '男', '2019-03-28']}
    user_dict2 = {'number': 2, 'cols': ['林小花', '27', '女', '2019-03-28']}
    user_list = []
    user_list.append(user_dict1)
    user_list.append(user_dict2)

    context['user_list'] = user_list
    template.render(context)
    

    template.save(os.path.join(filepath,filename))
    response = StreamingHttpResponse(read_file(os.path.join(filepath, filename), 512))
    response['Content-Type'] = 'application/msword'        #msword是输出word文件
#    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    # time.sleep(10)
    if os.path.exists(filename):
        data = {'code':200,'msg': 'success!','report_name':filename}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse('报告生成失败!')
'''


#定时调用生成报告的方法，只能生成当天的报告
img_name = path_name+datetime.now().strftime("%Y-%m-%d")+".png"
report_name = path_name+datetime.now().strftime("%Y-%m-%d")+".docx"

def generatereport_ds():
    filename = report_name        # 所生成的word文档需要以.docx结尾，文档格式需要
    filepath = path_name
    
    template_path = os.getcwd() + '/test.docx'  #加载模板文件
    template = DocxTemplate(template_path)
    if os.path.exists(img_name) == False:  #判断下面代码使用的图片是否存在，不存在则调用函数生成
        plt_fc(img_name)
    context = {'text': '哈哈哈，来啦',
           't1':'燕子',
            't2':'杨柳',
            't3':'桃花',
            't4':'针尖',
            't5':'头涔涔',
            't6':'泪潸潸',
            't7':'茫茫然',
            't8':'伶伶俐俐',
            'picture1': InlineImage(template, img_name, width=Mm(80), height=Mm(60)),}

    user_labels = ['姓名', '年龄', '性别', '入学日期']
    context['user_labels'] = user_labels
    user_dict1 = {'number': 1, 'cols': ['林小熊', '27', '男', '2019-03-28']}
    user_dict2 = {'number': 2, 'cols': ['林小花', '27', '女', '2019-03-28']}
    user_list = []
    user_list.append(user_dict1)
    user_list.append(user_dict2)

    context['user_list'] = user_list
    template.render(context)
    template.save(os.path.join(filepath,filename))
    

#生成报告的方法
def generatereport(d):
#    filename = report_name        # 所生成的word文档需要以.docx结尾，文档格式需要
    filepath = path_name
    img_name = path_name+d+".png"
    filename = path_name+d+".docx"
    
    template_path = os.getcwd() + '/test.docx'  #加载模板文件
    template = DocxTemplate(template_path)
    if os.path.exists(img_name) == False:  #判断下面代码使用的图片是否存在，不存在则调用函数生成
        plt_fc(img_name)
    context = {'text': '哈哈哈，来啦',
           't1':'燕子',
            't2':'杨柳',
            't3':'桃花',
            't4':'针尖',
            't5':'头涔涔',
            't6':'泪潸潸',
            't7':'茫茫然',
            't8':'伶伶俐俐',
            'picture1': InlineImage(template, img_name, width=Mm(80), height=Mm(60)),}

    user_labels = ['姓名', '年龄', '性别', '入学日期']
    context['user_labels'] = user_labels
    user_dict1 = {'number': 1, 'cols': ['林小熊', '27', '男', '2019-03-28']}
    user_dict2 = {'number': 2, 'cols': ['林小花', '27', '女', '2019-03-28']}
    user_list = []
    user_list.append(user_dict1)
    user_list.append(user_dict2)

    context['user_list'] = user_list
    template.render(context)
    template.save(os.path.join(filepath,filename))

   
#调用生成报告的方法来生成报告的接口
def generatereports(request):
    try:
        homedate = request.GET.get("date",'')
#        a1 = homedate[:8]+homedate[9] #构造前端传来的日期格式
        a = homedate[:10]  #获取前端传来的日期格式
        report_na = path_name+a+".docx"
        
        if os.path.exists(report_na):
            data = {'code':200,'msg': 'Report already exists!','report_name':report_na}
            return HttpResponse(json.dumps(data), content_type='application/json')
        elif os.path.exists(report_na) == False:
            generatereport(a)
            report_na1 = path_name+a+".docx"
            data1 = {'code':200,'msg': 'Report generated successfully!','report_name':report_na1}
            return HttpResponse(json.dumps(data1), content_type='application/json')
        else:
            return HttpResponse('报告生成失败！')
    except Exception as e:
        print(e)
        return HttpResponse('参数错误!')   
    
    
#报告查询接口
def queryreport(request):
    try:
        homedate = request.GET.get("date",'')
#        a1 = homedate[:8]+homedate[9] #构造前端传来的日期格式
        a = homedate[:10]  #获取前端传来的日期格式
        report_na = path_name+a+".docx"
        
        if os.path.exists(report_na):
            data = {'code':200,'msg': 'Report query successfully!','data':{'date':a,'path_name':path_name,'report_name':report_na}}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponse('报告未找到！')
    except Exception as e:
        print(e)
        return HttpResponse('参数错误!')   
    

    
    
    
    
    
    
    
    
    
    
    
    
    

