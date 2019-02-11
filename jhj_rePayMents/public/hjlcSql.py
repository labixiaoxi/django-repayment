# -*-coding:utf-8 -*-
# __author__ = 'xiaoxi'
# @time:2018/12/3 14:41
import MySQLdb,re


def intelligence(sql):
    '''
    hjlc数据库
    :param sql:
    :return:
    '''
    db=MySQLdb.connect(
       host='hjlcoutside.mysql.rds.aliyuncs.com',
       user='hjlc_test',
       passwd='3j42CBHjs5',
       db='intelligence',
       port=3320,
       charset='utf8'
    )
    cursor = db.cursor()
    cursor.execute(sql)
    result_sql= cursor.fetchone()
    return result_sql

def intelligenceUpdateDate(sql):

    db=MySQLdb.connect(
       host='hjlcoutside.mysql.rds.aliyuncs.com',
       user='hjlc_test',
       passwd='3j42CBHjs5',
       db='intelligence',
       port=3320,
       charset='utf8'
    )
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    #关闭
    db.close()

