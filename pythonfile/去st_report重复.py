#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import numpy as np
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import multiprocessing
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

def delete_mlti(st):
	print st
	sql="select id,round(p,6),round(pp,6),st,stockdate from st_report where st='%s' order by  stockdate desc,id desc" % (st)
	ares=ms.find_sql(sql)
	firstvalue=ares[0][1:]
	delvalue=[]
	for aitem in ares[1:]:
		if aitem[1:]==firstvalue:
			delvalue.append(str(aitem[0]))
		firstvalue=aitem[1:]
	mylenth=len(delvalue)
	print mylenth
	i=0
	while(1):
		temp=delvalue[5000*i:5000*i+5000]
		temp = ','.join(temp)
		if temp<>'':
			print st,i,[5000*i,5000*i+5000]
			sql = 'delete from st_report where id in (%s)' % (temp)
			ms.insert_sql(sql)
		i=i+1
		if 5000*i>mylenth:
			break



if __name__ == "__main__":
	multiprocessing.freeze_support()
	threads_N = 10
	pool = multiprocessing.Pool(processes=threads_N)
	sql = "select distinct st from st_report order by st"
	res = ms.dict_sql(sql)

	for item in res:
		if threads_N > 1:
			pool.apply_async(delete_mlti, (item['st'],))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
		else:
			delete_mlti(item['st'])

	print "Process Pool Closed, Waiting for sub Process Finishing..."
	pool.close()
	pool.join()

	print 'Finished'

	print "start Analysis"
