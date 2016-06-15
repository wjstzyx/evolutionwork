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

#将记录放入临时表(14秒)
def input_temp_table(ac,symbol,type,D):
	try:
		sql="drop table #real_quanyi_position"
		ms.insert_sql(sql)
	except:
		pass
	sql="select * into  #real_quanyi_position from (select '%s' as ac,'%s' as symbol,'%s' as type,temp.id,p,PP,p_size,ratio,st,o.stockdate from tsymbol o inner join (select real_st_report.id,real_st_report.p,real_st_report.pp,p.symbol,real_st_report.stockdate,real_st_report.st,p.p_size,p.ac,p.ratio,real_st_report.type from real_st_report  inner join p_log p on p.st=real_st_report.st and p.ac='%s' and p.symbol='%s' and p.d=%s and real_st_report.type=%s ) temp on temp.stockdate=o.stockdate and o.symbol=temp.symbol where o.symbol='%s' ) temp " % (ac,symbol,type,ac,symbol,D,type,symbol)
	ms.insert_sql(sql)
	##删除重复的项
	sql="delete from #real_quanyi_position where ID not in(select MAX(id) as id from #real_quanyi_position group by st,Stockdate)"
	ms.insert_sql(sql)

	##结束
	#如果有记录才进行
	sql="select count(1) from #real_quanyi_position"
	res=ms.find_sql(sql)[0][0]
	if res>0:
		sql="select top 1 totalposition,stockdate from [real_quanyi_log_groupby] where ac='%s' and symbol='%s' and TYPE=%s order by stockdate desc " % (ac,symbol,type)
		res=ms.dict_sql(sql)
		if res:
			lastP=res[0]['totalposition']
			laststockdate=res[0]['stockdate']
		else:
			lastP=0
			laststockdate='2010-01-01'
		tempD='20'+str(D)[0:2]+'/'+str(D)[2:4]+'/'+str(D)[4:6]
		sql="select distinct stockdate from Tsymbol where symbol='%s' and D='%s' and stockdate >'%s' order by stockdate " % (symbol,tempD,laststockdate)
		res=ms.find_sql(sql)
		sql="truncate table real_temp_position"
		ms.insert_sql(sql)
		for item in res:
			sql="select SUM(a.p*a.p_size*a.ratio/100) as P from #real_quanyi_position a inner join(  select MAX(StockDate) as stockdate,st from #real_quanyi_position where StockDate<='%s'  group by st  ) temp  on a.ST=temp.ST and a.StockDate=temp.stockdate" % (item[0])
			position=ms.find_sql(sql)[0][0]
			if position is None:
				position=0
			deltaposition=(position-lastP)
			lastP=position
			sql="insert into [real_temp_position](deltaposition,position,stockdate) values(%s,%s,'%s')" % (deltaposition,position,item[0])
			ms.insert_sql(sql)
		sql="insert into [real_quanyi_log_groupby] select '%s','%s',%s,deltaposition,stockdate,position from [real_temp_position] where deltaposition!=0 and stockdate>'%s'" % (ac,symbol,type,laststockdate)
		ms.insert_sql(sql)
	sql="drop table #real_quanyi_position"
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

# main_calculate(symbol,ac)


def main_calculate_distinc(symbolfrom,symbolto,ac):
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








def pre_quanyi_data(ac,symbol,type):
	sql="select (year(getdate())-2000)*10000+month(getdate())*100+day(getdate())"
	# print sql
	nowD=ms.find_sql(sql)[0][0]
	# print nowD
	# exit()
	sql="select distinct D from real_st_report where D=%s  order by D" % (nowD)
	sql="select distinct D from real_st_report  order by D"
	res=ms.dict_sql(sql)
	for item1 in res:
		print item1['D']
		input_temp_table(ac,symbol,type,item1['D'])



def pre_data_for_ac(itemlist,symbol):
	i=0
	for item in itemlist:
		i=i+1
		ac=item
		print i,ac,symbol
		pre_quanyi_data(ac,symbol,0)
		# pre_quanyi_data(ac,symbol,1)
		# main_calculate(symbol,ac)




def main_pre_quanyi():
	i=0
	TAlist=('CH4tazs','DayBrTA','DayTALineRrate')
	RUlist=('RUDTA','RUMY','RUV4E','RUv4ehc','RUV7','RUWEEKLY')
	RBlist=('Rb_QGpLud','RbCX_QGRev','RbCX_QGtr','RB_CXVolume','RB_Daybreaker','RB_LiangtuPipei','RB_LRC_Trend','RB_LUD','RB_MT','RB_RBreaker','RB_RSI','RB_ST_Reversal','RB_ST_Trend','RB_VPIN','RB_ZhixianPipei','CH4RBZS','DAYGAPRB','RBHAL','RBPUD','RBSV','UDKRB','V7RB','RBQGstrev_TG','RBQGTR_TG')
	CUlist=('CUDUDHL','ESPcu','LKVCU1','LKVCU2','PUDCU','QCU18MIN','QPMCU','Vk2CU','CUVK3')
	AGlist=('9AGOLD','9AGVD05','9AGVD06','AGNEW4','AGNEW6','AGNEW8','AGNEW19','AGNEWLVO')
	IClist=('YEEXIC','YEOTIC','YETRIC','YEZHIC')
	IFlist=('9CPPUD','DayBrIF','9Distance','9DUD1','9DUDHL','9DUDRV','9EXR1410','9EXV1410','9FORCE','9FQS1','9HAL','9HAL2','9HAL3','9HALMA','9HUITIAO','9HUITIAO2','9HUITIAO3','9HUITIAO4','9KDHDAY','9KDHPM','9Linerate','9RATE','9MALONGK','9MiddayTrend','9MinVolPbuy','9MONDAY','9MORNINGOUT','9MT','9MVRATE','9NHL','9NOON','9OpenBet','9QMA','9QPMIF','9Reversal','9Reversal2','9Reversal3','9V4EIV','9VK1','9VK3','9VPINVOl_L','9VPINVOl_S','9VPINVOl_S2','9wb','9weipan','9WeipanREV','9WeipanStatics','9YAP01','9YY2','9YYMA','9LUD','9LUD2CH','9LUD3','9LUD4','9LUD5','9LUD6','9LUD7','9LUD8','9LUD10','9LUD11V2','9LUD13','9LUD14','9LUD16','LUDch1','LUDch4','LUDch5','LUDch6','LUDch8','LUD52015','LUD62015','LUD72015','LUD82015','TimeV2Pm','TimeV3DtaPm','TimeV3HLAm','TimeV3HLPm','V4EIVelements','V4EIVNEW','IFQG1310','IFQGEX','IFQGOT','9QGBombma2','IFQGTB','IFQGTR','IFQGWB','YEQGTR','YEQGEX','YEQGOT','YEQGZH211')
	ICIFlist=('YEQGEX','YEQGOT','YEQGTR')

	# pre_data_for_ac(RBlist,'RB')
	# pre_data_for_ac(CUlist,'CU')
	# pre_data_for_ac(AGlist,'AG')
	# pre_data_for_ac(IClist,'IC')
	pre_data_for_ac(IFlist,'IF')
	# pre_data_for_ac(RUlist,'RU')
	# pre_data_for_ac(TAlist,'TA')
	# pre_data_for_ac_distinc(ICIFlist,'IF','IC')



# print "ddd"
# sql="select 1"
# res=ms.dict_sql(sql)
# print res
# main_pre_quanyi()
input_temp_table('YEQGOT','IF',0,160615)
# pre_data_for_ac(['RBQGstrev_TG','RBQGTR_TG'],'RB')

