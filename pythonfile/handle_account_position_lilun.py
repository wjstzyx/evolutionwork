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
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
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
	#2 shangpin yingshe
	ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="Future")
	sql="SELECT a.account as userID,a.stock as stockID,(handperstock*position) as position,GETDATE() as inserttime  FROM [future].[dbo].[SP_ACCOUNT_STRATEGY] a  left join [future].[dbo].[SP_STRATEGY] b  on a.stock=b.stock and a.strategyname=b.name where  position<>0"
	tempres=ms1.dict_sql(sql)
	totalsql=""
	tempv=""
	for item in tempres:
		tempv=",('%s','%s','%s','%s')" % (item['userID'],item['stockID'],item['position'],item['inserttime'].strftime("%Y-%m-%d %H:%M:%S"))
		totalsql=totalsql+tempv
	totalsql=totalsql.strip(",")
	totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) values%s" % (totalsql)
	ms.insert_sql(totalsql)


cal_distinct_position_lilun()


def show_distinct():
	nowday=datetime.datetime.now().strftime('%Y%m%d')
	sql=" select aaa.userID as realuserID,aaa.stockID as realstockID,aaa.position as realposition,aaa.inserttime as realinserttime,  bbb.* from (        select * from  (   select a.userID,a.stockID,(a.longhave-a.shorthave) as position,inserttime from [LogRecord].[dbo].[account_position] a inner join (  select MAX(time) as time  ,userid   FROM [LogRecord].[dbo].[account_position]  where date='20161129' group by userid) b  on a.time=b.time and a.userID=b.userID )ka ) aaa full outer join (    select * from [LogRecord].[dbo].[account_position_lilun]  ) bbb     on aaa.userID=bbb.userID and aaa.stockID=bbb.stockID     where aaa.position<>bbb.position or (bbb.userID is null and aaa.position<>0) or (aaa.userID is null and bbb.position<>0 )    "
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
	# print real_miss_set
	# print lilun_miss_set
	# print disticnt_set
	return real_miss_set,lilun_miss_set,disticnt_set


# real_miss_set,lilun_miss_set,disticnt_set=show_distinct()
# print disticnt_set