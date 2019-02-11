# -*-coding:utf-8 -*-
# __author__ = 'xiaoxi'
# @time:2018/11/27 14:27
from django.conf.urls import url
from django.contrib import admin
from jhj_rePayMents import views
urlpatterns = [
    url('repayments.html/', views.normal_repayment,name='login'),
    # url('result1/',views.repayments_xw),
    # url('pc/',views.pc_send),
    url('result/',views.repayments),
    url('test/',views.test)
]









