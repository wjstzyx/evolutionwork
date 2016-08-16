# -*- coding: utf-8 -*- 
import string, os
import csv
import time
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
aa=datetime.datetime(2016,8,9,22,24,20)
bb=datetime.datetime(2016,8,9,22,24,16,997000)
print aa
print bb
print aa.hour




def add_time_series(totalquanyi,res1):
	totalquanyitime=[k[0] for k in totalquanyi]
	res1time=[k[0] for k in res1]
	totalquanyidict={}
	for item in totalquanyi:
		totalquanyidict[item[0]]=item[1]
	res1dict={}
	for item in res1:
		res1dict[item[0]]=item[1]
	daylist=list(set(totalquanyitime).union(set(res1time)))
	daylist=sorted(daylist)
	totalquanyilastvalue=0
	res1lastvalues=0
	result={}
	for item in daylist:
		tempvalue=0
		if item in totalquanyitime:
			totalquanyilastvalue=totalquanyidict[item]
		if item in res1time:
			res1lastvalues=res1dict[item]
		tempvalue=totalquanyilastvalue+res1lastvalues
		result[item]=tempvalue
	result=sorted(result.iteritems(), key=lambda d:d[1], reverse = False)
	print result
	return result

totalquanyi=[("a11",1),("a13",2),("a15",3)]
res1=[("a12",10),("a13",20),("a14",300)]
kkk=add_time_series(totalquanyi,res1)
add_time_series(kkk,res1)