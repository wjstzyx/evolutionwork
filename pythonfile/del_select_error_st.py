#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import numpy as np
import pandas as pd
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import multiprocessing
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

def delete_mlti(st):
	print st
	sql="select id,round(p,6) as P,round(pp,6) as PP,st,stockdate from st_report where st='%s' order by  stockdate ,id" % (st)
	res=ms.dict_sql(sql)
	df1=pd.DataFrame(res)
	print 1
	df1['delta']=df1['P'].shift()-df1['PP']
	df2=df1[df1['delta']<>0]
	print 2



delete_mlti('1062100000')
exit()



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
