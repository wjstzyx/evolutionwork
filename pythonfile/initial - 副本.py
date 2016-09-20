#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

def all_file(numtpe):
	#get max StrategyID
	lenth1=len(numtpe)
	newnum=numtpe
	for i in range(10-lenth1):
		newnum=str(newnum)+'0'
	print 	numtpe,newnum
	sql="select top 1 max(st) as st from [LogRecord].[dbo].[all_st_list] where st like '%s%%'" % (numtpe)
	res=ms.dict_sql(sql)
	if res[0]['st'] is not None:
		StrategyID1=int(res[0]['st'])+1
	else:
		StrategyID1='no'
	sql="select top 1 max(st) as st from [Future].[dbo].[Trading_logSymbol] where st like '%s%%'" % (numtpe)
	res=ms.dict_sql(sql)
	if res[0]['st'] is not None:
		StrategyID2=int(res[0]['st'])+1
	else:
		StrategyID2='no'
	sql="select top 1 max(st) as st from [Future].[dbo].[P_BASIC] where st like '%s%%'" % (numtpe)
	res=ms.dict_sql(sql)
	if res[0]['st'] is not None:
		StrategyID3=int(res[0]['st'])+1
	else:
		StrategyID3='no'
	#get max
	if StrategyID1=='no' and StrategyID2=='no' and StrategyID3=='no':
		print "this is new stnum "
		if len(numtpe)==10:
			StrategyID=int(numtpe)
		else:
			print "error:Please input the right ST(length equals 10 )"
			exit()
	else:
		if StrategyID1=='no':
			StrategyID1=0
		if StrategyID2=='no':
			StrategyID2=0
		if StrategyID3=='no':
			StrategyID3=0
		StrategyID=max(StrategyID1,StrategyID2,StrategyID3)
		# if len(str(StrategyID))<8:
		# 	print "Find short lenth StrategyID %s" % (StrategyID)
		# 	print "Please input Number with more than 7 numbers"
		# 	exit()
	print StrategyID




numtpe='10122'
all_file(numtpe)