#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import csv
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


path=r"D:\DATA\daynight\RB.csv"
targetfile1=r"D:\DATA\datasplit\RBdaynight_201001_201412.csv"
targetfile4=r"D:\DATA\datasplit\RBdaynight_201412_201612.csv"

# path=r"D:\DATA\day\RB.csv"
# targetfile1=r"D:\DATA\datasplit\RBday_201001_201412.csv"
# targetfile4=r"D:\DATA\datasplit\RBday_201412_201612.csv"

with open(path,"rb" ) as f:
	reader=csv.reader(f)
	with open(targetfile1,'wb') as t:
		for row in reader:
			if int(row[0])>=20100101 and int(row[0])<=20141231:
				spamwriter = csv.writer(t)
				spamwriter.writerow(row)
	t.close()
f.close

with open(path,"rb" ) as f:
	reader=csv.reader(f)
	with open(targetfile4,'wb') as t:
		for row in reader:
			if int(row[0])>=20141201 and int(row[0])<=20161201:
				spamwriter = csv.writer(t)
				spamwriter.writerow(row)
	t.close()
f.close

