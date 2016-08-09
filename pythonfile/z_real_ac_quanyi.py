#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList




def ac_item_quanyi(ac):
	try:
		viewname="View_"+ac
		sql="select [STOCK],[Expr1],getdate() as inserttime from %s" % (viewname)
		res=ms.dict_sql(sql)
		for item in res:
			inserttime=item['inserttime'].strftime('%Y-%m-%d %H:%M:%S')
			sql="insert into [LogRecord].[dbo].[real_ac_quanyi](ac,position,stock,inserttime) values('%s',%s,%s,'%s')" % (ac,item['Expr1'],item['STOCK'],inserttime)
			ms.insert_sql(sql)
	except Exception,e:
		print ac
		print e




def ac_list_quanyi(aclist):
	for value in aclist:
		ac_item_quanyi(value)



def  main_fun():
	TAlist=('CH4tazs','DayBrTA','DayTALineRrate')
	RUlist=('RUDTA','RUMY','RUV4E','RUv4ehc','RUV7','RUWEEKLY')
	RBlist=('Rb_QGpLud','RbCX_QGRev','RbCX_QGtr','RB_CXVolume','RB_Daybreaker','RB_LiangtuPipei','RB_LRC_Trend','RB_LUD','RB_MT','RB_RBreaker','RB_RSI','RB_ST_Reversal','RB_ST_Trend','RB_VPIN','RB_ZhixianPipei','CH4RBZS','DAYGAPRB','RBHAL','RBPUD','RBSV','UDKRB','V7RB','RBQGstrev_TG','RBQGTR_TG')
	CUlist=('CUDUDHL','ESPcu','LKVCU1','LKVCU2','PUDCU','QCU18MIN','QPMCU','Vk2CU','CUVK3')
	AGlist=('9AGOLD','9AGVD05','9AGVD06','AGNEW4','AGNEW6','AGNEW8','AGNEW19','AGNEWLVO')
	IClist=('YEEXIC','YEOTIC','YETRIC','YEZHIC')
	IFlist=('9CPPUD','DayBrIF','9Distance','9DUD1','9DUDHL','9DUDRV','9EXR1410','9EXV1410','9FORCE','9FQS1','9HAL','9HAL2','9HAL3','9HALMA','9HUITIAO','9HUITIAO2','9HUITIAO3','9HUITIAO4','9KDHDAY','9KDHPM','9Linerate','9RATE','9MALONGK','9MiddayTrend','9MinVolPbuy','9MONDAY','9MORNINGOUT','9MT','9MVRATE','9NHL','9NOON','9OpenBet','9QMA','9QPMIF','9Reversal','9Reversal2','9Reversal3','9V4EIV','9VK1','9VK3','9VPINVOl_L','9VPINVOl_S','9VPINVOl_S2','9wb','9weipan','9WeipanREV','9WeipanStatics','9YAP01','9YY2','9YYMA','9LUD','9LUD2CH','9LUD3','9LUD4','9LUD5','9LUD6','9LUD7','9LUD8','9LUD10','9LUD11V2','9LUD13','9LUD14','9LUD16','LUDch1','LUDch4','LUDch5','LUDch6','LUDch8','LUD52015','LUD62015','LUD72015','LUD82015','TimeV2Pm','TimeV3DtaPm','TimeV3HLAm','TimeV3HLPm','V4EIVelements','V4EIVNEW','IFQG1310','IFQGEX','IFQGOT','9QGBombma2','IFQGTB','IFQGTR','IFQGWB','YEQGTR','YEQGEX','YEQGOT','YEQGZH211')
	ICIFlist=('YEQGEX','YEQGOT','YEQGTR')
	ac_list_quanyi(TAlist)
	ac_list_quanyi(RUlist)
	ac_list_quanyi(RBlist)
	ac_list_quanyi(CUlist)
	ac_list_quanyi(AGlist)
	ac_list_quanyi(IClist)
	ac_list_quanyi(IFlist)





main_fun()