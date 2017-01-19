#coding=utf-8 
#!/usr/bin/env python
import os
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")

# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

root1=r'C:\Users\YuYang\Documents\Tencent Files\794513386\FileRecv\data-qd\future_index_1m_2'

files=os.listdir(root1)
for item in files:
	print item 
	symbol=item.split('.csv')[0].split('_zs')[0]
	symbol=symbol.upper()

	content=csv.reader(open(root1+"\\"+item))
	str1="insert into [TSymbol_allfuture]([Symbol]  ,[O]   ,[C]   ,[H]   ,[L]   ,[V]   ,[OPI]   ,[D]   ,[T]  ,[StockDate]) values"
	totalstr=""
	i=0
	for row in content:
		if row[0]>='20161011' and row[0]<='20161229':
			D=row[0][0:4]+"/"+row[0][4:6]+"/"+row[0][6:]
			T=row[1][0:2]+":"+row[1][2:4]
			stockdate=D+" "+T
			temp="('%s',%s,%s,%s,%s,%s,%s,'%s','%s','%s')" % (symbol,row[2],row[5],row[3],row[4],row[6],row[7],D,T,stockdate)
			totalstr=totalstr+","+temp
			i=i+1
			if i>900:
				totalstr=totalstr.strip(",")
				totalstr=str1+totalstr
				ms.insert_sql(totalstr)
				totalstr=""
				i=0
	if len(totalstr)>20:
		totalstr=totalstr.strip(",")
		totalstr=str1+totalstr
		ms.insert_sql(totalstr)
		totalstr=""	
