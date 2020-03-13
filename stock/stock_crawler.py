# -*- coding: utf-8 -*-
import requests
import json
import xlwt
import pymysql
import time
import datetime
import traceback
import random
from lxml import etree
from stock import mysql_dao

err_url_path = '/Users/shanwang/Desktop/err_url.text'

f = open(err_url_path, "a+")

testCountSql = 'select count(1) from partition_stock_detail where hd_date="{dt}T00:00:00"  and  partition_code="{partition_code}" '

testQualitySql = 'select * from partition_stock_detail where hd_date="{dt}T00:00:00"  and  partition_code="{partition_code}" and  stock_code="{stock_code}" '

stock_list_url = 'http://quote.eastmoney.com/stock_list.html'

rzrq_detail_url = 'http://api.dataide.eastmoney.com/data/get_rzrq_ggmx?code=002415&orderby=date&order=desc&pageindex=3&pagesize=50&jsonp_callback=var%20DLgtJLPl=(x)&rt=52794205'
rzrq_detail_nameMapping = {
    "spj":"收盘价",
    "scode":"股票代码",
    "date":"交易日期",
    "zdf":"今日涨跌幅",
    "rzye":"融资余额",
    "rzyezb":"融资余额占流通股市值比",
    "rzmre":"融资买入额",
    "rzche":"融资偿还额",
    "rzjme":"融资净买入",
    "rqye":"融券余额",
    "rqyl":"融券余量",
    "rqmcl":"融券卖出量",
    "rqchl":"融券偿还量",
    "rqjmg":"融券净卖出",
    "rzrqye":"融资融券余额",
    "rzrqyecz":"融资融券余额差值",
    "rzmre3d":"融资买入额3d",
    "rzche3d":"融资偿还额3d",
    "rzjme3d":"融资净买入3d",
    "rqmcl3d":"融券卖出量3d",
    "rqchl3d":"融券偿还量3d",
    "rqjmg3d":"融券净卖出3d",
    "rzmre5d":"融资买入额5d",
    "rzche5d":"融资偿还额5d",
    "rzjme5d":"融资净买入5d",
    "rqmcl5d":"融券卖出量5d",
    "rqchl5d":"融券偿还量5d",
    "rqjmg5d":"融券净卖出5d",
    "rzmre10d":"融资买入额10d",
    "rzche10d":"融资偿还额10d",
    "rzjme10d":"融资净买入10d",
    "rqmcl10d":"融券卖出量10d",
    "rqchl10d":"融券偿还量10d",
    "rqjmg10d":"融券净卖出10d",
}


stock_detail_url = 'http://75.push2.eastmoney.com/api/qt/stock/get?fltt=2&invt=2&secid=1.600339&fields=f78,f58,f86,f43,f169,f170,f44,f45,f46,f47,f116,f117,f162,f167,f60&ut=b2884a393a59ad64002292a3e90d46a5&cb=jQuery18305844286905750697_1579587845624&_=1579587847181'


hsgt_jg_list_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=HSGTCOMSTA&token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDCOUNT&sr=3&p=1&ps=500&js=var%20lMCByFSy={pages:(tp),data:(x)}&filter=(MARKET=%27N%27)(HDDATE=^2020-01-09^)&rt=52628114'

hsgt_jg_dt_detail_list_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&sr=3&p=2&ps=50&js=var%20hjqVpcJG={pages:(tp),data:(x)}&filter=(PARTICIPANTCODE=%27B01110%27)(MARKET%20in%20(%27001%27,%27003%27))(HDDATE=^2020-01-10^)&type=HSGTNHDDET&rt=52629792'
jg_dt_detail_nameMapping = {
    "SCode":"股票代码",
    "CLOSEPRICE":"今日收盘价",
    "Zdf":"今日涨跌幅",
    "SHAREHOLDSUM":"持股数量",
    "SHAREHOLDPRICE":"持股市值",
    "Zb":"持股数量占比",
    "PARTICIPANTCODE":"机构代码",
    "HDDATE":"持股日期",
    "SHAREHOLDPRICEONE":"持股市值变化1",
    "SHAREHOLDPRICEFIVE":"持股市值变化5",
    "SHAREHOLDPRICETEN":"持股市值变化10",
}

bshy_url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGT20_HYTJ_SUM&token=894050c76af8597a853f5b408b759f5d&st=ShareSZ_ZC&sr=-1&p=1&ps=500&js=var%20GKTnTrxX={pages:(tp),data:(x)}&filter=(DateType=%271%27)&rt=52618843'

nameMapping = {
    "HYName":"名称",
    "Zdf" : "最新涨跌幅",
    "Count":"北上资金今日持股-股票只数",
    "ShareSZ_GZ":"北上资金今日持股-市值",
    "ShareHold_Chg_BK":"北上资金今日持股-占板块比",
    "ShareHold_Chg_GZ":"北上资金今日持股-占资金比",
    "ZC_Count":"北上资金今日增持-股票只数",
    "ShareSZ_ZC":"北上资金今日增持-市值",
    "ShareHold_ZC_Chg_BK":"北上资金今日增持-占板块比",
    "ShareHold_ZC_Chg_GZ":"北上资金今日增持-占资金比",
    "Max_SZ_Name":"最大今日增持-市值",
    "Max_ZB_Name":"最大今日增持-占股本比",
    "Min_SZ_Name":"最大今日减持-市值",
    "Min_ZB_Name":"最大今日减持-占股本比",
}

pecentStr = ['Zdf' , 'ShareHold_Chg_BK' , 'ShareHold_Chg_GZ' , 'ShareHold_ZC_Chg_BK' , 'ShareHold_ZC_Chg_GZ']

bshy_detail_url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGT20_GGTJ_SUM_BK&token=894050c76af8597a853f5b408b759f5d&st=ShareSZ_Chg_One&sr=-1&p=2&ps=50&js=var%20jWQXnVLQ={pages:(tp),data:(x)}&filter=(ORIGINALCODE=%27459%27%20and%20DateType=%271%27%20and%20HdDate=%272020-01-08%27)&rt=52618980'
detail_nameMapping = {
    "SCode":"股票代码",
    "SName":"股票名称",
    "NewPrice":"今日收盘价",
    "Zdf":"今日涨跌幅",
    "ShareHold":"cg股数",
    "ShareSZ":"cg市值",
    "SharesRate":"cg占流通股比",
    "ZZB":"cg占总股比",
    "ShareHold_Chg_One":"zc股数",
    "ShareSZ_Chg_One":"zc市值",
    "ShareSZ_Chg_Rate_One":"zc市值增幅",
    "LTZB_One":"zc占流通股比",
    "ZZB_One":"zc占总股本比",
    "HYName":"所属板块",
}

bsgg_url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGT20_GGTJ_SUM&token=894050c76af8597a853f5b408b759f5d&st=ShareSZ_Chg_One&sr=-1&p=2&ps=50&js=var%20gQhqBLfH={pages:(tp),data:(x)}&filter=(DateType=%271%27%20and%20HdDate=%272020-01-09%27)&rt=52621103'
bsgg_nameMapping = {
    "SCode":"股票代码",
    "SName":"股票名称",
    "NewPrice":"今日收盘价",
    "Zdf":"今日涨跌幅",
    "ShareHold":"cg股数",
    "ShareSZ":"cg市值",
    "SharesRate":"cg占流通股比",
    "ZZB":"cg占总股比",
    "ShareHold_Chg_One":"zc股数",
    "ShareSZ_Chg_One":"zc市值",
    "ShareSZ_Chg_Rate_One":"zc市值增幅",
    "LTZB_One":"zc占流通股比",
    "ZZB_One":"zc占总股本比",
    "HYName":"所属板块",
}


