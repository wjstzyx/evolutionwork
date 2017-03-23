#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime 
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms08 = MSSQL(host="192.168.0.8",user="future",pwd="K@ra0Key",db="HF_Future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


#1 get tradeday_list
def get_tradeday_list():
	sql="select distinct replace(CONVERT(nvarchar,stockdate,102),'.','') as day from TSymbol where symbol='RB' and T<='21:00' and T>='09:00' order by  replace(CONVERT(nvarchar,stockdate,102),'.','') "
	datlist=ms.dict_sql(sql)
	datlist=[item['day'] for item in datlist]
	#print datlist
	return datlist





def update_orderlog():
	daylist=get_tradeday_list()
	sql="SELECT [id]   ,[InsertTime],[Databasetime]   FROM [HF_Future].[dbo].[orderlog] where RealDay='not_update'"
	res=ms08.dict_sql(sql)
	totalsql=""
	aa=0
	for item in res:
		myid=item['id']
		Databasetime=item['Databasetime']
		InsertTime=item['InsertTime']
		today=Databasetime.strftime('%Y%m%d')
		last_tradeday=[item for item in daylist if item<today ]
		last_tradeday=last_tradeday[-1]
		last_tradeday_nextday=datetime.datetime.strptime(last_tradeday,'%Y%m%d')+datetime.timedelta(days=1)
		last_tradeday_nextday=last_tradeday_nextday.strftime('%Y%m%d')

		if InsertTime>='08:00:00' and InsertTime<='15:30:00':
			sql="update [HF_Future].[dbo].[orderlog] set RealDay='%s' where id=%s" % (today,myid)
			ms08.insert_sql(sql)

		if InsertTime<'06:00:00' and InsertTime>='00:00:00':
			sql="update [HF_Future].[dbo].[orderlog] set RealDay='%s' where id=%s" % (last_tradeday_nextday,myid)
		if InsertTime>='20:00:00' and InsertTime<='23:59:59':
			sql="update [HF_Future].[dbo].[orderlog] set RealDay='%s' where id=%s" % (last_tradeday,myid)
		totalsql=totalsql+sql
		aa=aa+1
		if aa>400:
			print aa
			ms08.insert_sql(totalsql)
			totalsql=""
			aa=0
	if len(totalsql)>10:
		ms08.insert_sql(totalsql)

			#
print '#1'
update_orderlog()





def update_tradelog():
	daylist=get_tradeday_list()
	sql="SELECT [id]    ,[TradeTime]   ,[Databasetime]FROM [HF_Future].[dbo].[tradelog] where RealDay='not_update'"
	res=ms08.dict_sql(sql)
	totalsql=""
	aa=0
	for item in res:
		myid=item['id']
		Databasetime=item['Databasetime']
		InsertTime=item['TradeTime']
		today=Databasetime.strftime('%Y%m%d')
		last_tradeday=[item for item in daylist if item<today ]
		last_tradeday=last_tradeday[-1]
		last_tradeday_nextday=datetime.datetime.strptime(last_tradeday,'%Y%m%d')+datetime.timedelta(days=1)
		last_tradeday_nextday=last_tradeday_nextday.strftime('%Y%m%d')

		if InsertTime>='08:00:00' and InsertTime<='15:30:00':
			sql="update [HF_Future].[dbo].[tradelog] set RealDay='%s' where id=%s" % (today,myid)
			ms08.insert_sql(sql)

		if InsertTime<'06:00:00' and InsertTime>='00:00:00':
			sql="update [HF_Future].[dbo].[tradelog] set RealDay='%s' where id=%s" % (last_tradeday_nextday,myid)
		if InsertTime>='20:00:00' and InsertTime<='23:59:59':
			sql="update [HF_Future].[dbo].[tradelog] set RealDay='%s' where id=%s" % (last_tradeday,myid)
		totalsql=totalsql+sql
		aa=aa+1
		if aa>400:
			print aa
			ms08.insert_sql(totalsql)
			totalsql=""
			aa=0
	if len(totalsql)>10:
		ms08.insert_sql(totalsql)

			#
print '#2'
update_tradelog()