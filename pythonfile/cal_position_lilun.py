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
	sql="select distinct userid from [LogRecord].[dbo].[account_position]  where userid<>'05810058' order by userid"
	res=ms.dict_sql(sql)
	totalsql=""
	for item in res:
		userid=item['userid']
		ispass=0
		try:
			sql="select 1 from Fun_account_position_all_V2('%s')" % (userid)
			ms.insert_sql(sql)
			ispass=1
		except:
			sql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime],beizhu) values('%s',0,'%s',getdate(),'%s')" % (userid,0,'No view in 0.5 database')
			ms.insert_sql(sql)
		if ispass==1:
			tempsql="select '%s' as [userID],STOCK as [stockID],Expr1 as position,GETDATE() as nowtime from Fun_account_position_all_V2('%s')" % (userid,userid)
			totalsql=totalsql+" union all "+tempsql
	totalsql=totalsql.strip(" union all ")
	totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) "+ totalsql
	ms.insert_sql(totalsql)

	#2 shangpin yingshe
	totalsql=""
	ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="Future")
	res=['05810058']
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
	sql="SELECT a.account,a.symbol,sum(a.ratio*b.position ) as Position  FROM [future].[dbo].[account_position_stock_yingshe] a left join [future].[dbo].[RealPosition] b on a.acanme=b.Name group by a.account,a.symbol having a.account not in ('666061008')"
	res=ms1.dict_sql(sql)
	for item in res:
		#print item 
		symbol_id=symboldict[item['symbol']]
		sql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) values('%s','%s','%s',getdate())" % (item['account'],symbol_id,item['Position'])
		#print sql 
		ms.insert_sql(sql)

	totalsql=""
	tempv=""
	for item in tempres:
		tempv=",('%s','%s','%s','%s')" % (item['userID'],item['stockID'],int(item['position']),item['inserttime'].strftime("%Y-%m-%d %H:%M:%S"))
		totalsql=totalsql+tempv
	totalsql=totalsql.strip(",")
	if len(totalsql)>10:
		totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) values%s" % (totalsql)
		print totalsql
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
			print sql 
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
					myuniqueid=item['userID']+'_'+str(int(item['stockID']))
					print myuniqueid,'delete'
					id=item['id']
					sql="delete from [LogRecord].[dbo].[account_position_temp_compare] where id=%s" % (id)
					ms.insert_sql(sql)
					#置为isactive=0
					sql="update [LogRecord].[dbo].[all_monitor_info] set [issolved]=1 where TYPE='Account' and item='%s' and [issolved]=0" % (myuniqueid)
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
					if atime>3:
						# print '报警'
						# print "@@@@@@@@@@@@@ERROE@@@@@@@@@@@@@@"
						# subject='%s 实盘仓位与数据库不一致' % (aa[0])
						# msg=subject
						# sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,	mailtolist,msg,0,sendmessage)
						# #print sql 
						# ms.insert_sql(sql)
						#插入信息显示
						type='Account'
						item=uniquekey
						msg='实盘仓位与数据库不一致'	
						classcode='fa-comment'
						sql="select 1 from [LogRecord].[dbo].[all_monitor_info] where type='%s' and item='%s' and issolved=0" % (type,item)
						res=ms.dict_sql(sql)
						#print sql 
						if res:
							sql="update [LogRecord].[dbo].[all_monitor_info] set updatetime=getdate()  where type='%s' and item='%s'" % (type,item)
							#print sql 
							ms.insert_sql(sql)
						else:
							sql=" insert into [LogRecord].[dbo].[all_monitor_info](type,item,msg,[issolved],[isactive],[inserttime],[updatetime],[classcode]) values('%s','%s','%s','%s','%s',getdate(),getdate(),'%s')" % (type,item,msg,0,1,classcode)
							#print sql 
							ms.insert_sql(sql)