testStr = '''
[{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00019","PARTICIPANTNAME":"香港上海汇丰银行有限公司","SHAREHOLDSUM":298895851.0,"SHARESRATE":4.96,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":20121668689.32,"SHAREHOLDPRICEONE":452749999.31999969,"SHAREHOLDPRICEFIVE":749177657.81999969,"SHAREHOLDPRICETEN":1301202219.3199997,"MARKET":"003","ShareHoldSumChg":339101.0,"Zb":0.050066984717841448,"Zzb":0.049685708530128166},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01224","PARTICIPANTNAME":"MLFE LTD","SHAREHOLDSUM":145919421.0,"SHARESRATE":2.42,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":9823295421.72,"SHAREHOLDPRICEONE":265466130.84000015,"SHAREHOLDPRICEFIVE":211674666.77999878,"SHAREHOLDPRICETEN":357177656.71999931,"MARKET":"003","ShareHoldSumChg":840045.0,"Zb":0.024442445075101668,"Zzb":0.024256307996363129},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00100","PARTICIPANTNAME":"JPMORGAN CHASE BANK, NATIONAL ASSOCIATION","SHAREHOLDSUM":137568307.0,"SHARESRATE":2.28,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":9261098427.24,"SHAREHOLDPRICEONE":352277326.07999992,"SHAREHOLDPRICEFIVE":611232505.73999977,"SHAREHOLDPRICETEN":826566802.23999977,"MARKET":"003","ShareHoldSumChg":2340300.0,"Zb":0.023043579565205544,"Zzb":0.022868095297131408},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00039","PARTICIPANTNAME":"渣打银行(香港)有限公司","SHAREHOLDSUM":101107485.0,"SHARESRATE":1.68,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":6806555890.1999989,"SHAREHOLDPRICEONE":355471131.95999908,"SHAREHOLDPRICEFIVE":537759427.499999,"SHAREHOLDPRICETEN":631571165.19999886,"MARKET":"003","ShareHoldSumChg":3185737.0,"Zb":0.016936156488684025,"Zzb":0.01680718221118534},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01161","PARTICIPANTNAME":"UBS SECURITIES HONG KONG LTD","SHAREHOLDSUM":66479717.0,"SHARESRATE":1.1,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":4475414548.44,"SHAREHOLDPRICEONE":197494837.92000008,"SHAREHOLDPRICEFIVE":144985426.25999928,"SHAREHOLDPRICETEN":312813573.43999958,"MARKET":"003","ShareHoldSumChg":1544688.0,"Zb":0.01113578179138199,"Zzb":0.011050979232319307},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00010","PARTICIPANTNAME":"花旗银行","SHAREHOLDSUM":55028749.0,"SHARESRATE":0.91,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":3704535382.68,"SHAREHOLDPRICEONE":247582388.51999998,"SHAREHOLDPRICEFIVE":341059423.79999971,"SHAREHOLDPRICETEN":634302567.67999983,"MARKET":"003","ShareHoldSumChg":2555267.0,"Zb":0.0092176707237897823,"Zzb":0.0091474751972772661},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01274","PARTICIPANTNAME":"MORGAN STANLEY HONG KONG SECURITIES LTD","SHAREHOLDSUM":35088549.0,"SHARESRATE":0.58,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":2362161118.68,"SHAREHOLDPRICEONE":71114747.039999962,"SHAREHOLDPRICEFIVE":282334635.89999986,"SHAREHOLDPRICETEN":302771513.67999983,"MARKET":"003","ShareHoldSumChg":312496.0,"Zb":0.0058775584896099175,"Zzb":0.0058327989917769715},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01110","PARTICIPANTNAME":"J.P. MORGAN BROKING (HONG KONG) LTD","SHAREHOLDSUM":21619660.0,"SHARESRATE":0.35,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":1455435511.1999998,"SHAREHOLDPRICEONE":144951078.24,"SHAREHOLDPRICEFIVE":94368320.4599998,"SHAREHOLDPRICETEN":130271216.19999981,"MARKET":"003","ShareHoldSumChg":1727668.0,"Zb":0.0036214326267945685,"Zzb":0.0035938542528663954},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01654","PARTICIPANTNAME":"中国国际金融香港证券有限公司","SHAREHOLDSUM":14432720.0,"SHARESRATE":0.23,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":971610710.39999986,"SHAREHOLDPRICEONE":42198135.4799999,"SHAREHOLDPRICEFIVE":19109018.219999909,"SHAREHOLDPRICETEN":100363515.39999986,"MARKET":"003","ShareHoldSumChg":325061.0,"Zb":0.0024175737778203035,"Zzb":0.0023991631761290364},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00093","PARTICIPANTNAME":"BNP PARIBAS SECURITIES SERVICES","SHAREHOLDSUM":7819444.0,"SHARESRATE":0.12,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":526404970.07999992,"SHAREHOLDPRICEONE":20232855.359999955,"SHAREHOLDPRICEFIVE":44225134.559999943,"SHAREHOLDPRICETEN":126599265.07999992,"MARKET":"003","ShareHoldSumChg":136200.0,"Zb":0.0013098073524279766,"Zzb":0.0012998327482694279},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01121","PARTICIPANTNAME":"法国兴业证券(香港)有限公司","SHAREHOLDSUM":4717231.0,"SHARESRATE":0.07,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":317563990.91999996,"SHAREHOLDPRICEONE":33138554.039999962,"SHAREHOLDPRICEFIVE":36692523.779999971,"SHAREHOLDPRICETEN":68761475.919999957,"MARKET":"003","ShareHoldSumChg":399905.0,"Zb":0.00079016664700216237,"Zzb":0.00078414927390639815},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01451","PARTICIPANTNAME":"高盛(亚洲)证券有限公司","SHAREHOLDSUM":4706082.0,"SHARESRATE":0.07,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":316813440.23999995,"SHAREHOLDPRICEONE":8852834.51999998,"SHAREHOLDPRICEFIVE":11756987.219999969,"SHAREHOLDPRICETEN":23977455.23999995,"MARKET":"003","ShareHoldSumChg":31513.0,"Zb":0.00078829911752407934,"Zzb":0.00078229596626579656},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01590","PARTICIPANTNAME":"盈透证券香港有限公司","SHAREHOLDSUM":4630308.0,"SHARESRATE":0.07,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":311712334.55999994,"SHAREHOLDPRICEONE":4137851.5199999809,"SHAREHOLDPRICEFIVE":5630275.9199999571,"SHAREHOLDPRICETEN":9656359.5599999428,"MARKET":"003","ShareHoldSumChg":-38400.0,"Zb":0.00077560648332619035,"Zzb":0.00076969999055865321},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01130","PARTICIPANTNAME":"中银国际证券有限公司","SHAREHOLDSUM":4287076.0,"SHARESRATE":0.07,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":288605956.32,"SHAREHOLDPRICEONE":6173389.4399999976,"SHAREHOLDPRICEFIVE":8390748.24000001,"SHAREHOLDPRICETEN":10947016.319999993,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":0.00071811290741611818,"Zzb":0.00071264424671625074},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01491","PARTICIPANTNAME":"CREDIT SUISSE SECURITIES (HONG KONG) LTD","SHAREHOLDSUM":2496009.0,"SHARESRATE":0.04,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":168031325.88,"SHAREHOLDPRICEONE":75612621.960000008,"SHAREHOLDPRICEFIVE":86494662.6,"SHAREHOLDPRICETEN":146476675.88,"MARKET":"003","ShareHoldSumChg":1093175.0,"Zb":0.00041809762176523059,"Zzb":0.00041491367393579735},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01138","PARTICIPANTNAME":"中信里昂证券有限公司","SHAREHOLDSUM":2392359.0,"SHARESRATE":0.03,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":161053607.88,"SHAREHOLDPRICEONE":2970660.9600000083,"SHAREHOLDPRICEFIVE":4162704.6599999964,"SHAREHOLDPRICETEN":4549272.8799999952,"MARKET":"003","ShareHoldSumChg":-7200.0,"Zb":0.000400735577599538,"Zzb":0.00039768384731920847},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00074","PARTICIPANTNAME":"德意志银行","SHAREHOLDSUM":1453039.0,"SHARESRATE":0.02,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":97818585.479999989,"SHAREHOLDPRICEONE":5781656.1599999964,"SHAREHOLDPRICEFIVE":82581531.539999992,"SHAREHOLDPRICETEN":82716290.479999989,"MARKET":"003","ShareHoldSumChg":56000.0,"Zb":0.00024339341333790417,"Zzb":0.00024153989423195067},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01323","PARTICIPANTNAME":"德意志证券亚洲有限公司","SHAREHOLDSUM":1388766.0,"SHARESRATE":0.02,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":93491727.11999999,"SHAREHOLDPRICEONE":2111819.0399999917,"SHAREHOLDPRICEFIVE":619560.83999998868,"SHAREHOLDPRICETEN":-3559772.88000001,"MARKET":"003","ShareHoldSumChg":1700.0,"Zb":0.00023262727089061466,"Zzb":0.00023085573942126068},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01565","PARTICIPANTNAME":"国泰君安证券(香港)有限公司","SHAREHOLDSUM":1117900.0,"SHARESRATE":0.01,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":75257027.999999985,"SHAREHOLDPRICEONE":1609775.9999999851,"SHAREHOLDPRICEFIVE":1400831.9999999851,"SHAREHOLDPRICETEN":2476527.9999999851,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":0.00018725546717634079,"Zzb":0.00018582945658161799},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01686","PARTICIPANTNAME":"第一上海证券有限公司","SHAREHOLDSUM":1012200.0,"SHARESRATE":0.01,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":68141304.0,"SHAREHOLDPRICEONE":1457568.0000000075,"SHAREHOLDPRICEFIVE":1761228.0,"SHAREHOLDPRICETEN":2348304.0,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":0.00016955003477582269,"Zzb":0.0001682588567420286},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01943","PARTICIPANTNAME":"宝生证券及期货有限公司","SHAREHOLDSUM":988000.0,"SHARESRATE":0.01,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":66512159.999999993,"SHAREHOLDPRICEONE":1192140.0,"SHAREHOLDPRICEFIVE":1424009.9999999925,"SHAREHOLDPRICETEN":2025659.9999999925,"MARKET":"003","ShareHoldSumChg":-3500.0,"Zb":0.00016549637854032089,"Zzb":0.00016423607040221718},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01284","PARTICIPANTNAME":"恒生证券有限公司","SHAREHOLDSUM":912300.0,"SHARESRATE":0.01,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":61416035.999999993,"SHAREHOLDPRICEONE":1313712.0,"SHAREHOLDPRICEFIVE":1174247.9999999925,"SHAREHOLDPRICETEN":34317535.999999993,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":0.00015281613982017688,"Zzb":0.00015165239577726998},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01143","PARTICIPANTNAME":"海通国际证券有限公司","SHAREHOLDSUM":843295.0,"SHARESRATE":0.01,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":56770619.399999991,"SHAREHOLDPRICEONE":1115524.799999997,"SHAREHOLDPRICEFIVE":6398949.29999999,"SHAREHOLDPRICETEN":5596444.3999999911,"MARKET":"003","ShareHoldSumChg":-1500.0,"Zb":0.00014125735682303633,"Zzb":0.00014018163662939042},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00040","PARTICIPANTNAME":"中国工商银行(亚洲)有限公司","SHAREHOLDSUM":748160.0,"SHARESRATE":0.01,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":50366131.199999996,"SHAREHOLDPRICEONE":1077350.3999999985,"SHAREHOLDPRICEFIVE":3079016.3999999985,"SHAREHOLDPRICETEN":-8358768.8000000045,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":0.00012532163013028995,"Zzb":0.0001243672656195575},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01858","PARTICIPANTNAME":"元大证券(香港)有限公司","SHAREHOLDSUM":624000.0,"SHARESRATE":0.01,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":42007679.999999993,"SHAREHOLDPRICEONE":898559.99999999255,"SHAREHOLDPRICEFIVE":2069459.9999999925,"SHAREHOLDPRICETEN":3462679.9999999925,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":0.0001045240285517816,"Zzb":0.00010372804446455822},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01825","PARTICIPANTNAME":"国元证券经纪(香港)有限公司","SHAREHOLDSUM":568600.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":38278151.999999993,"SHAREHOLDPRICEONE":818783.99999999255,"SHAREHOLDPRICEFIVE":989363.99999999255,"SHAREHOLDPRICETEN":1286651.9999999925,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":9.5244170888690742E-05,"Zzb":9.4518855901518908E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00033","PARTICIPANTNAME":"中国银行(香港)有限公司","SHAREHOLDSUM":524999.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":35342932.68,"SHAREHOLDPRICEONE":755998.56000000238,"SHAREHOLDPRICEFIVE":23667856.439999998,"SHAREHOLDPRICETEN":23771112.68,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":8.7940721900091031E-05,"Zzb":8.7271025025398419E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01115","PARTICIPANTNAME":"申万宏源证券(香港)有限公司","SHAREHOLDSUM":416200.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":28018583.999999996,"SHAREHOLDPRICEONE":698148.0,"SHAREHOLDPRICEFIVE":822557.99999999627,"SHAREHOLDPRICETEN":1063083.9999999963,"MARKET":"003","ShareHoldSumChg":1500.0,"Zb":6.9716186992390235E-05,"Zzb":6.9185275811136431E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00102","PARTICIPANTNAME":"MACQUARIE BANK LTD","SHAREHOLDSUM":333100.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":22424291.999999996,"SHAREHOLDPRICEONE":479663.99999999627,"SHAREHOLDPRICEFIVE":579593.99999999627,"SHAREHOLDPRICETEN":772791.99999999627,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":5.5796400497753931E-05,"Zzb":5.5371492966577473E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00088","PARTICIPANTNAME":"招商银行股份有限公司","SHAREHOLDSUM":293886.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":19784405.52,"SHAREHOLDPRICEONE":423195.83999999985,"SHAREHOLDPRICEFIVE":511361.6400000006,"SHAREHOLDPRICETEN":681815.51999999955,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":4.922780233168092E-05,"Zzb":4.8852916787678142E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01826","PARTICIPANTNAME":"广发证券(香港)经纪有限公司","SHAREHOLDSUM":258401.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":17395555.319999997,"SHAREHOLDPRICEONE":372097.43999999762,"SHAREHOLDPRICEFIVE":9447193.7399999965,"SHAREHOLDPRICETEN":9517490.3199999966,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":4.3283835740078391E-05,"Zzb":4.2954215412958829E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01345","PARTICIPANTNAME":"辉立证券(香港)有限公司","SHAREHOLDSUM":226700.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":15261443.999999998,"SHAREHOLDPRICEONE":333036.0,"SHAREHOLDPRICEFIVE":1469969.9999999981,"SHAREHOLDPRICETEN":1598443.9999999981,"MARKET":"003","ShareHoldSumChg":100.0,"Zb":3.7973713578027068E-05,"Zzb":3.7684531538646391E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01148","PARTICIPANTNAME":"招商证券(香港)有限公司","SHAREHOLDSUM":214615.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":14447881.799999999,"SHAREHOLDPRICEONE":309045.59999999963,"SHAREHOLDPRICEFIVE":629192.09999999963,"SHAREHOLDPRICETEN":751406.79999999888,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":3.5949398057116366E-05,"Zzb":3.5675631831348017E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01445","PARTICIPANTNAME":"胜利证券有限公司","SHAREHOLDSUM":200000.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":13463999.999999998,"SHAREHOLDPRICEONE":287999.99999999814,"SHAREHOLDPRICEFIVE":347999.99999999814,"SHAREHOLDPRICETEN":463999.99999999814,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":3.3501291202494108E-05,"Zzb":3.3246168097614814E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01555","PARTICIPANTNAME":"ABN AMRO CLEARING HONG KONG LTD","SHAREHOLDSUM":197643.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":13305326.759999998,"SHAREHOLDPRICEONE":1595617.9199999981,"SHAREHOLDPRICEFIVE":-1728625.9200000018,"SHAREHOLDPRICETEN":-1706163.2400000021,"MARKET":"003","ShareHoldSumChg":19900.0,"Zb":3.3106478485672712E-05,"Zzb":3.2854362006584425E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01668","PARTICIPANTNAME":"耀才证券国际(香港)有限公司","SHAREHOLDSUM":192900.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":12986027.999999998,"SHAREHOLDPRICEONE":-150444.00000000186,"SHAREHOLDPRICEFIVE":-254574.00000000186,"SHAREHOLDPRICETEN":-39972.000000001863,"MARKET":"003","ShareHoldSumChg":-6500.0,"Zb":3.2311995364805562E-05,"Zzb":3.2065929130149492E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01938","PARTICIPANTNAME":"兴证国际证券有限公司","SHAREHOLDSUM":192400.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":12952367.999999998,"SHAREHOLDPRICEONE":2569679.9999999981,"SHAREHOLDPRICEFIVE":2656307.9999999981,"SHAREHOLDPRICETEN":4502367.9999999981,"MARKET":"003","ShareHoldSumChg":34800.0,"Zb":3.222824213679933E-05,"Zzb":3.1982813709905452E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01228","PARTICIPANTNAME":"中信证券经纪(香港)有限公司","SHAREHOLDSUM":176547.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":11885144.04,"SHAREHOLDPRICEONE":1624531.6799999997,"SHAREHOLDPRICEFIVE":1015455.7799999993,"SHAREHOLDPRICETEN":2405089.0399999991,"MARKET":"003","ShareHoldSumChg":20800.0,"Zb":2.9572762289633635E-05,"Zzb":2.9347556195648015E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01089","PARTICIPANTNAME":"汇丰金融证券(香港)有限公司","SHAREHOLDSUM":174300.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":11733875.999999998,"SHAREHOLDPRICEONE":250991.99999999814,"SHAREHOLDPRICEFIVE":303281.99999999814,"SHAREHOLDPRICETEN":404375.99999999814,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":2.9196375282973611E-05,"Zzb":2.897403549707131E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01955","PARTICIPANTNAME":"富途证券国际(香港)有限公司","SHAREHOLDSUM":126300.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":8502516.0,"SHAREHOLDPRICEONE":511272.00000000093,"SHAREHOLDPRICEFIVE":-3006774.0,"SHAREHOLDPRICETEN":-3418484.0,"MARKET":"003","ShareHoldSumChg":5000.0,"Zb":2.115606539437503E-05,"Zzb":2.0994955153643759E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01256","PARTICIPANTNAME":"国金证券(香港)有限公司","SHAREHOLDSUM":120000.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":8078399.9999999991,"SHAREHOLDPRICEONE":172800.0,"SHAREHOLDPRICEFIVE":208799.99999999907,"SHAREHOLDPRICETEN":-3621600.0000000009,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":2.0100774721496462E-05,"Zzb":1.9947700858568891E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00016","PARTICIPANTNAME":"DBS BANK LTD","SHAREHOLDSUM":111700.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":7519643.9999999991,"SHAREHOLDPRICEONE":160848.0,"SHAREHOLDPRICEFIVE":4686587.9999999991,"SHAREHOLDPRICETEN":4686587.9999999991,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":1.8710471136592957E-05,"Zzb":1.8567984882517873E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01890","PARTICIPANTNAME":"国信证券(香港)经纪有限公司","SHAREHOLDSUM":100000.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":6731999.9999999991,"SHAREHOLDPRICEONE":143999.99999999907,"SHAREHOLDPRICEFIVE":173999.99999999907,"SHAREHOLDPRICETEN":231999.99999999907,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":1.6750645601247054E-05,"Zzb":1.6623084048807407E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01900","PARTICIPANTNAME":"东方证券(香港)有限公司","SHAREHOLDSUM":100000.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":6731999.9999999991,"SHAREHOLDPRICEONE":143999.99999999907,"SHAREHOLDPRICEFIVE":829799.99999999907,"SHAREHOLDPRICETEN":881999.99999999907,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":1.6750645601247054E-05,"Zzb":1.6623084048807407E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01962","PARTICIPANTNAME":"中信建投(国际)证券有限公司","SHAREHOLDSUM":99700.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":6711803.9999999991,"SHAREHOLDPRICEONE":143567.99999999907,"SHAREHOLDPRICEFIVE":173477.99999999907,"SHAREHOLDPRICETEN":231303.99999999907,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":1.6700393664443311E-05,"Zzb":1.6573214796660986E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01353","PARTICIPANTNAME":"大华继显(香港)有限公司","SHAREHOLDSUM":83100.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":5594291.9999999991,"SHAREHOLDPRICEONE":-532548.00000000093,"SHAREHOLDPRICEFIVE":-504648.00000000093,"SHAREHOLDPRICETEN":-340208.00000000093,"MARKET":"003","ShareHoldSumChg":-9900.0,"Zb":1.3919786494636301E-05,"Zzb":1.3813782844558956E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01901","PARTICIPANTNAME":"招银国际证券有限公司","SHAREHOLDSUM":65500.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":4409460.0,"SHAREHOLDPRICEONE":3388320.0,"SHAREHOLDPRICEFIVE":3497898.0,"SHAREHOLDPRICETEN":3083460.0,"MARKET":"003","ShareHoldSumChg":50000.0,"Zb":1.0971672868816821E-05,"Zzb":1.0888120051968854E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00058","PARTICIPANTNAME":"中信银行(国际)有限公司","SHAREHOLDSUM":61700.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":4153643.9999999995,"SHAREHOLDPRICEONE":88848.0,"SHAREHOLDPRICEFIVE":107357.99999999953,"SHAREHOLDPRICETEN":162643.99999999953,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":1.0335148335969432E-05,"Zzb":1.0256442858114172E-05},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"B01727","PARTICIPANTNAME":"工银亚洲证券有限公司","SHAREHOLDSUM":57218.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":3851915.76,"SHAREHOLDPRICEONE":-2025766.08,"SHAREHOLDPRICEFIVE":-4097560.6799999997,"SHAREHOLDPRICETEN":-4027254.24,"MARKET":"003","ShareHoldSumChg":-32000.0,"Zb":9.58438440012154E-06,"Zzb":9.5113962310466229E-06},{"HDDATE":"2020-01-07T00:00:00","HKCODE":"1000004198","SCODE":"000651","SNAME":"格力电器","PARTICIPANTCODE":"C00042","PARTICIPANTNAME":"招商永隆银行有限公司","SHAREHOLDSUM":52152.0,"SHARESRATE":0.0,"CLOSEPRICE":67.32,"ZDF":2.1858,"SHAREHOLDPRICE":3510872.6399999997,"SHAREHOLDPRICEONE":75098.879999999888,"SHAREHOLDPRICEFIVE":90744.479999999981,"SHAREHOLDPRICETEN":120992.63999999966,"MARKET":"003","ShareHoldSumChg":0.0,"Zb":8.7357966939623633E-06,"Zzb":8.66927079313404E-06}]
'''


