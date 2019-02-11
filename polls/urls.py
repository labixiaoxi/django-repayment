# -*-coding:utf-8 -*-
# __author__ = 'xiaoxi'
# @time:2018/12/21 17:48
from django.conf.urls import url,include
from django.contrib import admin
from polls import views
urlpatterns = [
    url(r'index/',views.index),
    url(r'addrun/',views.add),

]