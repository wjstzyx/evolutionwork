#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
ms = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select 1")
# print resList
import csv
# -*- coding: utf-8 -*-

dateroot=r'D:\KT\_ExportData_\60'
symbol='SM'


def input_date(symbol,tablename):
	splittime='2017-03-16 00:00:00'
	splittime=datetime.datetime.strptime(splittime,'%Y-%m-%d %H:%M:%S')
	if tablename=='Tsymbol':
		sql="delete from %s where symbol='%s' and StockDate<='%s'" % (tablename,symbol,splittime)
		ms.insert_sql(sql)
		sql="delete from TSymbol_quotes_backup where symbol='%s' and StockDate<='%s'" % (symbol,splittime)
		ms.insert_sql(sql)
	else:
		if tablename=='TSymbol_allfuture':
			sql="delete from %s where symbol='%s' and StockDate<='%s'" % (tablename,symbol,splittime)
			ms.insert_sql(sql)
		else:
			print 'Please input right Table Name'
			return 0
	totalsql=""
	realfile=dateroot+'\\'+symbol+'98.csv' #98 仓指
	with open(realfile, 'rb') as csvfile:
		spamreader = csv.reader(csvfile)
		i=0
		j=0
		for row in spamreader:
			#print row
			i=i+1
			if i>1:				 
				O=row[2]
				H=row[3]
				L=row[4]
				C=row[5]
				V=row[6]
				OPI=row[7]
				D=row[0]
				T=row[1]
				if len(T)<6:
					T='0'*(6-len(T))+T
				T=T[0:2]+':'+T[2:4]
				D=D[0:4]+'/'+D[4:6]+'/'+D[6:8]
				StockDate=datetime.datetime.strptime(D+' '+T,'%Y/%m/%d %H:%M')
				if StockDate<=splittime:
					sql="insert into %s ([Symbol]  ,[O]   ,[C]   ,[H]  ,[L]   ,[V]   ,[OPI]  ,[D]  ,[T]  ,[StockDate]  ,[refc] ) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',0);" % (tablename,symbol,O,C,H,L,V,OPI,D,T,StockDate)
					totalsql=totalsql+sql
					j=j+1
					if j>500:
						print j
						ms.insert_sql(totalsql)
						totalsql=""
						j=0
		if len(totalsql)>10:
			ms.insert_sql(totalsql)





input_date('SM','TSymbol_allfuture')
