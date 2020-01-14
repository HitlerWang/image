
# -*- coding: utf-8 -*-
import requests
import json
import xlwt
import pymysql
import time
import datetime

stock_partition_zc_sql='select stock_code,count(partition_code) from partition_stock_detail where hd_date="{dt}T00:00:00"  and stock_code="{code}" and hold_change_one>0 and hold_change_five>hold_change_one and hold_change_ten>hold_change_five group by stock_code order by 2 desc limit 20;'

stock_partition_zc_dt_sql='select stock_code,count(partition_code) from partition_stock_detail where hd_date="{dt}T00:00:00"  and stock_code="{code}" and hold_change_one>0 and hold_change_five>hold_change_one and hold_change_ten>hold_change_five group by stock_code order by 2 desc limit 20;'

stock_partition_jc_sql='select stock_code,count(partition_code) from partition_stock_detail where hd_date="{dt}T00:00:00"  and stock_code="{code}" and hold_change_one<0 and hold_change_five<hold_change_one and hold_change_ten>hold_change_five group by stock_code order by 2 desc limit 20;'

hq_zc_sql='select stock_code,count(partition_code) count_res from partition_stock_detail where hd_date>"2020-01-01T00:00:00" and hd_date<"2020-01-04T00:00:00"and hold_change_one>0 and hold_change_five>hold_change_one and hold_change_ten>hold_change_five group by stock_code  order by 2 desc limit 20;'

def gg_analyse(sqlTemp, code , startDt , endDt):
    resp = []
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    for dt in getDtList(startDt , endDt):
        sql = sqlTemp.format(code=code , dt = dt)
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            resp.append(row[2])
    # 关闭数据库连接
    db.close()
    return resp

def getDtList(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

if __name__ == '__main__':
    pass
