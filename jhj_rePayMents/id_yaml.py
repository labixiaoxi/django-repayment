# -*-coding:utf-8 -*-
# __author__ = 'xiaoxi'
# @time:2018/12/3 10:37
import yaml
def idYaml():
    with open('config/id.yaml','r') as f:
        result=f.read()
        userId=yaml.load(result)
        print userId
        return userId

idYaml()