filePath = '/Users/wangshan/Desktop/test.xls'
otherfilePath = '/Users/wangshan/Desktop/test_a.xls'
def test():
    sess = requests.Session()

    # res = sess.get(url='http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=HSGTSHHDDET&token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&sr=3&p=1&ps=250&js=var%20abtQHJpH={pages:(tp),data:(x)}&filter=(SCODE=%27000725%27)(HDDATE=^2020-01-08^)&rt=52618099')
    # print(res.text)
    resDict = json.loads(testStr)
    for item in resDict:
        print(len(item))
        print(item.get('HDDATE'))

def testWriteExl():
    file = xlwt.Workbook()
    sheet1 = file.add_sheet('test_stock' , cell_overwrite_ok=True)
    sheet2 = file.add_sheet('test_stock2' , cell_overwrite_ok=True)
    resDict = json.loads(testStr)
    for j in range(len(resDict)):
        for i in range(3):
            sheet1.write(j , i ,"=HYPERLINK(\"/Users/shanwang/Desktop/test_a.xls\",\"aa\")")
    file.save(filePath)

def bshy_detail():
    file = xlwt.Workbook()
    bszjhySheet = file.add_sheet("北上资金行业板块详情" , cell_overwrite_ok=True)
    sess = requests.Session()
    res = sess.get(url=bshy_detail_url)
    data = res.text.split("data:")[1][:-1]
    dataList = json.loads(data)
    print(dataList[0].keys())




