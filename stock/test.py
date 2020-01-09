import xlrd
from xlutils.copy import copy
import xlwt



filePath = '/Users/shanwang/Desktop/test.xls'
otherfilePath = '/Users/shanwang/Desktop/test_a.xls'
rb = xlrd.open_workbook(filePath)
wb = copy(rb)
ws = wb.get_sheet(0)
for i in range(2,159):
    ws.write(i,1,'=HYPERLINK(\"/Users/shanwang/Desktop/test_a.xls\")')


wb.save(filePath)