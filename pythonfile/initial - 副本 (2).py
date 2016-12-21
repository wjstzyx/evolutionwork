#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

print datetime.datetime.now()
sql="select distinct symbol from TSymbol_quotes_backup"
res=ms.dict_sql(sql)
for item in res:
	print item['symbol'] 
	sql="select * from (select top(30000) * from TSymbol_quotes_backup where symbol='%s' order by stockdate desc ) a order by stockdate" % (item['symbol'])
	res1=ms.dict_sql(sql)

print datetime.datetime.now()

print '*******************************'

print datetime.datetime.now()
sql="select distinct symbol from TSymbol_quotes_backup"
res=ms.dict_sql(sql)
for item in res:
	print item['symbol'] 
	sql="select * from (select top 30000 o,h,l,c,v,opi,CONVERT(CHAR(8),stockdate, 112 )as date,CONVERT(CHAR(8),stockdate, 8 )as time from [Future].[dbo].[TSymbol_quotes_backup] where Symbol='%s'  order by StockDate  desc) a order by stockdate" % (item['symbol'])
	res1=ms.dict_sql(sql)

print datetime.datetime.now()