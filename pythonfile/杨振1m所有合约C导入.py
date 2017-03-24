#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import csv
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


dateroot=r'Y:\data_yangzhen\to_huangcheng\future_all'
filename='1m_20170201.csv'

with open(dateroot+"\\"+filename) as fh:
	content=csv.reader(fh)
	totalsql=""
	i=0
	for row in content:
		i=i+1
		stockdate=datetime.datetime.strptime(row[1],'%Y%m%d%H%M%S')
		sql="insert into [LogRecord].[dbo].[every_con_close]([con] ,[stockdate]   ,[C]) values('%s','%s',%s)" % (row[0],stockdate,row[2])
		totalsql=totalsql+sql
		if i>900:
			print i
			ms.insert_sql(totalsql)
			totalsql=""
			i=0
	if len(totalsql)>10:
		ms.insert_sql(totalsql)

