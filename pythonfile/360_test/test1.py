#coding=utf-8
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

def gere_datafile(starttime):
	sql="select distinct symbol from [TSymbol_ZL] order by symbol"
	res1=ms.dict_sql(sql)
	for symbol in res1:
		sql="select CONVERT(varchar(20),StockDate,111) as data, CONVERT(varchar(20),StockDate,8) as time,O,H,L,C,V,OPI from TSymbol_ZL where Symbol='%s' and stockdate>='%s'  order by StockDate" % (symbol['symbol'],starttime)
		rows=ms.dict_sql(sql)
		datafir=r'E:'+"\\ABautofile\\\datafile"
		import csv
		fieldnames = ['data', 'time', 'O', 'H', 'L', 'C', 'V', 'OPI']
		dict_writer = csv.DictWriter(file(datafir+'\\%s.csv' % (symbol['symbol']), 'wb'), fieldnames=fieldnames)
		# dict_writer.writerow(fieldnames)
		dict_writer.writerows(rows)


gere_datafile('2017-01-01')