#coding=utf-8 
#!/usr/bin/env python
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

##产生数据

##读取数据写入数据库
def read_date_write_to_database(targetfile,date):
	print "Starting..."
	file = open(targetfile)
	successnum=0
	while 1:
		lines = file.readlines(100000)
		if not lines:
			break
		for line in lines:
			line=line.strip('\n')
			linelist=line.split(',')
			if linelist[7]==date:
				sql="insert into Tsymbol ([Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc])values('%s',%s,%s,%s,%s,%s,%s,'%s','%s','%s',%s)" % (linelist[0],linelist[1],linelist[2],linelist[3],linelist[4],linelist[5],linelist[6],linelist[7],linelist[8],linelist[9],linelist[10])
				try:
					ms.insert_sql(sql)
					successnum=successnum+1
					print successnum
				except Exception,e:
					if "Cannot insert duplicate key row" in str(e):
						pass				
					else:
						break
	file.close()
	print "Finish"
	print "Success Insert Num :",successnum










targetfile=r'Y:\data_wenhua\20160427_0_2359.csv'
date='2016/04/27'
read_date_write_to_database(targetfile,date)
