
# -*- coding=utf-8 -*-
import xlrd
from xlutils.copy import copy
import xlwt
from lxml import etree
import requests

import datetime


def testxpath():
    res=requests.get('http://www.w3school.com.cn/')
    tree=etree.HTML(res.content)
    div=tree.xpath('//div[@id="d1"]')[0]
    div_str=etree.tostring(div,encoding='utf-8')
    print(div_str)

def getDtList(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def testexcel():
    filePath = '/Users/shanwang/Desktop/test.xls'
    otherfilePath = '/Users/shanwang/Desktop/test_a.xls'
    rb = xlrd.open_workbook(filePath)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    for i in range(2,159):
        ws.write(i,1,'=HYPERLINK(\"/Users/shanwang/Desktop/test_a.xls\")')
    wb.save(filePath)

if __name__ == '__main__':
    for date in getDtList('2018-02-01', '2018-02-10'):
        print(date)