def bshy():
    file = xlwt.Workbook()
    bszjhySheet = file.add_sheet("北上资金行业板块" , cell_overwrite_ok=True)
    sess = requests.Session()
    res = sess.get(url=bshy_url)
    data = res.text.split("data:")[1][:-1]
    dataList = json.loads(data)

    print(dataList[0])
    k = 0
    for key in nameMapping.keys():
        bszjhySheet.write(0,k , nameMapping.get(key))
        k = k + 1

    for i in range(len(dataList)):
        j = 0
        for key in nameMapping.keys():
            res = dataList[i].get(key)
            if key == 'Zdf':
                res = str(round(res, 2)) + '%'
            elif key in ['ShareSZ_GZ' , 'ShareSZ_ZC']:
                res = str(round(res / 100000000, 2)) + '亿'
            elif key in ['ShareHold_Chg_BK' , 'ShareHold_Chg_GZ']:
                res = str(round(res * 100 ,2)) + '%'
            elif key in ['ShareHold_ZC_Chg_BK' , 'ShareHold_ZC_Chg_GZ']:
                res = str(round(res * 1000 ,2)) + '%'


            bszjhySheet.write(i + 1 , j , res)
            j = j + 1
    file.save(filePath)

def bsgg():
    file = xlwt.Workbook()
    bsggSheet = file.add_sheet("北上资金个股" , cell_overwrite_ok=True)
    sess = requests.Session()
    res = sess.get(url=bsgg_url)
    data = res.text.split("data:")[1][:-1]
    dataList = json.loads(data)
    print(dataList[0])
    for i in range(len(dataList)):
        j = 0
        for key in bsgg_nameMapping.keys():
            bsggSheet.write(i , j , dataList[i].get(key))
            j = j + 1
    file.save(filePath)

