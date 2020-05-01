# -*- coding: utf-8 -*-
import requests
import json
import xlwt
import pymysql
import time
import datetime
from stock import utils

from stock.mysql_dao import queryBySql , findOneBySql


query_hold_sql = 'select hold_sum from partition_stock_detail where partition_code="{partition_code}" and  stock_code="{stock_code}" and hd_date<="{dt}T00:00:00" order by hd_date desc'


stock_partition_zc_dt_sql='select stock_code,count(partition_code) , stock_name  from agg_partition_stock_detail where hd_date="{dt}" and stock_code="{code}" and avg_hold_sum_one>avg_hold_sum_three and avg_hold_sum_three>avg_hold_sum_five and avg_hold_sum_five>avg_hold_sum_ten and avg_hold_sum_ten>avg_hold_sum_thirty group by stock_code,stock_name'

stock_partition_jc_dt_sql='select stock_code,count(partition_code) , stock_name  from agg_partition_stock_detail where hd_date="{dt}" and stock_code="{code}" and avg_hold_sum_one<avg_hold_sum_three and avg_hold_sum_three<avg_hold_sum_five group by stock_code,stock_name'

hq_zc_sql='select hd_date ,count(partition_code) count_res from agg_partition_stock_detail where avg_hold_sum_one>avg_hold_sum_three and avg_hold_sum_three>avg_hold_sum_five and avg_hold_sum_five>avg_hold_sum_ten and avg_hold_sum_ten>avg_hold_sum_thirty  group by hd_date order by hd_date desc'

hq_jc_sql='select hd_date ,count(partition_code) count_res from agg_partition_stock_detail where avg_hold_sum_one<avg_hold_sum_three and avg_hold_sum_three<avg_hold_sum_five group by hd_date order by hd_date desc'

xgall_zc_sql='select stock_code,stock_name , 1,  count(partition_code) count_res from agg_partition_stock_detail  where hd_date>="{start_dt}" and hd_date<="{end_dt}" and  avg_hold_sum_one>avg_hold_sum_three and avg_hold_sum_three>avg_hold_sum_five and avg_hold_sum_five>avg_hold_sum_ten and avg_hold_sum_ten>avg_hold_sum_thirty  group by stock_code,stock_name  order by 4 desc limit 70;'

xgall_jc_sql='select stock_code,stock_name ,1, count(partition_code) count_res from agg_partition_stock_detail  where hd_date>="{start_dt}" and  hd_date<="{end_dt}" and  avg_hold_sum_one<avg_hold_sum_three and avg_hold_sum_three<avg_hold_sum_five group by stock_code,stock_name  order by 4 desc limit 70;'

xg_zc_sql='select stock_code,name , avg(today_zd),  count(partition_code) count_res from partition_stock_detail join allstock on (partition_stock_detail.stock_code = allstock.code) where hd_date>="{start_dt}T00:00:00" and hd_date<="{end_dt}T00:00:00" and partition_code in ("C00019","C00010","C00100","C00039","B01943","B01590","B01228","B01130","B01345","B01284","B01143","B01668","B01565","C00074","B02145","B01739") and hold_change_one>0 and hold_change_five>=hold_change_one and hold_change_ten>=hold_change_five group by stock_code  order by 4 desc limit 40;'

xg_jc_sql='select stock_code,name ,avg(today_zd), count(partition_code) count_res from partition_stock_detail join allstock on (partition_stock_detail.stock_code = allstock.code) where hd_date>="{start_dt}T00:00:00" and  hd_date<="{end_dt}T00:00:00" and partition_code in ("C00019","C00010","C00100","C00039","B01943","B01590","B01228","B01130","B01345","B01284","B01143","B01668","B01565","C00074","B02145","B01739") and hold_change_one<0 and hold_change_five<=hold_change_one and hold_change_ten<=hold_change_five group by stock_code  order by 4 desc limit 40;'

