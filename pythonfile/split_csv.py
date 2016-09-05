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
targetfile1=r"D:\DATA\datasplit\RB_201001_201212.csv"
targetfile2=r"D:\DATA\datasplit\RB_201301_201312.csv"
targetfile3=r"D:\DATA\datasplit\RB_201401_201412.csv"
targetfile4=r"D:\DATA\datasplit\RB_201501_201512.csv"
targetfile5=r"D:\DATA\datasplit\RB_201601_201612.csv"
with open(path,"rb" ) as f:
	reader=csv.reader(f)
	with open(targetfile5,'wb') as t:
		for row in reader:
			if int(row[0])<=20161231 and int(row[0])>=20160101:
				spamwriter = csv.writer(t)
				spamwriter.writerow(row)
			# if int(row[0])<=20131231 and int(row[0])>=20130101:
			# 	t2=open(targetfile2,'wb')
			# 	spamwriter = csv.writer(t2)
			# 	spamwriter.writerow(row)
			# if int(row[0])<=20141231 and int(row[0])>=20140101:
			# 	t3=open(targetfile3,'wb')
			# 	spamwriter = csv.writer(t3)
			# 	spamwriter.writerow(row)
			# if int(row[0])<=20151231 and int(row[0])>=20150101:
			# 	t4=open(targetfile4,'wb')
			# 	spamwriter = csv.writer(t4)
			# 	spamwriter.writerow(row)
			# if int(row[0])<=20161231 and int(row[0])>=20160101:
			# 	t5=open(targetfile5,'wb')
			# 	spamwriter = csv.writer(t5)
			# 	spamwriter.writerow(row)


