# -*-coding:utf-8 -*-
# __author__ = 'xiaoxi'
# @time:2018/12/3 13:54
import hashlib
class Md5:
    def md5(self,key):
        result=hashlib.md5()
        result.update(key)
        result_code=result.hexdigest()
        return result_code

# if __name__== '__main__':
#     m=md5()
#     print m.md5('xiaoxi1234')