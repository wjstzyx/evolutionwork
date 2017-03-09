#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import multiprocessing
from multiprocessing import Lock
#ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


def drop_replacate(res):
	reslist=[[round(item['P'],3),item['stockdate']] for item in res]
	lastvalue=reslist[0]
	res=[]
	res.append(lastvalue)
	for item in reslist:
		if item[0]<>lastvalue[0]:
			res.append(item)
		lastvalue=item
	return res 


def analysis_result(res,seocnds,nums):
	totalnum=[]
	for i in range(len(res)-nums):
		holdvalue=res[i:i+nums]
		#print "res["+str(i)+":"+str(i+nums)+"]"
		#print holdvalue
		delta=(holdvalue[-1][1]-holdvalue[0][1]).seconds
		#print 'delta',delta
		if delta<=seocnds:
			totalnum.append([holdvalue[0][1]])
	return len(totalnum),totalnum



def analysis_st(st):
	print st 
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	sql="select * from real_st_report where st='%s' order by stockdate,id" % (st)
	res=ms.dict_sql(sql)
	# drop replecate  return [[p,stockdate],[],[]]
	res=drop_replacate(res)
	(num60_3,content)=analysis_result(res,60,3)
	(num120_3, content) = analysis_result(res, 120, 3)
	(num120_4, content) = analysis_result(res, 120, 4)
	(num120_5, content) = analysis_result(res, 120, 5)
	aa= [st,num60_3,num120_3,num120_4,num120_5]
	sql = "insert into [LogRecord].[dbo].[st_shandan_analysis](st,[s60_3],[s120_3],[s120_4],[s120_5]) values('%s',%s,%s,%s,%s);" % (aa[0], aa[1], aa[2], aa[3], aa[4])
	ms.insert_sql(sql)



if __name__ == "__main__":
	threads_N = 6
	lock = Lock()
	multiprocessing.freeze_support()
	pool = multiprocessing.Pool(processes=threads_N)
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	sql = "select distinct st from real_st_report order by st"
	res1 = ms.dict_sql(sql)
	for item in res1:
		st = item['st']
		# add process to pool
		if threads_N > 1:
			#print multiprocessing.current_process().name
			pool.apply_async(analysis_st, (st,))
		else:
			analysis_st(st)

	print "Process Pool Closed, Waiting for sub Process Finishing..."
	pool.close()
	pool.join()

	print 'Finished'




