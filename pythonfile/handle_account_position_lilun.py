#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

def cal_distinct_position_lilun():
	#1 put lilun equity into account_position_lilun
	sql="truncate table [LogRecord].[dbo].account_position_lilun"
	ms.insert_sql(sql)
	sql="select distinct userid from [LogRecord].[dbo].[account_position] order by userid"
	res=ms.dict_sql(sql)
	totalsql=""
	for item in res:
		userid=item['userid']
		tempsql="select '%s' as [userID],STOCK as [stockID],Expr1 as position,GETDATE() as nowtime from future.dbo.view_%s" % (userid,userid)
		totalsql=totalsql+" union all "+tempsql
	totalsql=totalsql.strip(" union all ")
	totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) "+ totalsql
	ms.insert_sql(totalsql)

cal_distinct_position_lilun()


def show_distinct():
	nowday=datetime.datetime.now().strftime('%Y%m%d')
	sql=" select aaa.userID as realuserID,aaa.stockID as realstockID,aaa.position as realposition,aaa.inserttime as realinserttime,  bbb.* from (        select * from  (   select a.userID,a.stockID,(a.longhave-a.shorthave) as position,inserttime from [LogRecord].[dbo].[account_position] a inner join (  select MAX(time) as time  ,userid   FROM [LogRecord].[dbo].[account_position]  where date='20161129' group by userid) b  on a.time=b.time and a.userID=b.userID )ka ) aaa full outer join (    select * from [LogRecord].[dbo].[account_position_lilun]  ) bbb     on aaa.userID=bbb.userID and aaa.stockID=bbb.stockID     where aaa.position<>bbb.position or (bbb.userID is null and aaa.position<>0) or (aaa.userID is null and bbb.position<>0 )    "
		#670611	54	10	2016-11-29 11:10:07.040	NULL	NULL	NULL	NULL	NULL
		#666061001	54	20	2016-11-29 11:10:07.490	NULL	NULL	NULL	NULL	NULL
		#666061001	57	12	2016-11-29 11:10:07.490	158	666061001	57	15	2016-11-29 11:07:46.077
		#11803593	54	24	2016-11-29 11:10:07.490	NULL	NULL	NULL	NULL	NULL
		#11803593	57	17	2016-11-29 11:10:07.490	24	11803593	57	18	2016-11-29 11:07:46.077
		#11808319	54	9	2016-11-29 11:10:07.727	NULL	NULL	NULL	NULL	NULL
		#11808319	57	5	2016-11-29 11:10:07.727	40	11808319	57	7	2016-11-29 11:07:46.077
		#28032	54	20	2016-11-29 11:10:10.190	NULL	NULL	NULL	NULL	NULL
		#28032	57	12	2016-11-29 11:10:10.207	116	28032	57	15	2016-11-29 11:07:46.077
		#666061006	21	204	2016-11-29 11:11:01.780	161	666061006	21	210	2016-11-29 11:07:46.077
		#11803058	21	304	2016-11-29 11:11:07.583	4	11803058	21	308	2016-11-29 11:07:46.077
		#NULL	NULL	NULL	NULL	143	52001006	8	-2	2016-11-29 11:07:46.077
		#NULL	NULL	NULL	NULL	129	52001006	31	-5	2016-11-29 11:07:46.077
		#NULL	NULL	NULL	NULL	121	52001006	20	-4	2016-11-29 11:07:46.077
		#NULL	NULL	NULL	NULL	151	666061001	31	-11	2016-11-29 11:07:46.077
	res=ms.dict_sql(sql)
	disticnt_set=[]
	lilun_miss_set=[]
	real_miss_set=[]
	for item in res:
		if item['realuserID'] is None:
			real_miss_set.append(item)
		if item['userID'] is None:
			lilun_miss_set.append(item)
		if item['realuserID'] is not None and item['userID'] is not None:
			disticnt_set.append(item)
	print real_miss_set
	print lilun_miss_set
	print disticnt_set


show_distinct()