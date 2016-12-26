#coding=utf-8 
#!/usr/bin/env python
import sys
import os
import csv
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-
root=r'C:\Users\YuYang\Desktop\20161107'
files=os.listdir(root)
for file in files:
	conid=file.split('.csv')[0].split('_')[0]
	day=file.split('.csv')[0].split('_')[1]
	day=day[0:4]+'-'+day[4:6]+'-'+day[6:]
	csvfile = open(root+"\\"+file, 'rb')
	reader = csv.reader(csvfile)
	tempsql=""
	i=0
	for line in reader:
		datetime=day+' '+line[0]
		ask=line[1]
		askv=line[2]
		bid=line[3]
		bidv=line[4]
		lastp=line[5]
		cv=line[6]
		opi=line[7]
		sql="('%s','%s',%s,%s,%s,%s,%s,%s,%s)" % (conid,datetime,ask,askv,bid,bidv,lastp,cv,opi)
		tempsql=tempsql+','+sql
		i=i+1
		if i>=900:			
			tempsql=tempsql.strip(',')
			# tempsql=sql
			sql="insert into [LogRecord].[dbo].[Tick_data](conid,time,ask,askv,bid,bidv,lastp,cv,opi) values"+tempsql
			ms.insert_sql(sql)
			tempsql=""
		continue
	if len(tempsql)>=30:
		tempsql=tempsql.strip(',')
		# tempsql=sql
		sql="insert into [LogRecord].[dbo].[Tick_data](conid,time,ask,askv,bid,bidv,lastp,cv,opi) values"+tempsql
		ms.insert_sql(sql)
		tempsql=""


	    

	# csvfile.close() 

	# print conid,day