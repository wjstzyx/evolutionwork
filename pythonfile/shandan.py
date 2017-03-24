#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
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
		days=(holdvalue[-1][1]-holdvalue[0][1]).days
		#print 'delta',delta
		if delta<=seocnds and holdvalue[-1][0]==holdvalue[0][0] and days==0:
			totalnum.append('['+holdvalue[0][1].strftime('%Y-%m-%d %H:%M')+']')
	return len(totalnum),totalnum



def analysis_st(st,period):
	print st 
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	nowday=datetime.datetime.now().strftime('%y%m%d')
	nowday=int(nowday)
	sql="select * from real_st_report where st='%s'  and D>='%s' order by stockdate,id" % (st,nowday)
	res=ms.dict_sql(sql)
	# drop replecate  return [[p,stockdate],[],[]]
	res=drop_replacate(res)
	(num60_3,content)=analysis_result(res,60,3)
	contentstr=','.join(content[:5])
	contentstr=contentstr[:800]
	print contentstr
	(num120_3, content) = analysis_result(res, 120, 3)
	(num120_4, content) = analysis_result(res, 120, 4)
	(num120_5, content) = analysis_result(res, 120, 5)
	aa= [st,num60_3,num120_3,num120_4,num120_5]
	if aa<>[st,0,0,0,0]:
		sql = "insert into [LogRecord].[dbo].[st_shandan_analysis](st,[s60_3],[s120_3],[s120_4],[s120_5],s60_content,[period]) values('%s',%s,%s,%s,%s,'%s','%s');" % (aa[0], aa[1], aa[2], aa[3], aa[4],contentstr,period)
		ms.insert_sql(sql)





if __name__ == "__main__":
	threads_N = 8
	lock = Lock()
	multiprocessing.freeze_support()
	pool = multiprocessing.Pool(processes=threads_N)
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	sql="truncate table [LogRecord].[dbo].[st_shandan_analysis]"
	ms.insert_sql(sql)
	#sql = "select distinct st from real_st_report  where st in (SELECT distinct st  FROM [LogRecord].[dbo].[_del_temp_acname_in_use] a inner join P_BASIC p   on a.acanme=p.AC ) order by st"
	sql="select a.st,b.period from ( select distinct st from real_st_report  where st in (  SELECT distinct st  FROM [LogRecord].[dbo].[_del_temp_acname_in_use] a inner join P_BASIC p   on a.acanme=p.AC ) ) a inner join LogRecord.dbo.ST_heart b on a.ST=b.st order by st"
	res1 = ms.dict_sql(sql)
	for item in res1:
		st = item['st']
		period=item['period']
		# add process to pool
		if threads_N > 1:
			#print multiprocessing.current_process().name
			pool.apply_async(analysis_st, (st,period,))
		else:
			analysis_st(st,period)

	print "Process Pool Closed, Waiting for sub Process Finishing..."
	pool.close()
	pool.join()

	print 'Finished'