partition_youzi = 'and partition_code in ("C00019","C00010","C00100","C00039","B01943","B01590","B01228","B01130","B01345","B01284","B01143","B01668","B01565","C00074","B02145","B01739") '

queryStockSql = "select * from allstock"
queryPartitionSql = "select * from all_partition"
queryDetails = 'select partition_code, stock_code , hold_sum , hd_date from partition_stock_detail where hd_date<="{dt}T00:00:00" order by hd_date desc'


def fillRow(rowList , dt ):
    fillList = []
    for item in utils.getLast60TurnOnDtList(dt):
        fillList.append(containDate(rowList , item))
    return fillList

def containDate(rowList , dt ):
    for item in rowList:
        if item[1] == dt:
            return item[0]
    return 0.0

def getAllPartition():
    partitions = []
    rows = queryBySql(queryPartitionSql)
    for item in rows:
        partitions.append(item[2])
    return partitions

def getAllStock():
    stocks = []
    rows = queryBySql(queryStockSql)
    for item in rows:
        stocks.append((item[1],item[2]))
    return stocks

def getAllDetails(dt):
    detailMaps = {}
    rows = queryBySql(queryDetails.format(dt=dt))
    for item in rows:
        key = item[0] + item[1]
        value = detailMaps.get(key)
        if value is None:
            tempValue = []
            tempValue.append((item[2],item[3][:10]))
            detailMaps[key] = tempValue
        else:
            detailMaps[key].append((item[2],item[3][:10]))
    return detailMaps

def agg_partition_stock_all(dt):
    agg_results = []
    details = getAllDetails(dt)
    i = 0
    for partition in getAllPartition():
        for stock in getAllStock():
            i = i + 1
            print(i)
            row  = details.get(partition + stock[1])
            if row is None or len(row) == 0 :
                continue
            fillRows = fillRow(row , dt)
            print(fillRows)
            print("\n")
            sum_one = 0
            sum_three = 0
            sum_five = 0
            sum_ten = 0
            sum_thirty = 0
            for index , value in enumerate(fillRows):
                if index > 30:
                    break
                if index < 1:
                    sum_one += value
                    sum_three += value
                    sum_five += value
                    sum_ten += value
                    sum_thirty += value
                elif index>=1 and index<3:
                    sum_three += value
                    sum_five += value
                    sum_ten += value
                    sum_thirty += value
                elif index>=3 and index<5:
                    sum_five += value
                    sum_ten += value
                    sum_thirty += value
                elif index>=5 and index<10:
                    sum_ten += value
                    sum_thirty += value
                elif index>=10 and index<30:
                    sum_thirty += value
            agg_results.append((dt , partition , stock[1] , stock[0] , str(sum_one) , str(sum_three/3) , str(sum_five/5) , str(sum_ten/10) , str(sum_thirty/30)))
    saveAggPartitionStock(agg_results)


def saveAggPartitionStock(details):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    for item in details:
        try:
            # SQL 插入语句
            sql = 'INSERT INTO agg_partition_stock_detail(hd_date ,partition_code,stock_code,stock_name,avg_hold_sum_one,avg_hold_sum_three,avg_hold_sum_five,avg_hold_sum_ten,avg_hold_sum_thirty) ' \
                  'VALUES ("'+ item[0] + '","' +item[1] + '","' +item[2] + '","' +item[3] + '","' +item[4] + '","' +item[5] + '","' +item[6] + '","' +item[7] + '","' +item[8] + '")'

            # 执行sql语句
            cursor.execute(sql)
        except Exception as e:
            print(e)
            # traceback.print_exc()
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()


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
        if zc_res is None and jc_res is None:
            continue
        if zc_res is None :
            zc_res = (0,0)
        if jc_res is None:
            jc_res = (0,0,'')
        print(code+"\t"+dt+"\t"+str(zc_res[1])+"\t-"+str(jc_res[1])+"\t"+str(jc_res[2]))
    print("\n")
def analyse_gg_list(code_list , startDate , endDate):
    for code in code_list:
        analyse_gg(code , startDate , endDate)
        print("\n")

