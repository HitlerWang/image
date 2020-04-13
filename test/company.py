

import datetime

keyMetric = '''` (
  `id` bigint NOT NULL DEFAULT '0',
  `shopid` int NOT NULL DEFAULT '0',
  `dt` int NOT NULL DEFAULT '0',
  `period` int NOT NULL DEFAULT '0',
  `live_streaming_cnt` int NOT NULL DEFAULT '0',
  `viewers` int NOT NULL DEFAULT '0',
  `peak_viewers` int NOT NULL DEFAULT '0.0',
  `avg_views_duration` double NOT NULL DEFAULT '0.0',
  `orders` int NOT NULL DEFAULT '0',
  `sales` double NOT NULL DEFAULT '0.0',
  `live_streaming_list` text ,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_idx` (`shopid`, `dt`, `period`),
  KEY `dt_idx` (`dt`)
) ENGINE = InnoDB CHARSET = utf8mb4;
'''

overview = '''` (
  `id` bigint NOT NULL DEFAULT '0',
  `shopid` int NOT NULL DEFAULT '0',
  `dt` int NOT NULL DEFAULT '0',
  `period` int NOT NULL DEFAULT '0',
  `streaming_id` bigint NOT NULL DEFAULT '0',
  `viewers` int NOT NULL DEFAULT '0',
  `peak_viewers` int NOT NULL DEFAULT '0',
  `avg_views_duration` double NOT NULL DEFAULT '0.0',
  `sales` double NOT NULL DEFAULT '0.0',
  `orders` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_idx` (`shopid`, `dt`,`period`,`streaming_id`),
  KEY `dt_idx` (`dt`)
) ENGINE = InnoDB CHARSET = utf8mb4;

'''



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

def dropTable():
    print('use shopee_datagroup_mydata_db;')
    printDropTable('marketing_discount_overview_pastdays_tab' , '20191101','20200201')
    printDropTable('marketing_discount_key_metrics_pastdays_tab' , '20191101','20200201')
    printDropTable('follow_prize_key_metrics_pastdays_tab' , '20190801','20200201')
    printDropTable('marketing_voucher_key_metrics_pastdays_tab' , '20190801','20200201')
    printDropTable('marketing_voucher_performance_pastdays_tab' , '20190801','20200201')
    printDropTable('shocking_sale_key_metrics_pastdays_tab' , '20200117','20200201')

def printCreateTable(tablePre , tableEnd, beginDate , endDate):
    with open("/Users/shanwang/Desktop/live-streaming.sql" , "a") as f:
        for item in getDtList(beginDate, endDate):
            f.write(tablePre + item+ tableEnd + "\n")
            print(tablePre + item+ tableEnd)

def createTable():
    printCreateTable("CREATE TABLE IF NOT EXISTS `live_streaming_key_metrics_pastdays_tab_" , keyMetric , "20200401","20230401")
    printCreateTable("CREATE TABLE IF NOT EXISTS `live_streaming_overview_pastdays_tab_" , overview , "20200401","20230401")


if __name__ == '__main__':
    createTable()