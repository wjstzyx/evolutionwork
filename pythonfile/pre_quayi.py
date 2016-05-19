#coding=utf-8 
#!/usr/bin/env python
###检测st_report 和P_LOG 的联合记录是否连续

import sys
import threading
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

#将记录放入临时表(14秒)
def input_temp_table(ac,symbol,type):
	try:
		sql="drop table ##temp_quanyi"
		ms.insert_sql(sql)
	except:
		pass
	sql="select * into  ##temp_quanyi from (select '%s' as ac,'%s' as symbol,'%s' as type,temp.id,p,PP,p_size,ratio,st,o.stockdate from tsymbol o left outer join (select st_report.id,st_report.p,st_report.pp,p.symbol,st_report.stockdate,st_report.st,p.p_size,p.ac,p.ratio,st_report.type from st_report  inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and p.d=st_report.d and st_report.type=%s ) temp on temp.stockdate=o.stockdate and o.symbol=temp.symbol where o.symbol='%s' ) temp " % (ac,symbol,type,ac,symbol,type,symbol)
	ms.insert_sql(sql)
	sql="UPDATE ##temp_quanyi  SET PP=0 where id in(select MIN(id) as id from ##temp_quanyi a inner join(select min(stockdate) as stockdate,st from ##temp_quanyi  where p is not null group by st) temp on a.stockdate=temp.stockdate and a.st=temp.st group by a.stockdate,a.st) and pp!=0"
	ms.insert_sql(sql)
	sql="select top 1 * from [quanyi_log] where AC='%s' AND Symbol='%s' and TYPE=%s order by stockdate desc " % (ac,symbol,type)
	res=ms.dict_sql(sql)
	if not res:
		sql="insert into [quanyi_log] select * from  ##temp_quanyi"
		ms.insert_sql(sql)
	else:
		laststockdate=res[0]['stockdate']
		sql="insert into [quanyi_log] select * from  ##temp_quanyi where StockDate>'%s'" % (laststockdate)
		ms.insert_sql(sql)
	sql="drop table ##temp_quanyi"
	ms.insert_sql(sql)
	print "OK"







def pre_quanyi_data(ac,symbol,type):
	input_temp_table(ac,symbol,type)



def pre_data_for_ac(itemlist,symbol):
	i=0
	for item in itemlist:
		i=i+1
		ac=item
		print i,ac,symbol
		pre_quanyi_data(ac,symbol,0)
		pre_quanyi_data(ac,symbol,1)




def main_pre_quanyi():
	i=0
	TAlist=('CH4tazs','DayBrTA','DayTALineRrate')
	RUlist=('RUDTA','RUMY','RUV4E','RUv4ehc','RUV7','RUWEEKLY')
	RBlist=('Rb_QGpLud','RbCX_QGRev','RbCX_QGtr','RB_CXVolume','RB_Daybreaker','RB_LiangtuPipei','RB_LRC_Trend','RB_LUD','RB_MT','RB_RBreaker','RB_RSI','RB_ST_Reversal','RB_ST_Trend','RB_VPIN','RB_ZhixianPipei','CH4RBZS','DAYGAPRB','RBHAL','RBPUD','RBSV','UDKRB','V7RB')
	CUlist=('CUDUDHL','ESPcu','LKVCU1','LKVCU2','PUDCU','QCU18MIN','QPMCU','Vk2CU','CUVK3')
	AGlist=('9AGOLD','9AGVD05','9AGVD06','AGNEW4','AGNEW6','AGNEW8','AGNEW19','AGNEWLVO')
	IClist=('YEEXIC','YEOTIC','YETRIC','YEZHIC')
	IFlist=('9CPPUD','DayBrIF','9Distance','9DUD1','9DUDHL','9DUDRV','9EXR1410','9EXV1410','9FORCE','9FQS1','9HAL','9HAL2','9HAL3','9HALMA','9HUITIAO','9HUITIAO2','9HUITIAO3','9HUITIAO4','9KDHDAY','9KDHPM','9Linerate','9RATE','9MALONGK','9MiddayTrend','9MinVolPbuy','9MONDAY','9MORNINGOUT','9MT','9MVRATE','9NHL','9NOON','9OpenBet','9QMA','9QPMIF','9Reversal','9Reversal2','9Reversal3','9V4EIV','9VK1','9VK3','9VPINVOl_L','9VPINVOl_S','9VPINVOl_S2','9wb','9weipan','9WeipanREV','9WeipanStatics','9YAP01','9YY2','9YYMA','9LUD','9LUD2CH','9LUD3','9LUD4','9LUD5','9LUD6','9LUD7','9LUD8','9LUD10','9LUD11V2','9LUD13','9LUD14','9LUD16','LUDch1','LUDch4','LUDch5','LUDch6','LUDch8','LUD52015','LUD62015','LUD72015','LUD82015','TimeV2Pm','TimeV3DtaPm','TimeV3HLAm','TimeV3HLPm','V4EIVelements','V4EIVNEW','IFQG1310','IFQGEX','IFQGOT','9QGBombma2','IFQGTB','IFQGTR','IFQGWB','YEQGTR','YEQGEX','YEQGOT','YEQGZH211')

	# pre_data_for_ac(RBlist,'RB')
	# pre_data_for_ac(CUlist,'CU')
	# pre_data_for_ac(AGlist,'AG')
	# pre_data_for_ac(IClist,'IC')
	# pre_data_for_ac(IFlist,'IF')
	# pre_data_for_ac(RUlist,'RU')
	# pre_data_for_ac(TAlist,'TA')



print "ddd"
sql="select 1"
res=ms.dict_sql(sql)
print res
main_pre_quanyi()
# pre_quanyi_data('DayBrIF','IF',0)
# pre_quanyi_data('DayBrIF','IF',1)
# pre_quanyi_data('LUDch1','IF',0)
# pre_quanyi_data('LUDch1','IF',1)
# pre_quanyi_data('LUDch4','IF',0)
# pre_quanyi_data('LUDch4','IF',1)
# pre_quanyi_data('LUDch5','IF',0)
# pre_quanyi_data('LUDch5','IF',1)
# pre_quanyi_data('LUDch6','IF',0)
# pre_quanyi_data('LUDch6','IF',1)
# pre_quanyi_data('LUDch8','IF',0)