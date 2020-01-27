# -*- coding: utf-8 -*-
import requests
from stock.mysql_dao import queryBySql , findOneBySql
import numpy as np

dts = "2020-01-23T00:00:00,2020-01-22T00:00:00,2020-01-21T00:00:00,2020-01-20T00:00:00,2020-01-17T00:00:00,2020-01-16T00:00:00,2020-01-15T00:00:00,2020-01-14T00:00:00,2020-01-13T00:00:00,2020-01-10T00:00:00,2020-01-09T00:00:00,2020-01-08T00:00:00,2020-01-07T00:00:00,2020-01-06T00:00:00,2019-12-19T00:00:00,2019-12-18T00:00:00,2019-12-17T00:00:00,2019-12-16T00:00:00"
queryStockSql = "select * from allstock limit 1000"
queryPartitionSql = "select * from all_partition limit 15"
queryDetailsSql = "select * from partition_stock_detail limit 20000"

thread = 0.1
detailsMap = {}
stocks = []
partitions = []
vector = []
results = []
same_result = {}

def cos_dist(vec1,vec2):
    """
    :param vec1: 向量1
    :param vec2: 向量2
    :return: 返回两个向量的余弦相似度
    """
    dist1=float(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
    return dist1


def getAllPartition():
    rows = queryBySql(queryPartitionSql)
    for item in rows:
        partitions.append(item[2])

def getAllStock():
    rows = queryBySql(queryStockSql)
    for item in rows:
        stocks.append(item[2])

def getAllDetails():
    rows = queryBySql(queryDetailsSql)
    for item in rows:
        detailsMap[item[2]+item[3]+item[1]] = item[9]


def get_vector():
    getAllStock()
    getAllPartition()
    getAllDetails()
    for partition in partitions:
        partition_vector = []
        for stock in stocks:
            for dt in dts.split(","):
                key = partition + stock + dt
                value = detailsMap.get(key)
                if value is None:
                    partition_vector.append(0)
                elif value < 0 :
                    partition_vector.append(-1)
                elif value > 0 :
                    partition_vector.append(1)
                else:
                    partition_vector.append(0)

        vector.append(partition_vector)

def process():
    get_vector()
    for index , partition in enumerate(partitions):
        temp_result = {}
        for other_index , other_partition in enumerate(partitions):
            res = cos_dist(vector[index] , vector[other_index])
            if res > thread:
                temp_result[other_partition] = res
        same_result[partition] = temp_result

if __name__ == '__main__':
    process()
    print(same_result)