def getRzRqDetailList(startDt , endDt):
    for code in getAllStock():
        getAndSaverzrqDetail(code)


def getRzRqDetailByDt(startDt , endDt):
    for dt in getDtList(startDt,endDt):
        getAndSaverzrqDetailByDt(dt)


def getAndSaverzrqDetailByDt(dt):
    for i in range(100):
        result_data = []
        sess = requests.Session()
        url = 'http://api.dataide.eastmoney.com/data/get_rzrq_ggmx?pageindex=' + str(i+1) + '&pagesize=500&orderby=rzjme&order=desc&date=' + dt + '&jsonp_callback=var%20njWHabsi=(x)&rt=52802785'
        try:
            startTime = time.time()
            res = sess.get(url=url)
            data = res.text.split('DLgtJLPl=')[1]
            dataMap = json.loads(data)
            dataList = dataMap.get('data')
            for item in dataList:
                try:
                    tmp = {}
                    timeArray = time.localtime(item.get('date')/1000)
                    date = time.strftime("%Y-%m-%d", timeArray)
                    tmp['hd_date']=date
                    tmp['stock_code']=item.get('scode')
                    tmp['stock_name']=item.get('secname')
                    if item.get('close_price',0) is None:
                        item['close_price'] = 0
                    if item.get('zdf',0) is None:
                        item['zdf'] = 0
                    if item.get('rzye',0) is None:
                        item['rzye'] = 0
                    if item.get('rzyezb',0) is None:
                        item['rzyezb'] = 0
                    if item.get('rqye',0) is None:
                        item['rqye'] = 0
                    if item.get('rzrqye',0) is None:
                        item['rzrqye'] = 0
                    if item.get('rzrqyecz',0) is None:
                        item['rzrqyecz'] = 0

                    if item.get('rzmre',0) is None:
                        item['rzmre'] = 0
                    if item.get('rzche',0) is None:
                        item['rzche'] = 0
                    if item.get('rzjme',0) is None:
                        item['rzjme'] = 0
                    if item.get('rqmcl',0) is None:
                        item['rqmcl'] = 0
                    if item.get('rqchl',0) is None:
                        item['rqchl'] = 0
                    if item.get('rqjmg',0) is None:
                        item['rqjmg'] = 0

                    if item.get('rzmre3d',0) is None:
                        item['rzmre3d'] = 0
                    if item.get('rzche3d',0) is None:
                        item['rzche3d'] = 0
                    if item.get('rzjme3d',0) is None:
                        item['rzjme3d'] = 0
                    if item.get('rqmcl3d',0) is None:
                        item['rqmcl3d'] = 0
                    if item.get('rqchl3d',0) is None:
                        item['rqchl3d'] = 0
                    if item.get('rqjmg3d',0) is None:
                        item['rqjmg3d'] = 0

                    if item.get('rzmre5d',0) is None:
                        item['rzmre5d'] = 0
                    if item.get('rzche5d',0) is None:
                        item['rzche5d'] = 0
                    if item.get('rzjme5d',0) is None:
                        item['rzjme5d'] = 0
                    if item.get('rqmcl5d',0) is None:
                        item['rqmcl5d'] = 0
                    if item.get('rqchl5d',0) is None:
                        item['rqchl5d'] = 0
                    if item.get('rqjmg5d',0) is None:
                        item['rqjmg5d'] = 0

                    if item.get('rzmre10d',0) is None:
                        item['rzmre10d'] = 0
                    if item.get('rzche10d',0) is None:
                        item['rzche10d'] = 0
                    if item.get('rzjme10d',0) is None:
                        item['rzjme10d'] = 0
                    if item.get('rqmcl10d',0) is None:
                        item['rqmcl10d'] = 0
                    if item.get('rqchl10d',0) is None:
                        item['rqchl10d'] = 0
                    if item.get('rqjmg10d',0) is None:
                        item['rqjmg10d'] = 0

                    tmp['close_price']=str(round(item.get('close_price',0), 5))
                    tmp['zdf']=str(round(item.get('zdf',0), 5))
                    tmp['rz_remain_sum']=str(round(item.get('rzye',0), 5))
                    tmp['rz_remain_sum_percent']=str(round(item.get('rzyezb',0), 5))
                    tmp['rq_remain_sum']=str(round(item.get('rqye',0), 5))
                    tmp['rq_margin']=str(round(item.get('rqyl',0), 5))
                    tmp['rzrq_remain_sum']=str(round(item.get('rzrqye',0), 5))
                    tmp['rzrq_remain_sum_margin']=str(round(item.get('rzrqyecz',0), 5))
                    tmp['rz_buy_one']=str(round(item.get('rzmre',0), 5))
                    tmp['rz_repay_one']=str(round(item.get('rzche',0), 5))
                    tmp['rz_net_buy_one']=str(round(item.get('rzjme',0), 5))
                    tmp['rq_sell_one']=str(round(item.get('rqmcl',0), 5))
                    tmp['rq_repay_one']=str(round(item.get('rqchl',0), 5))
                    tmp['rq_net_sell_one']=str(round(item.get('rqjmg',0), 5))
                    tmp['rz_buy_three']=str(round(item.get('rzmre3d',0), 5))
                    tmp['rz_repay_three']=str(round(item.get('rzche3d',0), 5))
                    tmp['rz_net_buy_three']=str(round(item.get('rzjme3d',0), 5))
                    tmp['rq_sell_three']=str(round(item.get('rqmcl3d',0), 5))
                    tmp['rq_repay_three']=str(round(item.get('rqchl3d',0), 5))
                    tmp['rq_net_sell_three']=str(round(item.get('rqjmg3d',0), 5))
                    tmp['rz_buy_five']=str(round(item.get('rzmre5d',0), 5))
                    tmp['rz_repay_five']=str(round(item.get('rzche5d',0), 5))
                    tmp['rz_net_buy_five']=str(round(item.get('rzjme5d',0), 5))
                    tmp['rq_sell_five']=str(round(item.get('rqmcl5d',0), 5))
                    tmp['rq_repay_five']=str(round(item.get('rqchl5d',0), 5))
                    tmp['rq_net_sell_five']=str(round(item.get('rqjmg5d',0), 5))
                    tmp['rz_buy_ten']=str(round(item.get('rzmre10d',0), 5))
                    tmp['rz_repay_ten']=str(round(item.get('rzche10d',0), 5))
                    tmp['rz_net_buy_ten']=str(round(item.get('rzjme10d',0), 5))
                    tmp['rq_sell_ten']=str(round(item.get('rqmcl10d',0), 5))
                    tmp['rq_repay_ten']=str(round(item.get('rqchl10d',0), 5))
                    tmp['rq_net_sell_ten']=str(round(item.get('rqjmg10d',0), 5))
                    result_data.append(tmp)
                except Exception as e:
                    print(e)
            saveRzRqStockDetail(result_data)
            print(code + ' ' + str(i+1) + ' time : ' + str(time.time() - startTime))
            if len(dataList) < 450:
                print(code  + ' ' + str(i+1) + ' len : ' + str(len(dataList)))
                return
        except Exception as e:
            traceback.print_exc()
            f.write(url + '\n')
            print(url)
            print(e)



