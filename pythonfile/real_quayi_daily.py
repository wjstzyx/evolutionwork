#coding=utf-8 
#!/usr/bin/env python
###检测real_st_report 和P_LOG 的联合记录是否连续

import sys
import threading
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from real_st_report")
# print resList

def myround(num):
	if num>=0:
		return round(num)
	if num<=0:
		return round(num+0.000000001)


def main_calculate(symbol,ac):
	pointvalue={'IF':300,'CU':5,'RB':10,'AG':15,'IC':200,'RU':10,'TA':5}
	#commvalue={'IF':60,'CU':50,'RB':10,'AG':20,'IC':60,'RU':50,'TA':10}
	commvalue={'IF':60,'CU':20,'RB':10,'AG':8,'IC':60,'RU':20,'TA':10}
	tablename="#realtempinfo_%s" % (ac)
	# tablename='tempquanyiinfo'
	try:		
		sql="drop table %s" % (tablename)
		ms.insert_sql(sql)
	except:
		pass
	sql="select deltaposition,0 as position,C,0 as deltaquanyi,0 as comm, D,stockdate into %s from (select ISNULL(b.position,0) AS deltaposition ,a.StockDate,a.C,a.D from TSymbol a left outer join [real_quanyi_log_groupby] b on a.Symbol=b.symbol  and b.symbol='%s' and b.type=0  and b.ac='%s' and a.StockDate=b.stockdate where a.Symbol='%s' ) temp " % (tablename,symbol,ac,symbol)
	# sql="insert into tempquanyiinfo select deltaposition,0 as position,C,0 as deltaquayi,0 as comm, D,stockdate from (select ISNULL(b.position,0) AS deltaposition ,a.StockDate,a.C,a.D from TSymbol a left outer join [real_quanyi_log_groupby] b on a.Symbol=b.symbol  and b.symbol='%s' and b.type=0  and b.ac='%s' and a.StockDate=b.stockdate where a.Symbol='%s' ) temp " % (symbol,ac,symbol)
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
	sql="select max(D) from real_dailyquanyi where ac='%s' and symbol='%s'" % (ac,symbol)
	lastrecordday=ms.find_sql(sql)[0][0]
	for item in res[1:]:
		C=item['C']
		D=item['D']
		tempD=D[2:4]+D[5:7]+D[8:10]
		deltaposition=item['deltaposition']
		##开始计算
		deltaquanyi=myround(position)*float((C-lastClose))*float(pointvalue[symbol])
		# if tempD>160615:
		# 	print item['stockdate']
		# 	print 'deltaquanyi',deltaquanyi
		# 	print 'myround(position)',myround(position)
		# 	print 'float((C-lastClose))',float((C-lastClose))
		# 	print 'float(pointvalue[symbol])',float(pointvalue[symbol])
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
				sql="insert into real_dailyquanyi(ac,symbol,position,quanyi,comm,D,d_max,times) values('%s','%s',%s,%s,%s,%s,%s,%s)" % (ac,symbol,myround(position),lastdayquanyi,lastdaycomm,changeD,d_max,times)
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
		sql="select top 1 d fROM TSymbol ORDER BY id desc"
		refD=ms.find_sql(sql)[0][0]
		refD=refD[2:4]+refD[5:7]+refD[8:10]
		if newD==refD:
			sql="insert into real_dailyquanyi(ac,symbol,position,quanyi,comm,D,d_max,times) values('%s','%s',%s,%s,%s,%s,%s,%s)" % (ac,symbol,myround(position),lastdayquanyi,lastdaycomm,newD,d_max,times)
			ms.insert_sql(sql)


		# if tempD=='160523' and deltaposition!=0:
		# 	print item['stockdate'],'   ',lastdayquanyi,'   ',lastdaycomm,'   ',position
	try:		
		sql="drop table %s" % (tablename)
		ms.insert_sql(sql)
	except:
		pass




