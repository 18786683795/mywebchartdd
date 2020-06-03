#coding: utf-8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.core import serializers

def getJSON1(request):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8")
    conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select city,dat from meimei',conn)
    cb=[i for i in context['city']]
    xz=[i for i in context['dat'].apply(str)]
    ret=[cb,xz]
    #context[context.columns[3:]] = context[context.columns[3:]].applymap(str)
    #ret = context.to_json()
    #ret = json.loads(ret)
    return HttpResponse(json.dumps(ret), content_type='application/json')

def getflow0():
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="keen_its",charset="utf8")
    conn = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")
    data = pd.read_sql('select * from t_regional_hour_flow',conn)  # where regional="520115" and date in ("2019-12-1","2019-12-2")
    #data = data[data.columns[1:]]
    flow_h = []
    flow_t = []
    flow_z = []
    flow_w = []
    flow_p = []
    for qy in set(data['regional']):
        data1 = data[data['regional']==qy]
        for rq in set(data['date']):
            data2 = data1[data1['date']==rq]
            datah = [qy,rq,u'小时',[str(x) for x in list(data2[data2.columns[3:]].sum())]]
            flow_h.append(datah)
            datat = [qy,rq,r'全天',str(list(data2.sum(axis=1))[0])]
            flow_t.append(datat)
            dataz = [qy,rq,r'早高峰',str(list(data2[['time7','time8','time9']].sum(axis=1))[0])]
            print(dataz)
            flow_z.append(dataz)
            dataw = [qy,rq,r'晚高峰',str(list(data2[['time17','time18','time19']].sum(axis=1))[0])]
            flow_w.append(dataw)
            datap = [qy,rq,r'平峰',str(list(data2[data2.columns[9:23]].sum(axis=1))[0])]
            print(datap)
            flow_p.append(datap)
    return flow_h,flow_t,flow_z,flow_w,flow_p

#ll
def Pie_Bar(dat):
    Xdat = [i['name'] for i in dat]
    Ydat = [i['value'] for i in dat]
    data_br = [Xdat,Ydat]
    return data_br


rq='2019-12-01'
qy='520115'
def getflow(rq,qy):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="keen_its",charset="utf8")
    conn = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")
    data = pd.read_sql('select * from t_regional_hour_flow',conn)
    #data = data[data.columns[1:]]
    flow_h = []
    flow_t = []
    flow_z = []
    flow_w = []
    flow_p = []

    data1 = data[data['regional']==qy]
    data2 = data1[data1['date']==rq]
    datah = [qy,rq,[str(x) for x in list(data2[data2.columns[3:]].sum())]]
    flowh = []
    flow_h.append(datah)

    datat = {'date':rq,'values':{'name':qy,'value':str(list(data2.sum(axis=1))[0])}}
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
                    
    return flow_h,flow_t,flow_z,flow_w,flow_p



def getflows(request):	  
    import json  
    flow = getflow(rq,qy)
    return  HttpResponse(json.dumps(flow), content_type='application/json')





#sd
def getspeed(rq,qy):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="keen_its",charset="utf8")
    conn = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")
    data = pd.read_sql('select * from t_regional_hour_speed',conn)
    #data = data[data.columns[1:]]
    flow_h = []
    flow_t = []
    flow_z = []
    flow_w = []
    flow_p = []
    data1 = data[data['regional']==qy]
    data2 = data1[data1['date']==rq]
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

    return flow_h,flow_t,flow_z,flow_w,flow_p

def getspeeds(request):
    import json
    speed = getspeed(rq,qy)
    return  HttpResponse(json.dumps(speed), content_type='application/json')


#zs
def getcongest(rq,qy):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="keen_its",charset="utf8")
    conn = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")
    data = pd.read_sql('select * from t_regional_hour_congestion',conn)
    data = data[data.columns[1:]]
    flow_h = []
    flow_t = []
    flow_z = []
    flow_w = []
    flow_p = []
    data1 = data[data['regional']==qy] 
    data2 = data1[data1['date']==rq] 
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

    return flow_h,flow_t,flow_z,flow_w,flow_p

def getcongests(request):
    import json
    congestion = getcongest(rq,qy)
    return  HttpResponse(json.dumps(congestion), content_type='application/json')


def getFlowData(request):
    return render(request,'flowdata.html')

def getSpeedData(request):
    return render(request,'speeddata.html')

def getCongestData(request):
    return render(request,'congestdata.html')



#shouye
def getshouye(r):
    import json
    import pymysql
    import pandas as pd 
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8")
    conn = pymysql.connect(host="172.168.16.249",user="keen",password="keen123456",database="keen_its",charset="utf8")
    dataf = pd.read_sql('select * from t_regional_hour_flow',conn)
    contextf1 = int(dataf[dataf[dataf['date']==r].columns[3:]].mean().sum())
    contextf = [r,contextf1]

    datas = pd.read_sql('select * from t_regional_hour_speed',conn)
    contexts1 = round(datas[datas[datas['date']==r].columns[3:]].mean().mean(),2)
    contexts = [r,contexts1]

    datac = pd.read_sql('select * from t_regional_hour_congestion',conn)
    contextc1 = round(datac[datac[datac['date']==r].columns[3:]].mean().mean(),2)
    contextc = [r,contextc1]
 

    return contextf,contexts,contextc