def getAndSaverzrqDetail(code):
    for i in range(100):
        result_data = []
        sess = requests.Session()
        url = 'http://api.dataide.eastmoney.com/data/get_rzrq_ggmx?code='+code+'&orderby=date&order=desc&pageindex='+str(i+1)+'&pagesize=500&jsonp_callback=var%20DLgtJLPl=(x)&rt=52794205'
        try:
            startTime = time.time()
            res = sess.get(url=url)
            data = res.text.split('DLgtJLPl=')[1]
            dataMap = json.loads(data)
            dataList = dataMap.get('data')
            for item in dataList:
                try:
                    tmp = {}
                    timeArray = time.localtime(item.get('date')/1000)
                    date = time.strftime("%Y-%m-%d", timeArray)
                    tmp['hd_date']=date
                    tmp['stock_code']=item.get('scode')
                    tmp['stock_name']=item.get('secname')
                    if item.get('close_price',0) is None:
                        item['close_price'] = 0
                    if item.get('zdf',0) is None:
                        item['zdf'] = 0
                    if item.get('rzye',0) is None:
                        item['rzye'] = 0
                    if item.get('rzyezb',0) is None:
                        item['rzyezb'] = 0
                    if item.get('rqye',0) is None:
                        item['rqye'] = 0
                    if item.get('rzrqye',0) is None:
                        item['rzrqye'] = 0
                    if item.get('rzrqyecz',0) is None:
                        item['rzrqyecz'] = 0

                    if item.get('rzmre',0) is None:
                        item['rzmre'] = 0
                    if item.get('rzche',0) is None:
                        item['rzche'] = 0
                    if item.get('rzjme',0) is None:
                        item['rzjme'] = 0
                    if item.get('rqmcl',0) is None:
                        item['rqmcl'] = 0
                    if item.get('rqchl',0) is None:
                        item['rqchl'] = 0
                    if item.get('rqjmg',0) is None:
                        item['rqjmg'] = 0

                    if item.get('rzmre3d',0) is None:
                        item['rzmre3d'] = 0
                    if item.get('rzche3d',0) is None:
                        item['rzche3d'] = 0
                    if item.get('rzjme3d',0) is None:
                        item['rzjme3d'] = 0
                    if item.get('rqmcl3d',0) is None:
                        item['rqmcl3d'] = 0
                    if item.get('rqchl3d',0) is None:
                        item['rqchl3d'] = 0
                    if item.get('rqjmg3d',0) is None:
                        item['rqjmg3d'] = 0

                    if item.get('rzmre5d',0) is None:
                        item['rzmre5d'] = 0
                    if item.get('rzche5d',0) is None:
                        item['rzche5d'] = 0
                    if item.get('rzjme5d',0) is None:
                        item['rzjme5d'] = 0
                    if item.get('rqmcl5d',0) is None:
                        item['rqmcl5d'] = 0
                    if item.get('rqchl5d',0) is None:
                        item['rqchl5d'] = 0
                    if item.get('rqjmg5d',0) is None:
                        item['rqjmg5d'] = 0

                    if item.get('rzmre10d',0) is None:
                        item['rzmre10d'] = 0
                    if item.get('rzche10d',0) is None:
                        item['rzche10d'] = 0
                    if item.get('rzjme10d',0) is None:
                        item['rzjme10d'] = 0
                    if item.get('rqmcl10d',0) is None:
                        item['rqmcl10d'] = 0
                    if item.get('rqchl10d',0) is None:
                        item['rqchl10d'] = 0
                    if item.get('rqjmg10d',0) is None:
                        item['rqjmg10d'] = 0

                    tmp['close_price']=str(round(item.get('close_price',0), 5))
                    tmp['zdf']=str(round(item.get('zdf',0), 5))
                    tmp['rz_remain_sum']=str(round(item.get('rzye',0), 5))
                    tmp['rz_remain_sum_percent']=str(round(item.get('rzyezb',0), 5))
                    tmp['rq_remain_sum']=str(round(item.get('rqye',0), 5))
                    tmp['rq_margin']=str(round(item.get('rqyl',0), 5))
                    tmp['rzrq_remain_sum']=str(round(item.get('rzrqye',0), 5))
                    tmp['rzrq_remain_sum_margin']=str(round(item.get('rzrqyecz',0), 5))
                    tmp['rz_buy_one']=str(round(item.get('rzmre',0), 5))
                    tmp['rz_repay_one']=str(round(item.get('rzche',0), 5))
                    tmp['rz_net_buy_one']=str(round(item.get('rzjme',0), 5))
                    tmp['rq_sell_one']=str(round(item.get('rqmcl',0), 5))
                    tmp['rq_repay_one']=str(round(item.get('rqchl',0), 5))
                    tmp['rq_net_sell_one']=str(round(item.get('rqjmg',0), 5))
                    tmp['rz_buy_three']=str(round(item.get('rzmre3d',0), 5))
                    tmp['rz_repay_three']=str(round(item.get('rzche3d',0), 5))
                    tmp['rz_net_buy_three']=str(round(item.get('rzjme3d',0), 5))
                    tmp['rq_sell_three']=str(round(item.get('rqmcl3d',0), 5))
                    tmp['rq_repay_three']=str(round(item.get('rqchl3d',0), 5))
                    tmp['rq_net_sell_three']=str(round(item.get('rqjmg3d',0), 5))
                    tmp['rz_buy_five']=str(round(item.get('rzmre5d',0), 5))
                    tmp['rz_repay_five']=str(round(item.get('rzche5d',0), 5))
                    tmp['rz_net_buy_five']=str(round(item.get('rzjme5d',0), 5))
                    tmp['rq_sell_five']=str(round(item.get('rqmcl5d',0), 5))
                    tmp['rq_repay_five']=str(round(item.get('rqchl5d',0), 5))
                    tmp['rq_net_sell_five']=str(round(item.get('rqjmg5d',0), 5))
                    tmp['rz_buy_ten']=str(round(item.get('rzmre10d',0), 5))
                    tmp['rz_repay_ten']=str(round(item.get('rzche10d',0), 5))
                    tmp['rz_net_buy_ten']=str(round(item.get('rzjme10d',0), 5))
                    tmp['rq_sell_ten']=str(round(item.get('rqmcl10d',0), 5))
                    tmp['rq_repay_ten']=str(round(item.get('rqchl10d',0), 5))
                    tmp['rq_net_sell_ten']=str(round(item.get('rqjmg10d',0), 5))
                    result_data.append(tmp)
                except Exception as e:
                    print(e)
            saveRzRqStockDetail(result_data)
            print(code + ' ' + str(i+1) + ' time : ' + str(time.time() - startTime))
            if len(dataList) < 450:
                print(code  + ' ' + str(i+1) + ' len : ' + str(len(dataList)))
                return
        except Exception as e:
            traceback.print_exc()
            f.write(url + '\n')
            print(url)
            print(e)