# update getrecordlist=[{'item':myitem['name'],'msg':msg},{},{}]
def update_target_table(getrecordlist,type):
	sql="SELECT [id]   ,[type]    ,[item]    ,[msg]     ,[issolved]    ,[isactive]    ,[inserttime] ,[updatetime]     ,[classcode]    FROM [LogRecord].[dbo].[all_monitor_info] where type='%s' and issolved=0 and isactive=1 order by id " % (type)
	res2=ms.dict_sql(sql)
	res2item=[[aa['item'],aa['id']] for aa in res2]
	res1item=[aa['item'] for aa in getrecordlist]
	#1 set some to issovlved
	for item in res2item:
		if item[0] not in res1item:
			sql="update [LogRecord].[dbo].[all_monitor_info] set issolved=1 where type='%s' and id=%s" % (type,item[1])
			ms.insert_sql(sql)
	#2 update or insert to all_monitor_info
	for item in getrecordlist:
		sql = "select 1 from [LogRecord].[dbo].[all_monitor_info] where type='%s' and item='%s' and issolved=0" % (
		type, item['item'])
		res = ms.dict_sql(sql)
		if res:
			sql = "update [LogRecord].[dbo].[all_monitor_info] set updatetime=getdate()  where type='%s' and item='%s'" % (
			type, item['item'])
			# print sql
			ms.insert_sql(sql)
		else:
			sql = " insert into [LogRecord].[dbo].[all_monitor_info](type,item,msg,[issolved],[isactive],[inserttime],[updatetime],[classcode]) values('%s','%s','%s','%s','%s',getdate(),getdate(),'%s')" % (
			type, item['item'], item['msg'], 0, 1, 'fa-bolt')
			# print sql
			ms.insert_sql(sql)