def main_calculate_distinc(symbolfrom,symbolto,ac):
	pointvalue={'IF':300,'CU':5,'RB':10,'AG':15,'IC':200,'RU':10,'TA':5}
	#commvalue={'IF':60,'CU':50,'RB':10,'AG':20,'IC':60,'RU':50,'TA':10}
	commvalue={'IF':60,'CU':20,'RB':10,'AG':8,'IC':60,'RU':20,'TA':10}
	tablename="#realtempinfo_%s" % (ac)
	# tablename='tempquanyiinfo'
	try:		
		sql="drop table %s" % (tablename)
		ms.insert_sql(sql)
	except:
		pass
	sql="select deltaposition,0 as position,C,0 as deltaquanyi,0 as comm, D,stockdate into %s from (select ISNULL(b.position,0) AS deltaposition ,a.StockDate,a.C,a.D from TSymbol a left outer join [real_quanyi_log_groupby] b on a.Symbol='%s'  and b.symbol='%s' and b.type=0  and b.ac='%s' and a.StockDate=b.stockdate where a.Symbol='%s' ) temp " % (tablename,symbolto,symbolfrom,ac,symbolto)
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
	sql="select max(D) from real_dailyquanyi where ac='%s' and symbol='%s'" % (ac,symbolto)
	lastrecordday=ms.find_sql(sql)[0][0]
	for item in res[1:]:
		C=item['C']
		D=item['D']
		tempD=D[2:4]+D[5:7]+D[8:10]
		deltaposition=item['deltaposition']
		##开始计算
		deltaquanyi=myround(position)*float((C-lastClose))*float(pointvalue[symbolto])
		comm=abs(myround(position+deltaposition)-myround(position))*commvalue[symbolto]
		times=times+abs(myround(position+deltaposition)-myround(position))
		if changeD!=tempD:
			print lastrecordday,changeD
			#每天第一根
			if changeD>lastrecordday:
				sql="SELECT round(sum(p_size*ratio/100),0) FROM p_log where type=1 and st<>123456 and ac='%s' and symbol='%s' and d=%s" % (ac,symbolfrom,changeD)
				d_max=ms.find_sql(sql)[0][0]
				if d_max is None or d_max==0:
					d_max=0.0001
				sql="insert into real_dailyquanyi(ac,symbol,position,quanyi,comm,D,d_max,times) values('%s','%s',%s,%s,%s,%s,%s,%s)" % (ac,symbolto,myround(position),lastdayquanyi,lastdaycomm,changeD,d_max,times)
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
	if newD>lastrecordday:
		sql="SELECT round(sum(p_size*ratio/100),0) FROM p_log where type=1 and st<>123456 and ac='%s' and symbol='%s' and d=%s" % (ac,symbolfrom,newD)
		d_max=ms.find_sql(sql)[0][0]
		if d_max is None or d_max==0:
			d_max=0.0001
		sql="select top 1 d fROM TSymbol ORDER BY id desc"
		refD=ms.find_sql(sql)[0][0]
		refD=refD[2:4]+refD[5:7]+refD[8:10]
		if newD==refD:
			sql="insert into real_dailyquanyi(ac,symbol,position,quanyi,comm,D,d_max,times) values('%s','%s',%s,%s,%s,%s,%s,%s)" % (ac,symbolto,myround(position),lastdayquanyi,lastdaycomm,newD,d_max,times)
			ms.insert_sql(sql)


	try:		
		sql="drop table %s" % (tablename)
		ms.insert_sql(sql)
	except:
		pass



def pre_data_for_ac(itemlist,symbol):
	i=0
	for item in itemlist:
		i=i+1
		ac=item
		print i,ac,symbol
		main_calculate(symbol,ac)


def pre_data_for_ac_distinc(itemlist,symbolfrom,symbolto):
	i=0
	for item in itemlist:
		i=i+1
		ac=item
		print i,ac,symbolto
		main_calculate_distinc(symbolfrom,symbolto,ac)