def getBsDtDetailList(startDt , endDt):
    for partition in getAllParitionFromDB():
        for dt in getDtList(startDt,endDt):
            getAndsavePartitionDtDetail(partition , dt)


def getAndsavePartitionDtDetail(partitionCode , dt):
    for i in range(10):
        result_data = []
        sess = requests.Session()
        url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&sr=3&p=' + str(i+1) + '&ps=500&js=var%20hjqVpcJG={pages:(tp),data:(x)}&filter=(PARTICIPANTCODE=%27'+ partitionCode +'%27)(MARKET%20in%20(%27001%27,%27003%27))(HDDATE=^'+ dt +'^)&type=HSGTNHDDET&rt=52629792'
        try:
            startTime = time.time()
            res = sess.get(url=url)
            data = res.text.split("data:")[1][:-1]
            dataList = json.loads(data)
            for item in dataList:
                result_data.append(item)
            savePartitionStockDetail(result_data)
            print(partitionCode + ' ' + dt + ' ' + str(i+1) + ' time : ' + str(time.time() - startTime))
            if len(dataList) < 450:
                print(partitionCode + ' ' + dt + ' ' + str(i+1) + ' len : ' + str(len(dataList)))
                return
        except Exception as e:
            f.write(url + '\n')
            print(url)
            print(e)
def getAndsavePartitionDtDetailFromUrl(url):
    result_data = []
    sess = requests.Session()
    try:
        startTime = time.time()
        res = sess.get(url=url)
        data = res.text.split("data:")[1][:-1]
        dataList = json.loads(data)
        for item in dataList:
            result_data.append(item)
        savePartitionStockDetail(result_data)
        print(' time : ' + str(time.time() - startTime))
    except Exception as e:
        f.write(url + '\n')
        print(url)
        print(e)

