#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
import pandas as pd
import numpy as np
import time
import os
import csv
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

#删除已有信息,20s后进行
# delcmd = "del /s C:\\_wenhua_\\wh6all\\Data\\*00*.dat"
# os.system(delcmd)
# time.sleep(20)

def write_to_database(tablename,lastquotes,n,isday):
	#Date  0,Time1,Open2,High3,Low4,Close5,Volume6,OpenInterest7,SettlementPrice
	#rint "begin "+str(n)+" "+datetime.datetime.now().strftime('%H:%M:%S')
	insertdate=lastquotes
	ispass=0
	numtime=int(insertdate[1][0:2]+insertdate[1][3:5])
	if isday==1 and numtime>=800 and numtime<=1600:
		ispass=1
	if isday==0 and (numtime>=2050 or numtime<=300):
		ispass=1
	if ispass==1:
		Date=insertdate[0]
		stockdate=Date[0:4]+'-'+Date[4:6]+'-'+Date[6:9]+' '+insertdate[1]
		Date=Date[0:4]+'/'+Date[4:6]+'/'+Date[6:9]
		Time=insertdate[1][0:5]
		Open=round(float(insertdate[2]),n)
		High=round(float(insertdate[3]),n)
		Low=round(float(insertdate[4]),n)
		Close=round(float(insertdate[5]),n)
		Volume=round(float(insertdate[6]),n)
		OpenInterest=round(float(insertdate[7]),n)
		sql="Insert_quotes '%s',%s,%s,%s,%s,%s,%s,'%s','%s','%s'" % (tablename,Open,Close,High,Low,Volume,OpenInterest,Date,Time,stockdate)
		print n,sql
		threads = []
		# threads.append(threading.Thread(target=insert_database,args=(sql,ms07,'07数据库')))
		threads.append(threading.Thread(target=insert_database,args=(sql,colud246,'246云数据库')))
		threads.append(threading.Thread(target=insert_database,args=(sql,ms03,'03数据库')))
		threads.append(threading.Thread(target=insert_database,args=(sql,ms,'05数据库')))
		for t in threads:
			t.setDaemon(True)
			t.start()
		for t in threads:
			t.join()




	#time.sleep(3*n)
	#print "end "+str(n)+" "+datetime.datetime.now().strftime('%H:%M:%S')



def read_to_datanbase(filepath,symbol):
	csvfile = file(filepath, 'rb')
	reader = csv.reader(csvfile)
	linelist=[]
	for line in reader:
		linelist.append(line)
	csvfile.close()
	#选择最近的一条记录
	sql=" SELECT max(StockDate) as stockdate FROM [Future].[dbo].[TSymbol_ZL] WHERE symbol='%s' " % (symbol)
	maxstockdate=ms.dict_sql(sql)[0]['stockdate']
	print symbol,'maxstockdate',maxstockdate
	if maxstockdate is None:
		maxstockdate='2015-01-01'
	else:
		maxstockdate=maxstockdate.strftime("%Y-%m-%d %H:%M:%S")

	beginsql = 'insert into[Future].[dbo].[TSymbol_ZL](O,C,H,L,V,OPI,D,T,StockDate,symbol) values'
	counti=0
	tempsql=""
	for insertdate in linelist[1:-1]:
		n=2
		Date = insertdate[0]
		stockdate = Date[0:4] + '-' + Date[4:6] + '-' + Date[6:9] + ' ' + insertdate[1]
		Date = Date[0:4] + '/' + Date[4:6] + '/' + Date[6:9]
		Time = insertdate[1][0:5]
		Open = round(float(insertdate[2]), n)
		High = round(float(insertdate[3]), n)
		Low = round(float(insertdate[4]), n)
		Close = round(float(insertdate[5]), n)
		Volume = round(float(insertdate[6]), n)
		OpenInterest = round(float(insertdate[7]), n)
		sql = "(%s,%s,%s,%s,%s,%s,'%s','%s','%s','%s')" % (Open, Close, High, Low, Volume, OpenInterest, Date, Time, stockdate,symbol)
		if stockdate>maxstockdate:
			tempsql=tempsql+','+sql
			counti=counti+1
		if counti>998:
			tempsql=tempsql.strip(',')
			sql=beginsql+tempsql
			ms.insert_sql(sql)
			tempsql=""
			counti=0
	tempsql = tempsql.strip(',')
	if len(tempsql)>10:
		sql = beginsql + tempsql
		ms.insert_sql(sql)








wenhuapath="C:\\_wenhua_\\wh6all"



sql="SELECT path,symbol FROM [LogRecord].[dbo].[catch_quotes_ZL] order by symbol "
res=ms.dict_sql(sql)
for item in res:
	filepath = wenhuapath + "\\data_out" + item['path']
	symbol = item['symbol']
	read_to_datanbase(filepath,symbol)




