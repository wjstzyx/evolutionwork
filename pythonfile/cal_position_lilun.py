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

def get_messagelist():
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
	return mailtolist,sendmessage


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


#仓位报警-差异超过3分钟就报警
def account_database_isdistinct():
	#查询发件人
	(mailtolist,sendmessage)=get_messagelist()
	# print mailtolist
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='Account_distinguish' and ismonitor=1"
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
			nowday=datetime.datetime.now().strftime('%Y%m%d')
			sql="select aaa.userID as realuserID,aaa.stockID as realstockID,aaa.position as realposition,aaa.inserttime as realinserttime,  bbb.* from (        select * from  	(   select a.userID,a.stockID,(a.longhave-a.shorthave) as position,inserttime from [LogRecord].[dbo].[account_position] a inner join (  select MAX(time) as 	time  ,userid   FROM [LogRecord].[dbo].[account_position]  where date='%s' group by userid) b  on a.time=b.time and a.userID=b.userID and a.date='%s')ka ) aaa 	full outer join (     select userID,stockID,sum(position)as position,MAX(inserttime)as inserttime  from [LogRecord].[dbo].[account_position_lilun]  group by 	userID,stockID ) bbb       on aaa.userID=bbb.userID and aaa.stockID=bbb.stockID  where aaa.position<>bbb.position or (bbb.userID is null and aaa.position<>0) 	or (aaa.userID is null and bbb.position<>0 ) and (bbb.userID in (select distinct userID from [LogRecord].[dbo].account_position)) order by aaa.userID" % (nowday,nowday)
			res=ms.dict_sql(sql)
			newrecord=[]
			for item in res:
				if item['realuserID'] is None:
					temp=[item['userID'],item['stockID'],0,item['position'],item['inserttime']]
				if item['userID'] is None:
					temp=[item['realuserID'],item['realstockID'],item['realposition'],0,item['realinserttime']]
				if item['realuserID'] is not None and item['userID'] is not None:
					temp=[item['realuserID'],item['realstockID'],item['realposition'],item['position'],item['realinserttime']]
				newrecord.append(temp)
			#listnew
			newlistquotes=[aa[0]+'_'+str(int(aa[1])) for aa in newrecord]
			#print newlistquotes
			# for item in newrecord:
			# 	print item 
			sql="SELECT id,[userID]   ,[stockID]   ,[realposition]   ,[lilunposition]    ,[inserttime] FROM [LogRecord].[dbo].[account_position_temp_compare]"
			res=ms.dict_sql(sql)
			#delete 
			oldlistquotes=[]
			for item in res:
				oldlistquotes.append(item['userID']+'_'+str(int(item['stockID'])))
				if item['userID']+'_'+str(int(item['stockID'])) not in newlistquotes:
					print item['userID']+'_'+str(int(item['stockID'])),'delete'
					id=item['id']
					sql="delete from [LogRecord].[dbo].[account_position_temp_compare] where id=%s" % (id)
					ms.insert_sql(sql)
			#update and insert 
			for aa in newrecord:
				uniquekey=aa[0]+'_'+str(int(aa[1]))
				if uniquekey  not in oldlistquotes:
					print 'update   insert'
					sql="insert into [LogRecord].[dbo].[account_position_temp_compare](userID,stockID,realposition,lilunposition,inserttime) values('%s','%s','%s','%s',getdate())" % (aa[0],aa[1],aa[2],int(aa[3]))
					ms.insert_sql(sql)
				else:
					sql="SELECT DATEDIFF(MINUTE, inserttime,getdate()) as timediff  FROM [LogRecord].[dbo].[account_position_temp_compare] where userID='%s' and stockID='%s'" %	 (aa[0],int(aa[1]))
					mytime=ms.dict_sql(sql)
					atime=mytime[0]['timediff']
					if atime>2:
						# print '报警'
						# print "@@@@@@@@@@@@@ERROE@@@@@@@@@@@@@@"
						subject='%s 实盘仓位与数据库不一致' % (aa[0])
						msg=subject
						sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,	mailtolist,msg,0,sendmessage)
						#print sql 
						ms.insert_sql(sql)
						break









def monitor_add_errorinfo(type,myitem):
	#查询发件人
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
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
			print sql 
			ms.insert_sql(sql)
			break






try:
	cal_position_lilun()
	account_database_isdistinct()

except:
	monitor_add_errorinfo('crontab','cal_position_lilun')
	print '$$$send error info'
