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

def myround(num):
	if num>=0:
		return round(num)
	if num<=0:
		return round(num+0.000000001)

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
	sql="select top 1 * from [quanyi_log_groupby] where AC='%s' AND Symbol='%s' and TYPE=%s order by stockdate desc " % (ac,symbol,type)
	res=ms.dict_sql(sql)
	if not res:
		sql="insert into [quanyi_log_groupby]  select '%s','%s',%s,SUM((P-PP)*p_size*ratio/100) as position,stockdate from ##temp_quanyi where AC='%s' AND Symbol='%s' and TYPE=%s and p is not null group by stockdate order by stockdate" % (ac,symbol,type,ac,symbol,type)
		ms.insert_sql(sql)
	else:
		laststockdate=res[0]['stockdate']
		sql="insert into [quanyi_log_groupby]  select '%s','%s',%s,SUM((P-PP)*p_size*ratio/100) as position,stockdate from ##temp_quanyi where AC='%s' AND Symbol='%s' and TYPE=%s and p is not null and StockDate>'%s'  group by stockdate order by stockdate" % (ac,symbol,type,ac,symbol,type,laststockdate)
		print sql
		ms.insert_sql(sql)
	sql="drop table ##temp_quanyi"
	ms.insert_sql(sql)
	print "OK"




def main_calculate(symbol,ac):
	pointvalue={'IF':300,'CU':5,'RB':10,'AG':15,'IC':200,'RU':10,'TA':5}
	#commvalue={'IF':60,'CU':50,'RB':10,'AG':20,'IC':60,'RU':50,'TA':10}
	commvalue={'IF':60,'CU':20,'RB':10,'AG':8,'IC':60,'RU':20,'TA':10}
	tablename="#tempinfo_%s" % (ac)
	# tablename='tempquanyiinfo'
	try:		
		sql="drop table %s" % (tablename)
		ms.insert_sql(sql)
	except:
		pass
	sql="select deltaposition,0 as position,C,0 as deltaquanyi,0 as comm, D,stockdate into %s from (select ISNULL(b.position,0) AS deltaposition ,a.StockDate,a.C,a.D from TSymbol a left outer join [quanyi_log_groupby] b on a.Symbol=b.symbol  and b.symbol='%s' and b.type=0  and b.ac='%s' and a.StockDate=b.stockdate where a.Symbol='%s' ) temp " % (tablename,symbol,ac,symbol)
	# sql="insert into tempquanyiinfo select deltaposition,0 as position,C,0 as deltaquayi,0 as comm, D,stockdate from (select ISNULL(b.position,0) AS deltaposition ,a.StockDate,a.C,a.D from TSymbol a left outer join [quanyi_log_groupby] b on a.Symbol=b.symbol  and b.symbol='%s' and b.type=0  and b.ac='%s' and a.StockDate=b.stockdate where a.Symbol='%s' ) temp " % (symbol,ac,symbol)
	# print sql
	ms.insert_sql(sql)
	sql="select * from %s order by stockdate" % (tablename)
	res=ms.dict_sql(sql)
	# print res[1]
	lastposition=0
	lastClose=res[0]['C']
	position=res[0]['deltaposition']
	changeD=0
	lastdaypostiion=0
	lastdayquanyi=0
	lastdaycomm=0
	times=0
	sql="select max(D) from dailyquanyi where ac='%s' and symbol='%s'" % (ac,symbol)
	lastrecordday=ms.find_sql(sql)[0][0]
	for item in res[1:]:
		C=item['C']
		D=item['D']
		tempD=D[2:4]+D[5:7]+D[8:10]
		deltaposition=item['deltaposition']
		##开始计算
		deltaquanyi=myround(position)*float((C-lastClose))*float(pointvalue[symbol])
		comm=abs(myround(position+deltaposition)-myround(position))*commvalue[symbol]
		times=times+abs(myround(position+deltaposition)-myround(position))
		if changeD!=tempD:
			print lastrecordday,changeD
			#每天第一根
			if changeD>lastrecordday:
				sql="SELECT round(sum(p_size*ratio/100),0) FROM p_log where type=1 and st<>123456 and ac='%s' and symbol='%s' and d=%s" % (ac,symbol,changeD)
				d_max=ms.find_sql(sql)[0][0]
				if d_max is None or d_max==0:
					d_max=0.0001
				sql="insert into dailyquanyi(ac,symbol,position,quanyi,comm,D,d_max,times) values('%s','%s',%s,%s,%s,%s,%s,%s)" % (ac,symbol,myround(position),lastdayquanyi,lastdaycomm,changeD,d_max,times)
				# print sql
				ms.insert_sql(sql)
			changeD=tempD
			lastdayquanyi=0
			lastdaycomm=0
			times=0
		lastdayquanyi=lastdayquanyi+deltaquanyi
		lastdaycomm=lastdaycomm+comm
		position=position+deltaposition
		lastClose=C
	sql="select getdate()"
	res=ms.find_sql(sql)[0][0]
	res=res.strftime("%Y-%m-%d %H:%M:%S")
	newD=res[2:4]+res[5:7]+res[8:10]
	print newD
	if newD>lastrecordday:
		sql="SELECT round(sum(p_size*ratio/100),0) FROM p_log where type=1 and st<>123456 and ac='%s' and symbol='%s' and d=%s" % (ac,symbol,newD)
		d_max=ms.find_sql(sql)[0][0]
		if d_max is None or d_max==0:
			d_max=0.0001
		sql="insert into dailyquanyi(ac,symbol,position,quanyi,comm,D,d_max,times) values('%s','%s',%s,%s,%s,%s,%s,%s)" % (ac,symbol,myround(position),lastdayquanyi,lastdaycomm,newD,d_max,times)
		ms.insert_sql(sql)

		# if tempD=='160523' and deltaposition!=0:
		# 	print item['stockdate'],'   ',lastdayquanyi,'   ',lastdaycomm,'   ',position
	try:		
		sql="drop table %s" % (tablename)
		ms.insert_sql(sql)
	except:
		pass

