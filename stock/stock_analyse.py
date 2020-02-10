# -*- coding: utf-8 -*-
import requests
import json
import xlwt
import pymysql
import time
import datetime

stock_partition_zc_dt_sql='select stock_code,count(partition_code) from partition_stock_detail where hd_date="{dt}T00:00:00"  and stock_code="{code}" and hold_change_one>0 and hold_change_five>hold_change_one and hold_change_ten>hold_change_five'

stock_partition_jc_dt_sql='select stock_code,count(partition_code) from partition_stock_detail where hd_date="{dt}T00:00:00"  and stock_code="{code}" and hold_change_one<0 and hold_change_five<hold_change_one and hold_change_ten<hold_change_five'

hq_zc_sql='select hd_date ,count(partition_code) count_res from partition_stock_detail where hold_change_one>0 and hold_change_five>hold_change_one and hold_change_ten>hold_change_five group by hd_date order by hd_date desc'

hq_jc_sql='select hd_date ,count(partition_code) count_res from partition_stock_detail where hold_change_one<0 and hold_change_five<hold_change_one and hold_change_ten<hold_change_five group by hd_date order by hd_date desc'

xg_zc_sql='select stock_code,name , avg(today_zd),  count(partition_code) count_res from partition_stock_detail join allstock on (partition_stock_detail.stock_code = allstock.code) where hd_date>="{start_dt}T00:00:00" and hd_date<="{end_dt}T00:00:00" and partition_code in ("C00019","C00010","C00100","C00039","B01943","B01590","B01228","B01130","B01345","B01284","B01143","B01668","B01565","C00074","B02145","B01739") and hold_change_one>0 and hold_change_five>hold_change_one and hold_change_ten>hold_change_five group by stock_code  order by 4 desc limit 20;'

xg_jc_sql='select stock_code,name ,avg(today_zd), count(partition_code) count_res from partition_stock_detail join allstock on (partition_stock_detail.stock_code = allstock.code) where hd_date>="{start_dt}T00:00:00" and  hd_date<="{end_dt}T00:00:00" and partition_code in ("C00019","C00010","C00100","C00039","B01943","B01590","B01228","B01130","B01345","B01284","B01143","B01668","B01565","C00074","B02145","B01739") and hold_change_one<0 and hold_change_five<hold_change_one and hold_change_ten<hold_change_five group by stock_code  order by 4 desc limit 20;'

partition_youzi = 'and partition_code in ("C00019","C00010","C00100","C00039","B01943","B01590","B01228","B01130","B01345","B01284","B01143","B01668","B01565","C00074","B02145","B01739") '

def list_analyse(sqlTemp , code , dt):
    resp = []
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = sqlTemp.format(code=code, dt=dt)
    # 执行sql语句
    cursor.execute(sql)
    results = cursor.fetchall()
    for item in results:
        resp.append(item)
    # 关闭数据库连接
    db.close()
    return resp

def xuangu_analyse(sqlTemp , start_dt , end_dt):
    resp = []
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = sqlTemp.format(start_dt=start_dt , end_dt = end_dt)
    # 执行sql语句
    cursor.execute(sql)
    results = cursor.fetchall()
    for item in results:
        resp.append(item)
    # 关闭数据库连接
    db.close()
    return resp

def analyse(sqlTemp, code , dt):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = sqlTemp.format(code=code , dt = dt)
    # 执行sql语句
    cursor.execute(sql)
    result = cursor.fetchone()
    # 关闭数据库连接
    db.close()
    return result


def getDtList(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

def analyse_gg(code , startDate , endDate):
    for dt in getDtList(startDate , endDate):
        zc_res = analyse(stock_partition_zc_dt_sql , code , dt)
        jc_res = analyse(stock_partition_jc_dt_sql , code , dt)
        print(code+"\t"+dt+"\t"+str(zc_res[1])+"\t-"+str(jc_res[1]))

def analyse_hq():
    zc_res = list_analyse(hq_zc_sql , '' , '')
    jc_res = list_analyse(hq_jc_sql , '' , '')
    for i in range(len(zc_res)):
        print(zc_res[i][0]+"\t"+str(zc_res[i][1])+"\t"+str(jc_res[i][1]))

def analyse_xuangu(startDate , endDate):
    zc_res = xuangu_analyse(xg_zc_sql , startDate , endDate)
    jc_res = xuangu_analyse(xg_jc_sql , startDate , endDate)
    for i in range(len(zc_res)):
        print(str(i) + "\t" + zc_res[i][0] + "\t"+ str(zc_res[i][1]) +"\t"+ str(zc_res[i][2]) +"\t"+str(zc_res[i][3]) +"\t"+ jc_res[i][0] +"\t"+ jc_res[i][1]+"\t"+ str(jc_res[i][2]) + "\t-"+ str(jc_res[i][3]) )
    pass
if __name__ == '__main__':
    # gg_analyse(stock_partition_jc_dt_sql , '000651' ,'2020-01-13')、、、
    # analyse_gg("600339","2020-01-01","2020-01-20")
    # print("\n")
    # analyse_gg("600398","2020-01-01","2020-01-20")
    # print("\n")
    # analyse_gg("600489","2020-01-01","2020-01-20")
    # print("\n")
    # analyse_gg("601766", "2020-01-01", "2020-01-20")
    # print("\n")
    # analyse_gg("600598", "2020-01-01", "2020-01-20")
    # print("\n")
    # analyse_gg("002415", "2020-01-01", "2020-01-20")

    analyse_hq()
    analyse_xuangu("2020-01-22","2020-01-23")

    pass

