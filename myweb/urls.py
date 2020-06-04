"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from myapp.views import ajax_flows,ajax_speeds,ajax_congests,getshouyes,getShouyeData,getFlowData,\
getSpeedData,getCongestData,generatereport,downloadreport,generatereport0,generatereport1
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

    

router = DefaultRouter()

#配置goods的url
router.register(r'ajax_flows', ajax_flows, basename="ajax_flows")
router.register(r'ajax_speeds', ajax_speeds, basename="ajax_speeds")
router.register(r'ajax_congests', ajax_congests, basename="ajax_congests")
    

urlpatterns = [
    path('getshouyes/',getshouyes),
    path('getShouyeData/',getShouyeData),
    path('ajax_flows/',ajax_flows),
    path('ajax_speeds/',ajax_speeds),
    path('ajax_congests/',ajax_congests),
    path('getFlowData/',getFlowData),
    path('getSpeedData/',getSpeedData),
    path('getCongestData/',getCongestData),
    path('generatereport1/', generatereport1),
    path('downloadreport/', downloadreport),
#    url(r'^', include(router.urls)),
#    url(r'docs/', include_docs_urls(title="交通流量接口文档")),
]




#报告定时生成
import datetime
import threading
import os
import time

path_name = "E:/GZ/Django/Django_API-1/DJangoDRF/mywebchartdd/"
img_name = path_name+datetime.datetime.now().strftime("%Y-%m-%d")+".png"
report_name = path_name+datetime.datetime.now().strftime("%Y-%m-%d")+".docx"
 
# 获取现在时间
now_time = datetime.datetime.now()
# 获取明天时间
next_time = now_time #+ datetime.timedelta(days=+1)
next_year = next_time.date().year
next_month = next_time.date().month
next_day = next_time.date().day
# 获取明天3点时间
next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 15:15:00", "%Y-%m-%d %H:%M:%S")
# # 获取昨天时间
# last_time = now_time + datetime.timedelta(days=-1)
 
# 获取距离明天3点时间，单位为秒
timer_start_time = (next_time - now_time).total_seconds()
 
 
#定时器,参数为(多少时间后执行，单位为秒，执行的方法)
if os.path.exists(report_name) == False:
    timer = threading.Timer(timer_start_time, generatereport0)
    timer.start()
else:
    time.sleep(timer_start_time)