def analyse_hq():
    zc_res = list_analyse(hq_zc_sql , '' , '')
    jc_res = list_analyse(hq_jc_sql , '' , '')
    for i in range(len(zc_res)):
        print(zc_res[i][0]+"\t"+str(zc_res[i][1])+"\t"+str(jc_res[i][1]))

def analyse_xuanguall(startDate , endDate):
    zc_res = xuangu_analyse(xgall_zc_sql , startDate , endDate)
    jc_res = xuangu_analyse(xgall_jc_sql , startDate , endDate)
    for i in range(len(zc_res)):
        print(str(i) + "\t" + zc_res[i][0] + "\t"+ str(zc_res[i][1]) +"\t"+ str(zc_res[i][2]) +"\t"+str(zc_res[i][3]) +"\t"+ jc_res[i][0] +"\t"+ jc_res[i][1]+"\t"+ str(jc_res[i][2]) + "\t-"+ str(jc_res[i][3]) )
    pass

def analyse_gg_xuangu_all(startDate , endDate , an_startDate , an_endDate):
    zc_res = xuangu_analyse(xgall_zc_sql , startDate , endDate)
    jc_res = xuangu_analyse(xgall_jc_sql , startDate , endDate)
    zc_gg = []
    jc_gg = []

    for i in range(len(zc_res)):
        print(str(i) + "\t" + zc_res[i][0] + "\t"+ str(zc_res[i][1]) +"\t"+ str(zc_res[i][2]) +"\t"+str(zc_res[i][3]) +"\t"+ jc_res[i][0] +"\t"+ jc_res[i][1]+"\t"+ str(jc_res[i][2]) + "\t-"+ str(jc_res[i][3]) )
        zc_gg.append(zc_res[i][0])
        jc_gg.append(jc_res[i][0])
    print("增持")
    for item in zc_gg:
        analyse_gg(item , an_startDate , an_endDate)
    print("减持")
    for item in jc_gg:
        analyse_gg(item , an_startDate , an_endDate)
    pass


def analyse_xuangu(startDate , endDate):
    zc_res = xuangu_analyse(xg_zc_sql , startDate , endDate)
    jc_res = xuangu_analyse(xg_jc_sql , startDate , endDate)
    for i in range(len(zc_res)):
        print(str(i) + "\t" + zc_res[i][0] + "\t"+ str(zc_res[i][1]) +"\t"+ str(zc_res[i][2]) +"\t"+str(zc_res[i][3]) +"\t"+ jc_res[i][0] +"\t"+ jc_res[i][1]+"\t"+ str(jc_res[i][2]) + "\t-"+ str(jc_res[i][3]) )
    pass

def analyse_me(an_start , an_end , start_date , end_date):
    # has buy
    analyse_gg_list(["600489","601766","600398","600111"],"2019-12-31", end_date)

    # last study
    analyse_gg_list(["002506", "601162","000959","000869"], "2019-12-31", end_date)

    # bo li
    analyse_gg_list(["000725", "000100"], "2019-12-31", end_date)

    # teach
    analyse_gg_list(["600446", "300085", "601519","002797","603000","600476","600624"], "2019-12-31", end_date)

    analyse_gg_list([""],"2019-12-31", end_date)
    analyse_hq()
    analyse_gg_xuangu_all(an_start, an_end , start_date, end_date)


if __name__ == '__main__':
    analyse_me("2020-04-20","2020-04-24" , "2019-12-31" , "2020-04-24" )

    # agg_partition_stock_all("2020-03-16")
    # for item in ["02","03","06","07","08","09","10","13","14","15","16","17","20","21","22","23"]:
    # agg_partition_stock_all("2020-03-06")
    # for item in ["04","05","06","07","10","11","12","13","14","17","18","19","20","21","24","25","26","27","28"]:
    #     agg_partition_stock_all("2020-02-"+ item)
    # for item in ["20","21","22","23","24"]:
    #     agg_partition_stock_all("2020-04-"+ item)