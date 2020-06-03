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
from myapp.views import ajax_flows,ajax_speeds,ajax_congests,getshouyes,getShouyeData,getFlowData,getSpeedData,getCongestData,generatereport,downloadreport
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
    path('generatereport/', generatereport),
    path('downloadreport/', downloadreport),
#    url(r'^', include(router.urls)),
#    url(r'docs/', include_docs_urls(title="交通流量接口文档")),
]