def getDtList(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates
def getBXJGList():
    for day in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']:
        partitionList = []
        res = requests.get(url='http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=HSGTCOMSTA&token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDCOUNT&sr=3&p=1&ps=500&js=var%20lMCByFSy={pages:(tp),data:(x)}&filter=(MARKET=%27N%27)(HDDATE=^2020-02-'+ day +'^)&rt=52628114')
        data = res.text.split("data:")[1][:-1]
        dataList = json.loads(data)
        for item in dataList:
            partitionList.append({"name":item.get("PARTICIPANTNAME"),"code":item.get("PARTICIPANTCODE")})
        print(partitionList)
        saveAllParition(partitionList)
def saveAllParition(paritionList):

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    for item in paritionList:
        # SQL 插入语句
        sql = 'INSERT INTO all_partition(name ,code) VALUES ("'+ item.get('name')+'","'+item.get('code')+'")'
        # print(sql)

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            print("err")
    # 关闭数据库连接
    db.close()
def getStockList():
    result = []
    res = requests.get(url=stock_list_url)
    htmlTree=etree.HTML(res.content.decode('gbk'))
    stockList =htmlTree.xpath("/html/body/div[@class='qox']/div[@class='quotebody']/div[@id='quotesearch']/ul/li/a//text()")
    for item in stockList:
        # stockStr = etree.tostring(item , encoding='utf-8')
        stockData = item.split('(')
        name = stockData[0]
        code = stockData[1].replace(')','')
        if isAStock(code=code):
            result.append({"name":name , "code":code})
    saveAllStock(result)
def isAStock(code):
    if code[0] == '6' or code[0] == '0' or code[:3] == '300':
        return True
    return False
def saveAllStock(stockList):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    for item in stockList:
        # SQL 插入语句
        sql = 'INSERT INTO allstock(name ,code) VALUES ("'+ item.get('name')+'","'+item.get('code')+'")'
        # print(sql)
        # 执行sql语句
        cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()

def savePartitionStockDetail(details):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    for item in details:
        try:
            # SQL 插入语句
            sql = 'INSERT INTO partition_stock_detail(hd_date ,partition_code,stock_code,close_price,hold_sum,hold_money,today_zd,hold_sum_percent,hold_change_one,hold_change_five,hold_change_ten) ' \
                  'VALUES ("' + item.get('HDDATE') + '","' + item.get('PARTICIPANTCODE') + '","'+ item.get('SCODE') + '","'+ str(round(item.get('CLOSEPRICE'), 5))+'","'+str(round(item.get('SHAREHOLDSUM'), 5))\
                  + '","' + str(round(item.get('SHAREHOLDPRICE'), 5))+'","'+ str(round(item.get('ZDF'), 5))+'","'\
                  +str(round(item.get('Zb'), 5))+ '","'+ str(round(item.get('SHAREHOLDPRICEONE'), 5))+'","'+ str(round(item.get('SHAREHOLDPRICEFIVE'), 5))+'","'+str(round(item.get('SHAREHOLDPRICETEN'), 5))+ '")'

            # 执行sql语句
            cursor.execute(sql)
        except Exception as e:
            print(e)
            # traceback.print_exc()
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()


def saveRzRqStockDetail(details):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    for item in details:
        try:
            # SQL 插入语句
            sql =  'INSERT INTO rzrq_stock_detail(hd_date,stock_code,stock_name,close_price,zdf,rz_remain_sum,rz_remain_sum_percent,rq_remain_sum,rq_margin,rzrq_remain_sum,rzrq_remain_sum_margin,rz_buy_one,rz_repay_one,rz_net_buy_one,rq_sell_one,rq_repay_one,rq_net_sell_one,rz_buy_three,rz_repay_three,rz_net_buy_three,rq_sell_three,rq_repay_three,rq_net_sell_three,rz_buy_five,rz_repay_five,rz_net_buy_five,rq_sell_five,rq_repay_five,rq_net_sell_five,rz_buy_ten,rz_repay_ten,rz_net_buy_ten,rq_sell_ten,rq_repay_ten,rq_net_sell_ten) VALUES ("'+item.get('hd_date')+'","'+item.get('stock_code')+'","'+item.get('stock_name')+'","'+item.get('close_price')+'","'+item.get('zdf')+'","'+item.get('rz_remain_sum')+'","'+item.get('rz_remain_sum_percent')+'","'+item.get('rq_remain_sum')+'","'+item.get('rq_margin')+'","'+item.get('rzrq_remain_sum')+'","'+item.get('rzrq_remain_sum_margin')+'","'+item.get('rz_buy_one')+'","'+item.get('rz_repay_one')+'","'+item.get('rz_net_buy_one')+'","'+item.get('rq_sell_one')+'","'+item.get('rq_repay_one')+'","'+item.get('rq_net_sell_one')+'","'+item.get('rz_buy_three')+'","'+item.get('rz_repay_three')+'","'+item.get('rz_net_buy_three')+'","'+item.get('rq_sell_three')+'","'+item.get('rq_repay_three')+'","'+item.get('rq_net_sell_three')+'","'+item.get('rz_buy_five')+'","'+item.get('rz_repay_five')+'","'+item.get('rz_net_buy_five')+'","'+item.get('rq_sell_five')+'","'+item.get('rq_repay_five')+'","'+item.get('rq_net_sell_five')+'","'+item.get('rz_buy_ten')+'","'+item.get('rz_repay_ten')+'","'+item.get('rz_net_buy_ten')+'","'+item.get('rq_sell_ten')+'","'+item.get('rq_repay_ten')+'","'+item.get('rq_net_sell_ten')+'")'

            # 执行sql语句
            cursor.execute(sql)
        except Exception as e:
            print(e)
            # traceback.print_exc()
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()

def getAllStock():
    stocks = []
    rows = mysql_dao.queryBySql("select * from allstock")
    for item in rows:
        stocks.append(item[2])
    return stocks
def getAllParitionFromDB():
    resp = []
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = "select * from all_partition"
    # 执行sql语句
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        resp.append(row[2])
    # 关闭数据库连接
    db.close()
    return resp

def getfailUrl(filePath):
    with open(filePath, "r") as file:
        for line in file.readlines():
            url = line.replace("\n","")
            getAndsavePartitionDtDetailFromUrl(url)


def query(sql_temp ,stock_code , dt ,partition_code):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "wangshan", "stock")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = sql_temp.format(stock_code=stock_code , dt = dt , partition_code=partition_code)
    # 执行sql语句
    cursor.execute(sql)
    result = cursor.fetchone()
    # 关闭数据库连接
    db.close()
    return result

def testCrawlerCount(countPartition , startDt , endDt):
    partition = getAllParitionFromDB()
    allDt = getDtList(startDt , endDt)
    for dt in allDt:
        for i in range(countPartition):
            ranparti = random.randint(1,len(partition))
            code = partition[ranparti]
            sess = requests.Session()
            url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&sr=3&p=1&ps=50&js=var%20hjqVpcJG={pages:(tp),data:(x)}&filter=(PARTICIPANTCODE=%27' + code + '%27)(MARKET%20in%20(%27001%27,%27003%27))(HDDATE=^' + dt + '^)&type=HSGTNHDDET&rt=52629792'
            res = sess.get(url=url)
            try:
                pages = res.text.split("pages:")[1].split(",")[0]
                res = query(testCountSql,'' ,dt ,code)
                if int(pages)*50 - res[0] >50:
                    print("loss\t"+dt + "\t" +code )
                else:
                    print("ok\t"+dt + "\t" +code )
            except Exception as e:
                print(e)


def testCrawlerQuality(countPartition , startDt , endDt):
    partition = getAllParitionFromDB()
    allDt = getDtList(startDt , endDt)
    for dt in allDt:
        for i in range(countPartition):
            ranparti = random.randint(1,len(partition))
            code = partition[ranparti]
            sess = requests.Session()
            url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&sr=3&p=1&ps=50&js=var%20hjqVpcJG={pages:(tp),data:(x)}&filter=(PARTICIPANTCODE=%27' + code + '%27)(MARKET%20in%20(%27001%27,%27003%27))(HDDATE=^' + dt + '^)&type=HSGTNHDDET&rt=52629792'
            res = sess.get(url=url)
            data = res.text.split("data:")[1][:-1]
            dataList = json.loads(data)
            for item in dataList:
                result = query(testQualitySql , item.get('SCODE') , dt , item.get('PARTICIPANTCODE'))
                if result[4] == round(item.get('CLOSEPRICE'), 5) and result[5] == round(item.get('SHAREHOLDSUM'), 5) \
                        and result[6] == round(item.get('SHAREHOLDPRICE'), 5) and  result[7] == round(item.get('ZDF'), 5)\
                        and  result[9] == round(item.get('SHAREHOLDPRICEONE'), 5)\
                        and result[10] == round(item.get('SHAREHOLDPRICEFIVE'), 5) and result[11] == round(item.get('SHAREHOLDPRICETEN'), 5):
                    print("ok")
                else:
                    print("mismatch" + "\t" + str(item)+"\t" + str(result))

def testRzrq(code , dt):
    sess = requests.Session()
    res = sess.get(url=rzrq_detail_url)
    print(res.text.split('DLgtJLPl=')[1])
    data = res.text.split('DLgtJLPl=')[1]
    dataMap = json.loads(data)
    for item in dataMap.get('data'):
        print(item)


if __name__ == '__main__':
    # getBXJGList()
    # getfailUrl(err_url_path)
    # getAndsavePartitionDtDetail('B01451' , '2019-12-16')
    getBsDtDetailList('2020-03-09' , '2020-03-12')
    # getRzRqDetailList('2020-03-06' , '2020-03-06')

    # testCrawlerCount(7,"2019-12-16","2019-12-20")
    # testCrawlerQuality(7,"2019-12-16","2019-12-20")
    # f.close()