# main_calculate(symbol,ac)







def pre_quanyi_data(ac,symbol,type):
	input_temp_table(ac,symbol,type)



def pre_data_for_ac(itemlist,symbol):
	i=0
	for item in itemlist:
		i=i+1
		ac=item
		print i,ac,symbol
		pre_quanyi_data(ac,symbol,0)
		# pre_quanyi_data(ac,symbol,1)
		main_calculate(symbol,ac)




def main_pre_quanyi():
	i=0
	TAlist=('CH4tazs','DayBrTA','DayTALineRrate')
	RUlist=('RUDTA','RUMY','RUV4E','RUv4ehc','RUV7','RUWEEKLY')
	RBlist=('Rb_QGpLud','RbCX_QGRev','RbCX_QGtr','RB_CXVolume','RB_Daybreaker','RB_LiangtuPipei','RB_LRC_Trend','RB_LUD','RB_MT','RB_RBreaker','RB_RSI','RB_ST_Reversal','RB_ST_Trend','RB_VPIN','RB_ZhixianPipei','CH4RBZS','DAYGAPRB','RBHAL','RBPUD','RBSV','UDKRB','V7RB','RBQGstrev_TG','RBQGTR_TG')
	CUlist=('CUDUDHL','ESPcu','LKVCU1','LKVCU2','PUDCU','QCU18MIN','QPMCU','Vk2CU','CUVK3')
	AGlist=('9AGOLD','9AGVD05','9AGVD06','AGNEW4','AGNEW6','AGNEW8','AGNEW19','AGNEWLVO')
	IClist=('YEEXIC','YEOTIC','YETRIC','YEZHIC')
	IFlist=('9CPPUD','DayBrIF','9Distance','9DUD1','9DUDHL','9DUDRV','9EXR1410','9EXV1410','9FORCE','9FQS1','9HAL','9HAL2','9HAL3','9HALMA','9HUITIAO','9HUITIAO2','9HUITIAO3','9HUITIAO4','9KDHDAY','9KDHPM','9Linerate','9RATE','9MALONGK','9MiddayTrend','9MinVolPbuy','9MONDAY','9MORNINGOUT','9MT','9MVRATE','9NHL','9NOON','9OpenBet','9QMA','9QPMIF','9Reversal','9Reversal2','9Reversal3','9V4EIV','9VK1','9VK3','9VPINVOl_L','9VPINVOl_S','9VPINVOl_S2','9wb','9weipan','9WeipanREV','9WeipanStatics','9YAP01','9YY2','9YYMA','9LUD','9LUD2CH','9LUD3','9LUD4','9LUD5','9LUD6','9LUD7','9LUD8','9LUD10','9LUD11V2','9LUD13','9LUD14','9LUD16','LUDch1','LUDch4','LUDch5','LUDch6','LUDch8','LUD52015','LUD62015','LUD72015','LUD82015','TimeV2Pm','TimeV3DtaPm','TimeV3HLAm','TimeV3HLPm','V4EIVelements','V4EIVNEW','IFQG1310','IFQGEX','IFQGOT','9QGBombma2','IFQGTB','IFQGTR','IFQGWB','YEQGTR','YEQGEX','YEQGOT','YEQGZH211')

	pre_data_for_ac(RBlist,'RB')
	pre_data_for_ac(CUlist,'CU')
	pre_data_for_ac(AGlist,'AG')
	pre_data_for_ac(IClist,'IC')
	pre_data_for_ac(IFlist,'IF')
	pre_data_for_ac(RUlist,'RU')
	pre_data_for_ac(TAlist,'TA')



# print "ddd"
# sql="select 1"
# res=ms.dict_sql(sql)
# print res
main_pre_quanyi()
# pre_data_for_ac(['RBQGstrev_TG','RBQGTR_TG'],'RB')

