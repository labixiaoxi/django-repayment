# -*-coding:utf-8 -*-
# __author__ = 'xiaoxi'
# @time:2018/12/3 14:59
import MySQLdb,re
def message(sql):
        '''
        运营平台数据库
        :param sql:
        :return:
        '''
        db=MySQLdb.connect(
           host='hjlcoutside.mysql.rds.aliyuncs.com',
           user='demo_jhj_apps',
           passwd='NjRZWq3UYuww',
           db='demo_jhj_message',
           port=3320,
           charset='utf8'
        )
        cursor = db.cursor()
        #执行sql
        # data=cursor.execute("select * from t_member where Id=532517")
        # sql="select * from t_sms where Mobile='17120000006' order by Id DESC"
        result=cursor.execute(sql)
        '''
        1获取第一条查询结果
        2拿到content信息,也就是通过索引3获取
        3正则拿到验证码
        '''
        result_sql= cursor.fetchone()
        result_message=result_sql[3]
        r=re.compile(r'\d+')
        res1=re.search(r,result_message)
        cursor.close()
        db.close()
        return res1.group(0)