#coding=utf-8
#!/usr/bin/env python
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import os
import datetime
import multiprocessing

ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-
symbolList = ['A','AG','AL','AU','BU','C','CF','CS','CU','FG','HC','I','J','JD','JM','L','M','MA','NI','OI','p','PP','RB','RM','RU','SR','TA','YY','ZC','ZN']


def gere_datafile(symbol,starttime,dataroot,datatype):
	if datatype=='day':
		sql = "select CONVERT(varchar(20),StockDate,111) as data, CONVERT(varchar(20),StockDate,8) as time,O,H,L,C,V,OPI from TSymbol_quotes_backup where Symbol='%s' and stockdate>='%s'  order by StockDate" % (symbol, starttime)
	else:
		sql = "select CONVERT(varchar(20),StockDate,111) as data, CONVERT(varchar(20),StockDate,8) as time,O,H,L,C,V,OPI from TSymbol_allfuture where Symbol='%s' and stockdate>='%s'  order by StockDate" % (symbol, starttime)
	rows = ms.dict_sql(sql)
	datafir = dataroot + "\\ABautofile\\\datafile"
	fieldnames = ['data', 'time', 'O', 'H', 'L', 'C', 'V', 'OPI']
	dict_writer = csv.DictWriter(file(datafir + '\\%s.csv' % (symbol), 'wb'), fieldnames=fieldnames)
	# dict_writer.writerow(fieldnames)
	dict_writer.writerows(rows)
	print "%s get_data finished" % (symbol)




if __name__ == "__main__":
	a=datetime.datetime.now()
	multiprocessing.freeze_support()

	threads_N = 10
	starttime='2015-01-01'
	dataroot=r'E:'
	datatype='day'
	#datatype=sys.argv[1]
	#datatype='daynight'
	pool = multiprocessing.Pool(processes=threads_N)
	for symbol in symbolList:
		if threads_N > 1:
			pool.apply_async(gere_datafile, (symbol,starttime,dataroot,datatype,))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
		else:
			gere_datafile(symbol,starttime,dataroot,datatype)

	print "Process Pool Closed, Waiting for sub Process Finishing..."
	pool.close()
	pool.join()

	print 'Finished'

	print "start Analysis"
	print 'spend time:',datetime.datetime.now()-a