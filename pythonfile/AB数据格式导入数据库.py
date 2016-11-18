#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
import csv
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms03 = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-



def main_fun():
	fileroot=r'Y:\data_shiwei\20161021\1Min'
	symbol='OI'
	srcFilePath=fileroot+"\\"+'%s.csv' % (symbol)
	reader = csv.reader(file(srcFilePath,'rb'))
	for line in reader:
		line_write_in_database(symbol,line)





def line_write_in_database(symbol,line):
	stockdate=line[0]+" "+line[1]
	stockdate=datetime.datetime.strptime(stockdate,'%Y/%m/%d %H:%M')
	if stockdate>datetime.datetime.strptime('2015/01/01','%Y/%m/%d') and stockdate<datetime.datetime.strptime('2016/06/01','%Y/%m/%d'):
		sql="select 1 from [TSymbol_quotes_backup] where symbol='%s' and stockdate='%s'" % (symbol,stockdate)
		res=ms.dict_sql(sql)
		if not res:
			sql="insert into [Future].[dbo].[TSymbol_quotes_backup]([Symbol] ,[D] ,[T],[O] ,H ,[L] ,C,[V] ,[OPI] ,[StockDate] ,[refc]) values('%s','%s','%s',%s,%s,%s,%s,%s,%s,'%s',%s)" % (symbol,line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],stockdate,0)
			ms.insert_sql(sql)
		else:
			print 111

# line=['2016/03/22', '10:51', '1281.0', '1281.0', '1280.0', '1281.0', '920', '100952']
# line_write_in_database("symbol",line)
main_fun()