#仓位报警-差异超过3分钟就报警
def account_database_isdistinct_V2():
	getrecordlist=[]
	#查询发件人
	(mailtolist,sendmessage)=get_messagelist()
	# print mailtolist
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='Account_distinguish' and ismonitor=1"
	res=ms.dict_sql(sql)
	nowhour=datetime.datetime.now().strftime('%H%M')
	nowhour=int(nowhour)
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
			sql="select kaa.userid as account_userid,kaa.stockid as account_stockid,kaa.position as account_position,kaa.sendposition,kaa.inserttime as account_time,kbb.* from (select a.userID,a.stockID,(a.longhave-a.shorthave) as position,([longsend]-[shortsend]) as sendposition ,inserttime from [LogRecord].[dbo].[account_position] a inner join (  select MAX(time) as 	time  ,userid   FROM [LogRecord].[dbo].[account_position]  where date='%s' group by userid) b  on a.time=b.time and a.userID=b.userID and a.date='%s' where not ((a.longhave-a.shorthave)=0 and ([longsend]-[shortsend])=0)) kaa full outer join ( select userID,stockID,sum(position)as position,MAX(inserttime)as inserttime  from [LogRecord].[dbo].[account_position_lilun]  group by 	userID,stockID  having sum(position)<>0  ) kbb on kaa.userID=kbb.userID and kaa.stockID=kbb.stockID   where kaa.userID is null or kbb.stockID is null or not  (kaa.position=kbb.position and kaa.sendposition=0) and (kaa.userid<>'05810058' or kbb.userid<>'05810058')" % (nowday,nowday)
			res=ms.dict_sql(sql)
			newrecord=[]
			#[[userid,stockid,account_posiiotn,account_sendposition,position,account_time,inserttime]]
			for item in res:
				if item['account_userid'] is None:
					temp=[item['userID'],item['stockID'],0,0,item['position'],item['inserttime'],item['inserttime']]
				if item['userID'] is None:
					temp=[item['account_userid'],item['account_stockid'],item['account_position'],item['sendposition'],0,item['account_time'],item['account_time']]
				if item['account_userid'] is not None and item['userID'] is not None:
					temp=[item['account_userid'],item['account_stockid'],item['account_position'],item['sendposition'],item['position'],item['account_time'],item['inserttime']]
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
					myuniqueid=item['userID']+'_'+str(int(item['stockID']))
					#print myuniqueid,'delete'
					id=item['id']
					sql="delete from [LogRecord].[dbo].[account_position_temp_compare] where id=%s" % (id)
					ms.insert_sql(sql)
					#置为isactive=0
					sql="update [LogRecord].[dbo].[all_monitor_info] set [issolved]=1 where TYPE='Account' and item='%s' and [issolved]=0" % (myuniqueid)
					ms.insert_sql(sql)
			#update and insert 
			for aa in newrecord:
				uniquekey=aa[0]+'_'+str(int(aa[1]))
				now_real_position=int(aa[2])+int(aa[3])
				if uniquekey  not in oldlistquotes:
					#print 'insert'
					sql="insert into [LogRecord].[dbo].[account_position_temp_compare](userID,stockID,realposition,lilunposition,inserttime) values('%s','%s','%s','%s',getdate())" % (aa[0],aa[1],int(aa[2])+int(aa[3]),int(aa[4]))
					ms.insert_sql(sql)
				else:
					sql="SELECT DATEDIFF(MINUTE, inserttime,getdate()) as timediff,inserttime, getdate() as nowtime,realposition FROM [LogRecord].[dbo].[account_position_temp_compare] where userID='%s' and stockID='%s'" %	 (aa[0],int(aa[1]))
					mytime=ms.dict_sql(sql)
					atime=mytime[0]['timediff']
					last_real_position=mytime[0]['realposition']
					if int(last_real_position)<>int(now_real_position):
						print uniquekey,'last_real_position',last_real_position,'now_real_position',now_real_position
						sql="update [LogRecord].[dbo].account_position_temp_compare set [inserttime]=getdate() where userid='%s' and stockid=%s" % (aa[0],int(aa[1]))
						ms.insert_sql(sql)
						continue
					if atime>4 and ((nowhour>=901 and nowhour<=1130) or (nowhour>=1331 and nowhour<=1459)):
						print uniquekey,'last_real_position',last_real_position,'now_real_position',now_real_position
						print 'aa',aa
						if int(aa[1]) in (11,4) and nowhour>933:
							getrecordlist.append({'item':uniquekey,'msg':'仓位不一致 real:%s database:%s' % (aa[2],aa[4])})
						if int(aa[1]) not in (11,4):
							getrecordlist.append({'item':uniquekey,'msg':'仓位不一致 real:%s database:%s' % (aa[2],aa[4])})
	dayofweek=datetime.datetime.now().weekday()
	if dayofweek in (5,6):
		getrecordlist=[]

	update_target_table(getrecordlist, 'Account')

						# if aa[3]<>0:
						# 	if 
						# 算上send position 再比较

						# print '报警'
						# print "@@@@@@@@@@@@@ERROE@@@@@@@@@@@@@@"
						# subject='%s 实盘仓位与数据库不一致' % (aa[0])
						# msg=subject
						# sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,	mailtolist,msg,0,sendmessage)
						# #print sql 
						# ms.insert_sql(sql)
						#插入信息显示
						# type='Account'
						# item=uniquekey
						# msg='实盘仓位与数据库不一致 lasttime:%s nowtime:%s' % (mytime[0]['inserttime'],mytime[0]['nowtime'])
						# classcode='fa-comment'
						# sql="select 1 from [LogRecord].[dbo].[all_monitor_info] where type='%s' and item='%s' and issolved=0" % (type,item)
						# res=ms.dict_sql(sql)
						# #print sql 
						# if res:
						# 	sql="update [LogRecord].[dbo].[all_monitor_info] set updatetime=getdate()  where type='%s' and item='%s'" % (type,item)
						# 	#print sql 
						# 	ms.insert_sql(sql)
						# else:
						# 	sql=" insert into [LogRecord].[dbo].[all_monitor_info](type,item,msg,[issolved],[isactive],[inserttime],[updatetime],[classcode]) values('%s','%s','%s','%s','%s',getdate(),getdate(),'%s')" % (type,item,msg,0,1,classcode)
						# 	#print sql 
						# 	ms.insert_sql(sql)








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




def crontab_delete_record():
	hour=datetime.datetime.now().hour
	minutes=datetime.datetime.now().minute
	if hour==19 and (minutes>=0 or minutes<=5):
		sql="delete from [LogRecord].[dbo].[all_monitor_info] where issolved=1 and isactive=1 and  DATEDIFF(day,updatetime,GETDATE())>5"
		ms.insert_sql(sql)




try:
	print "begin: cal_position_lilun"
	cal_position_lilun()
	print "begin: account_database_isdistinct_V2"
	account_database_isdistinct_V2()
	crontab_delete_record()

except:
	monitor_add_errorinfo('crontab','cal_position_lilun')
	print '$$$send error info'
