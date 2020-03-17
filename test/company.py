

import datetime





def getDtList(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
    return dates

def printDropTable(tabeName , beginDate, endDate):
    for item in getDtList(beginDate, endDate):
        print('drop table '+ tabeName +'_' +  item+ ';')

if __name__ == '__main__':
    print('use shopee_datagroup_mydata_db;')
    printDropTable('marketing_discount_overview_pastdays_tab' , '20191101','20200201')
    printDropTable('marketing_discount_key_metrics_pastdays_tab' , '20191101','20200201')
    printDropTable('follow_prize_key_metrics_pastdays_tab' , '20190801','20200201')
    printDropTable('marketing_voucher_key_metrics_pastdays_tab' , '20190801','20200201')
    printDropTable('marketing_voucher_performance_pastdays_tab' , '20190801','20200201')
    printDropTable('shocking_sale_key_metrics_pastdays_tab' , '20200117','20200201')
