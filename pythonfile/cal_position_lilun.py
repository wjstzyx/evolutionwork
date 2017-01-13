#coding=utf-8 
#!/usr/bin/env python
###
#此脚本每隔一分钟运行一次，产生账户的理论仓位

import sys, urllib, urllib2, json
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

#将账号仓位快照入库
def cal_position_lilun():
	#1 put lilun equity into account_position_lilun,添加不存在报警机制
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="truncate table [LogRecord].[dbo].account_position_lilun"
	ms.insert_sql(sql)
	sql="select distinct userid from [LogRecord].[dbo].[account_position] order by userid"
	res=ms.dict_sql(sql)
	totalsql=""
	for item in res:
		userid=item['userid']
		ispass=0
		try:
			sql="select 1 from future.dbo.view_%s" % (userid)
			ms.insert_sql(sql)
			ispass=1
		except:
			sql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime],beizhu) values('%s',0,'%s',getdate(),'%s')" % (userid,0,'No view in 0.5 database')
			ms.insert_sql(sql)
		if ispass==1:
			tempsql="select '%s' as [userID],STOCK as [stockID],Expr1 as position,GETDATE() as nowtime from future.dbo.view_%s" % (userid,userid)
			totalsql=totalsql+" union all "+tempsql
	totalsql=totalsql.strip(" union all ")
	totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) "+ totalsql
	ms.insert_sql(totalsql)

	#2 shangpin yingshe
	totalsql=""
	ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="Future")
	res=['05810058','032442']
	for item in res:
		userid=item
		ispass=0
		try:
			sql="select 1 from future.dbo.view_%s" % (userid)
			ms1.insert_sql(sql)
			ispass=1
		except:
			sql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime],beizhu) values('%s',0,'%s',getdate(),'%s')" % (userid,0,'No view in 0.5 database')
			print sql
			ms.insert_sql(sql)
		if ispass==1:
			tempsql="select '%s' as [userID],STOCK as [stockID],Expr1 as position,GETDATE() as inserttime from future.dbo.view_%s" % (userid,userid)
			totalsql=totalsql+" union all "+tempsql
	totalsql=totalsql.strip(" union all ")
	#totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) "+ totalsql
	tempres=ms1.dict_sql(totalsql)

	#3 stock yinghse
	sql="SELECT [Symbol]  ,[S_ID] FROM [Future].[dbo].[Symbol_ID] where Symbol in ('IC','IF','IH','TF','T')"
	res=ms.dict_sql(sql)
	symboldict={}
	for item in res:
		symboldict[item['Symbol']]=item['S_ID']
	sql="SELECT a.account,a.symbol,sum(a.ratio*b.position ) as Position  FROM [future].[dbo].[account_position_stock_yingshe] a left join [future].[dbo].[RealPosition] b on a.acanme=b.Name group by a.account,a.symbol"
	res=ms1.dict_sql(sql)
	for item in res:
		print "'"+item['symbol']+"'"
		symbol_id=symboldict[item['symbol']]
		sql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) values('%s','%s','%s',getdate())" % (item['account'],symbol_id,item['Position'])
		ms.insert_sql(sql)
	totalsql=""
	tempv=""
	for item in tempres:
		tempv=",('%s','%s','%s','%s')" % (item['userID'],item['stockID'],int(item['position']),item['inserttime'].strftime("%Y-%m-%d %H:%M:%S"))
		totalsql=totalsql+tempv
	totalsql=totalsql.strip(",")
	totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) values%s" % (totalsql)
	ms.insert_sql(totalsql)





def monitor_add_errorinfo(type,myitem):
	#查询发件人
	sql="select email from [LogRecord].[dbo].[mailtolist] where istomail=1"
	reslist=ms.find_sql(sql)
	mailtolist=''
	sendmessage=''
	for item in reslist:
		if "@" in item[0]:
			mailtolist=mailtolist+','+item[0]
		else:
			sendmessage=sendmessage+','+item[0]
	mailtolist=mailtolist.strip(',')
	sendmessage=sendmessage.strip(',')

	# print mailtolist
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='%s' and item='%s' and ismonitor=1" % (type,myitem)
	res=ms.dict_sql(sql)
	for item in res:
		symbol=item['item']
		starttime=item['starttime']
		endtime=item['endtime']
		sql="select getdate()"
		getnow=ms.find_sql(sql)[0][0]
		nowtime=getnow.strftime('%H:%M:%S')
		nowtime=datetime.datetime.strptime(nowtime,'%H:%M:%S')
		starttime=datetime.datetime.strptime(starttime,'%H:%M:%S')
		endtime=datetime.datetime.strptime(endtime,'%H:%M:%S')
		if nowtime>starttime and nowtime<=endtime:
			# print '报警'
			# print "@@@@@@@@@@@@@ERROE@@@@@@@@@@@@@@"
			subject='ctontab出错 %s' % (myitem)
			msg=subject
			sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,msg,0,sendmessage)
			ms.insert_sql(sql)
			break

try:
	cal_position_lilun()
except:
	monitor_add_errorinfo('crontab','cal_position_lilun')
	print '$$$send error info'