def getshouyes(request):
    import json
    shouyes = getshouye(r)
    return  HttpResponse(json.dumps(shouyes), content_type='application/json')

def getShouyeData(request):
    return render(request,'index.html')




















#load data infile '/var/lib/mysql-files/2019120105xs.csv' into table t_regional_hour_flow fields terminated by ',' LINES TERMINATED BY '\n' #IGNORE 1 LINES;













def getPie(request):
    import json
    import pymysql
    import pandas as pd
    conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8")
    #conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select city,dat from meimei',conn)
    Pie=[]
    for i in range(len(context)):
        a={"name":str(context['city'][i]),"value":str(context['dat'][i])}
        Pie.append(a)
    return HttpResponse(json.dumps(Pie), content_type='application/json')


def getHTML0(request):
    return render(request,'showhtml.html')

def show0(request):
    import json
    import pymysql
    import pandas as pd
    conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8")
    #conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select city,dat from meimei',conn)
    #cot = context.to_json(orient='records')
    cb=[i for i in context['city']]
    xz=[i for i in context['dat'].apply(str)]
    ret=[cb,xz]
    return render(request,'show.html',{'ret':json.dumps(ret)})#有中文是js端var data=JSON.parse("{{ data|escapejs }}");
    #return render(request,'show0.html',{'cb':cb,'xz':xz})  #return render(request,'show0.html',{'ret':ret})

def show01(request):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8") 
    conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select city,dat from meimei',conn)
    #cot = context.to_json(orient='records')
    cb=[i for i in context['city']]
    xz=[i for i in context['dat']]
    ret=[cb,xz]
    return render(request,'show2.html',{'ret':json.dumps(ret)})#有中文是js端var data=JSON.parse("{{ data|escapejs }}");
    #return render(request,'show0.html',{'cb':cb,'xz':xz})  #return render(request,'show0.html',{'ret':ret})



def show00(request):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8")
    conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select cb,xz from meimei1',conn)
    #cot = context.to_json(orient='records')
    cb=[i for i in context['cb']]
    xz=[i for i in context['xz']]
    ret=[cb,xz]
    return render(request,'show0.html',{'ret':ret})
    #return render(request,'show0.html',{'cb':cb,'xz':xz})  #return render(request,'show0.html',{'ret':ret})


def show0api(request):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8")
    conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select * from meimei',conn)
    name=list(context['city'])
    xz=list(context['dat'])
    ret={'name':name,'xz':xz}
    print(ret)
    return JsonResponse(ret)

def show(request):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8") 
    conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select * from meimei',conn) #to_json(orient='records')
    jsondata={
	"key":[i for i in context['city']],
	"value":[i for i in context['dat']]
    }
    #return JsonResponse(jsondata)
    return render(request,'show.html',{'jsondata':jsondata})

def mytest(request):
    #df = pd.read_csv(r'E:\mywebsite\ui\myapp\xx.csv')
 
    import random
 
    # dfx = pd.DataFrame()
    # dfx['a'] = ['2017-08-08','2017-08-09','2017-08-10']
    # dfx['b'] = [random.random(),random.random(),random.random()]
    # dfx['c'] = [random.random(),random.random(),random.random()]
    #
    # dfx['a'] = pd.to_datetime(dfx.a)
    #
    # dfx = dfx.set_index('a')
 
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8")
    conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select * from meimei',conn).to_json(orient='records')
    #df = df.set_index(pd.to_datetime(df.TimeStamp))
    #dfn = pd.DataFrame()
    #dfn['ws'] = df.grWindSpeed.astype(float)
 
    #dfn = dfn.tail(500)
 
    #option = de.eplot(dfn,1)
    #str_option = json.dumps(dfn)
    #context = {"myContext": str_option}
 
    return render(request,'index.html',{'context':context})
    #return HttpResponse(str_option)
 
 
def test_ajax(request):
    import json
    import pymysql
    import pandas as pd
    #conn = pymysql.connect(host="127.0.0.1",user="root",password="mysql",database="django_jk1",charset="utf8")
    conn = pymysql.connect(host="172.168.16.70",user="root",password="root",database="django_jk1",charset="utf8")
    context = pd.read_sql('select * from meimei',conn).to_json(orient='records')
    #df = df.set_index(pd.to_datetime(df.TimeStamp))
    #dfn = pd.DataFrame()
    #dfn['ws'] = df.grWindSpeed.astype(float)
 
    #dfn = dfn.tail(500)
 
    #option = de.eplot(dfn,1)
    #str_option = json.dumps(dfn)
    #context = {"myContext": str_option}
 
 
    #context = {"myContext": {'a':[1,2],'b':[3,4]}}
    return render(request, 'ajax.html', {'context':context})

