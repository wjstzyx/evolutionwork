#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import numpy
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-
# 获取正在账号正在使用的所有虚拟组
def get_acname_in_use():
	total=set()
	totalsql=""
	sql="select distinct userid from LogRecord.dbo.account_position"
	res=ms.dict_sql(sql)
	for item in res:
		userid=item['userid']
		sql="WITH Emp AS   (SELECT AC,           F_ac,          ratio,          stock    FROM dbo.p_follow    WHERE (AC = '%s')      UNION ALL      SELECT d.AC,            d.F_ac,    d.ratio * Emp_3.ratio / 100.0 AS Expr1,         d.stock      FROM Emp AS Emp_3      INNER JOIN dbo.p_follow AS d ON d.AC = Emp_3.F_ac)  select * from Emp where F_ac not  in (select distinct ac from p_follow where ac is not null)" % (userid)
		res1=ms.dict_sql(sql)
		if res1:
			for item1 in res1:
				total.add((item1['F_ac'],item1['stock']))



	for item1 in total:
		sql="insert into LogRecord.dbo.[_del_temp_acname_in_use](acanme,stock) values('%s','%s');" % (item1[0],item1[1])
		totalsql=totalsql+sql
	ms.insert_sql(totalsql)


def drop_replacate(res):
	reslist=[[round(item['P'],2),item['stockdate']] for item in res]
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
			totalnum.append([holdvalue[0][1]])
	return len(totalnum),totalnum

# 将最近4个月 中出现次数>3 的 st 存入表中
def get_st_num():
	totalv=[]
	sql="select ss.* from [LogRecord].[dbo].st_shandan_analysis   ss inner join (select distinct st from [LogRecord].[dbo].[_del_temp_acname_in_use]  d inner join Future.dbo.P_BASIC p on d.acanme=p.AC) dd on ss.st=dd.ST where s60_3>4 order by s60_3 desc"
	res=ms.dict_sql(sql) #439
	#res=[{'st':'1012100190'}]
	for item in res:
		st=item['st']
		sql="select * from real_st_report where st='%s'  and  stockdate>='2016-12-01' order by stockdate,id" % (st)
		#print sql 
		res=ms.dict_sql(sql)
		#print len(res) 
		if res:
			res=drop_replacate(res)
			(num60_3,content)=analysis_result(res,60,3)
			if num60_3>3:
				print st,num60_3
				# for aaa in content:
				# 	print aaa
				totalv.append([st,num60_3])

	# for item in totalv:
	# 	sql="insert into [LogRecord].[dbo].[_del_temp_st_in_use2](st,num) values('%s','%s');" % (item[0],item[1])
	# 	ms.insert_sql(sql)

	# df1=pd.DataFrame(totalv,columns=['st','num'])
	# df1=df1.sort_values(['num'],ascending=False)

get_st_num()

# sql="SELECT zl,CONVERT(nvarchar(10),getdate(),120) as day  FROM [Future].[dbo].[symbol_id_zl] order by zl"
# res=ms.dict_sql(sql)
# #res=[{'zl':'a1705','day':'2017-03-13'},{},{}]