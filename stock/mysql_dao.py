# -*- coding: utf-8 -*-
import pymysql

def queryBySql(sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 执行sql语句
    cursor.execute(sql)
    results = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    return results

def findOneBySql(sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 执行sql语句
    cursor.execute(sql)
    result = cursor.fetchone()
    # 关闭数据库连接
    db.close()
    return result
