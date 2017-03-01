#coding=utf-8
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import os
import re
import pandas as pd
import numpy as np
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-
def bulk_insert(tablename,valuelist,columns):
	columns=','.join(columns)
	totalsql=""
	for item in valuelist:
		atr=['%s' % i for i in item]
		value="','".join(atr)
		value="'"+value+"'"
		sql1="insert into %s(%s) values(%s);" % (tablename,columns,value)
		totalsql=totalsql+sql1
	if len(totalsql)>20:
		ms.insert_sql(totalsql)


root=r'E:\ABautofile\aflfile'
filelist=os.listdir(root)
totallist=[]
for item in filelist:
	symbol=item.split('-')[1]
	sql="select s_id from symbol_id where symbol='%s'" % (symbol)
	s_id=ms.dict_sql(sql)[0]['s_id']
	f=open(root+"\\"+item)
	read=f.read()
	apttern=r'StrategyID = "(.*)";'
	match=re.search(apttern,read)
	ac='20170228_'+symbol.upper()
	alist=[ac,s_id,match.group(1),1,1]
	totallist.append(alist)


bulk_insert('P_BASIC_test',totallist,['AC','STOCK','ST','P_size','type'])