def main_pre_quanyi():
	i=0
	TAlist=('CH4tazs','DayBrTA','DayTALineRrate')
	RUlist=('RU2v7','RUDTA','RUMY','RUV4E','RUv4ehc','RUV7','RUWEEKLY')
	RBlist=('RBQGSTTR_TG','Rb_QGpLud','RbCX_QGRev','RbCX_QGtr','RB_CXVolume','RB_Daybreaker','RB_LiangtuPipei','RB_LRC_Trend','RB_LUD','RB_MT','RB_RBreaker','RB_RSI','RB_ST_Reversal','RB_ST_Trend','RB_VPIN','RB_ZhixianPipei','CH4RBZS','DAYGAPRB','RBHAL','RBPUD','RBSV','UDKRB','V7RB','RBQGstrev_TG','RBQGTR_TG')
	CUlist=('CUDUDHL','ESPcu','LKVCU1','LKVCU2','PUDCU','QCU18MIN','QPMCU','Vk2CU','CUVK3')
	AGlist=('9AGOLD','9AGVD05','9AGVD06','AGNEW4','AGNEW6','AGNEW8','AGNEW19','AGNEWLVO')
	IClist=('YEEXIC','YEOTIC','YETRIC','YEZHIC')
	IFlist=('9CPPUD','DayBrIF','9Distance','9DUD1','9DUDHL','9DUDRV','9EXR1410','9EXV1410','9FORCE','9FQS1','9HAL','9HAL2','9HAL3','9HALMA','9HUITIAO','9HUITIAO2','9HUITIAO3','9HUITIAO4','9KDHDAY','9KDHPM','9Linerate','9RATE','9MALONGK','9MiddayTrend','9MinVolPbuy','9MONDAY','9MORNINGOUT','9MT','9MVRATE','9NHL','9NOON','9OpenBet','9QMA','9QPMIF','9Reversal','9Reversal2','9Reversal3','9V4EIV','9VK1','9VK3','9VPINVOl_L','9VPINVOl_S','9VPINVOl_S2','9wb','9weipan','9WeipanREV','9WeipanStatics','9YAP01','9YY2','9YYMA','9LUD','9LUD2CH','9LUD3','9LUD4','9LUD5','9LUD6','9LUD7','9LUD8','9LUD10','9LUD11V2','9LUD13','9LUD14','9LUD16','LUDch1','LUDch4','LUDch5','LUDch6','LUDch8','LUD52015','LUD62015','LUD72015','LUD82015','TimeV2Pm','TimeV3DtaPm','TimeV3HLAm','TimeV3HLPm','V4EIVelements','V4EIVNEW','IFQG1310','IFQGEX','IFQGOT','9QGBombma2','IFQGTB','IFQGTR','IFQGWB','YEQGTR','YEQGEX','YEQGOT','YEQGZH211')
	ICIFlist=('YEQGEX','YEQGOT','YEQGTR')

	sql="select getdate()"
	res=ms.find_sql(sql)[0][0]
	res=res.strftime("%Y-%m-%d %H:%M:%S")
	newD=res[2:4]+res[5:7]+res[8:10]
	sql="delete from real_dailyquanyi where D=%s" % (newD)
	ms.insert_sql(sql)
	pre_data_for_ac(RBlist,'RB')
	pre_data_for_ac(CUlist,'CU')
	pre_data_for_ac(AGlist,'AG')
	pre_data_for_ac(IClist,'IC')
	pre_data_for_ac(IFlist,'IF')
	pre_data_for_ac(RUlist,'RU')
	pre_data_for_ac(TAlist,'TA')
	pre_data_for_ac_distinc(ICIFlist,'IF','IC')



# print "ddd"
# sql="select 1"
# res=ms.dict_sql(sql)
# print res
main_pre_quanyi()

# main_calculate('IF','9DUD1')
# input_temp_table('YEQGOT','IF',0,160615)
# pre_data_for_ac(['RU2v7'],'RU')

