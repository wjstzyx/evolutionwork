#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
import time
import sys, urllib, urllib2, json
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList


def cloud_database_quotes():
	myms=MSSQL(host="139.196.190.246",user="future",pwd="K@ra0Key",db="future")
	sql=""


def monitor_AB_st_night():
	#查询发件人
	(mailtolist,sendmessage)=get_messagelist()
	# print mailtolist
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='AB_ST_NIGHT' and ismonitor=1"
	res=ms.dict_sql(sql)[0]
	starttime=res['starttime']
	endtime=res['endtime']
	sql="select getdate()"
	getnow=ms.find_sql(sql)[0][0]
	nowtime=getnow.strftime('%H:%M:%S')
	nowtime=datetime.datetime.strptime(nowtime,'%H:%M:%S')
	starttime=datetime.datetime.strptime(starttime,'%H:%M:%S')
	endtime=datetime.datetime.strptime(endtime,'%H:%M:%S')
	if nowtime>starttime and nowtime<=endtime:
		##报警超过3分钟的st(type 字段说明：默认0 不报警，1位白天监控，2为夜盘监控)
		sql="SELECT  [id]     ,[st]    ,DATEDIFF(MINUTE, [stockdate], getdate()) as timediff   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3   and type in (2,12) order by timediff desc"
		res=ms.dict_sql(sql)
		message=''
		subject='AB策略卡死报警'+datetime.datetime.now().strftime("%H:%M:%S")
		if res:
			print "have waring2"
			stringnum=0
			for item in res:
				stringnum=stringnum+1
				st=item['st']
				timediff=item['timediff']
				if stringnum<50:
					message=message+'策略号 '+str(st)+': '+' 卡死时间: '+str(timediff)+'(分钟)'
			sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,message,0,sendmessage)
			ms.insert_sql(sql)
		else:	
			# print starttime
			# print endtime
			# print nowtime
			pass
		sql="select * from [LogRecord].[dbo].[ST_heart] where type in (2,12)"
		res=ms.dict_sql(sql)
		for item in res:
			stockdate=item['stockdate']
			timenum=item["timenum"]
			period=item['period']
			st=item['st']
			timenum=str(timenum)
			if len(timenum)==5:
				timenum="0"+timenum
			timenum=datetime.datetime.strptime(timenum,'%H%M%S')
			stockdate=datetime.datetime.strptime(stockdate.strftime("%H%M%S"),'%H%M%S')
			if stockdate>=timenum:
				tempdate=round((stockdate-timenum).seconds/60)
			else:
				tempdate=round((timenum-stockdate).seconds/60)

			if tempdate>(period+16) and (nowtime1>='21:05:00' and nowtime1<='23:00:00'):
				message=''+str(st)
				subject='夜盘策略行情无更新'+datetime.datetime.now().strftime("%H:%M:%S")
				print "have waring3"
				sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,message,0,sendmessage)
				ms.insert_sql(sql)
				break







def monitor_AB_st_day():
	#查询发件人
	(mailtolist,sendmessage)=get_messagelist()
	# print mailtolist
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='AB_ST_DAY' and ismonitor=1"
	res=ms.dict_sql(sql)[0]
	starttime=res['starttime']
	endtime=res['endtime']
	sql="select getdate()"
	getnow=ms.find_sql(sql)[0][0]
	nowtime=getnow.strftime('%H:%M:%S')
	nowtime1=nowtime
	nowtime=datetime.datetime.strptime(nowtime,'%H:%M:%S')
	starttime=datetime.datetime.strptime(starttime,'%H:%M:%S')
	endtime=datetime.datetime.strptime(endtime,'%H:%M:%S')
	if nowtime>starttime and nowtime<=endtime:
		##报警超过3分钟的st(type 字段说明：默认0 不报警，1位白天监控，2为夜盘监控)
		sql="SELECT  [id]     ,[st]  ,address  ,DATEDIFF(MINUTE, [stockdate], getdate()) as timediff   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3   and type in (1,12)  order by timediff desc"
		res=ms.dict_sql(sql)
		message=''
		subject='AB策略卡死报警'+datetime.datetime.now().strftime("%H:%M:%S")
		if res:
			subject=str(res[0]['st'])+" "+str(res[0]['address'])+"策略卡死"+datetime.datetime.now().strftime("%H:%M:%S")
			
		if res:
			print "have waring4"
			stringnum=0
			for item in res:
				stringnum=stringnum+1
				st=item['st']
				address=item['address']
				timediff=item['timediff']
				if stringnum<30:
					message=message+'策略号 '+str(st)+' '+str(address)+' 卡死时间: '+str(timediff)+'(分钟)'
			# if len(message)>1800:
			# 	message=message[:1000]
			sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,message,0,sendmessage)
			ms.insert_sql(sql)
		else:	
			# print starttime
			# print endtime
			# print nowtime
			pass
		sql="select * from [LogRecord].[dbo].[ST_heart] where type in (1,12)"
		res=ms.dict_sql(sql)
		for item in res:
			stockdate=item['stockdate']
			timenum=item["timenum"]
			period=item['period']
			# stockdate=datetime.datetime.strptime('2016-11-21 09:47:02','%Y-%m-%d %H:%M:%S')
			# timenum=94600
			st=item['st']
			timenum=str(timenum)
			if len(timenum)==5:
				timenum="0"+timenum
			timenum=datetime.datetime.strptime(timenum,'%H%M%S')
			stockdate=datetime.datetime.strptime(stockdate.strftime("%H%M%S"),'%H%M%S')
			if stockdate>=timenum:
				tempdate=round((stockdate-timenum).seconds/60)
			else:
				tempdate=round((timenum-stockdate).seconds/60)

			if tempdate>(period+16) and ((nowtime1>='09:33:00' and nowtime1<='10:14:00') or (nowtime1>='10:30:00' and nowtime1<='11:30:00') or (nowtime1>='13:35:00' and nowtime1<='15:00:00')):
				print stockdate,timenum,round((stockdate-timenum).seconds/60),period
				message=''+str(st)+stockdate.strftime('%Y-%m-%d %H:%M:%S')+" "+timenum.strftime('%Y-%m-%d %H:%M:%S')+" "+str(period)+" "+str(round((stockdate-timenum).seconds/60))
				subject='日盘策略没有更新行情'+" "+datetime.datetime.now().strftime("%H:%M:%S")
				print "have waring1"
				sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,message,0,sendmessage)
				ms.insert_sql(sql)
				break






def monitor_wenhua():
	#查询发件人
	(mailtolist,sendmessage)=get_messagelist()
	# print mailtolist
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='wenhua' and ismonitor=1"
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
			#检测最新的一根与当时的时间差，如果相差3分钟就报警
			sql="select top 1 stockdate from Tsymbol where Symbol='%s' order by StockDate desc" % (symbol)
			res=ms.find_sql(sql)
			if res:
				lasttime=res[0][0]
				print "wenhua"
				if getnow>lasttime:
					deltatime=(getnow-lasttime).seconds
				else:
					deltatime=(lasttime-getnow).seconds
				print deltatime
				if deltatime>180:
					subject='%s文华数据采集产生延迟' % (symbol)
					msg='%s 文华数据采集产生延迟' % (symbol)
					sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,msg,0,sendmessage)
					ms.insert_sql(sql)
		else:	
			# print starttime
			# print endtime
			# print nowtime
			pass



def monitor_AB():
	#查询发件人
	(mailtolist,sendmessage)=get_messagelist()
	# print mailtolist
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='AB' and ismonitor=1"
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
			#检测最新更新时间与当时的时间差，如果相差60s就报警
			sql="SELECT TOP 1 UpdateTime   FROM [Future].[dbo].[Trading_ABMonitor] WHERE ComputerName='%s' and IFMonitor=1" % (symbol)
			res=ms.find_sql(sql)
			if res:
				lasttime=res[0][0]
				print "AB"
				print lasttime
				print getnow
				if getnow>lasttime:
					deltatime=(getnow-lasttime).seconds
				else:
					deltatime=(lasttime-getnow).seconds
				print deltatime
				if deltatime>50:
					subject='%s AB程序出错' % (symbol)
					msg='%s AB程序出错' % (symbol)
					sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,msg,0,sendmessage)
					ms.insert_sql(sql)
		else:	
			# print starttime
			# print endtime
			# print nowtime
			pass



def monitor_Thunder():
	#查询发件人
	(mailtolist,sendmessage)=get_messagelist()
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='Thunder' and ismonitor=1"
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
			#检测最新更新时间与当时的时间差，如果相差70s就报警
			sql="SELECT time  FROM [future].[dbo].[Program_night] where name='%s'" % (symbol)
			res=ms1.find_sql(sql)
			if res:
				lasttime=res[0][0]
				print lasttime
				#lasttime=210509
				#nowtime='21:05:01'
				mynowtime=int(getnow.strftime('%H%M%S'))
				print mynowtime
				chayi=minusmin(lasttime,mynowtime)
				print 'chayi',chayi
				if chayi>70 or chayi<-70:
					subject='%s Thunder程序出错' % (symbol)
					msg='%s Thunder程序出错' % (symbol)
					sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,msg,0,sendmessage)
					ms.insert_sql(sql)
			else:
				subject='%s Thunder程序出错' % (symbol)
				msg='%s Thunder程序出错' % (symbol)
				sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,msg,0,sendmessage)
				ms.insert_sql(sql)


		else:	
			# print starttime
			# print endtime
			# print nowtim
			pass


def minusmin(time1,time2):
	#time1=160523
	hour1=round(time1/10000)
	min1=round((time1%10000)/100)
	sec1=time1-hour1*10000-min1*100
	hour2=round(time2/10000)
	min2=round((time2%10000)/100)
	sec2=time2-hour2*10000-min2*100
	return (hour2-hour1)*3600+(min2-min1)*60+(sec2-sec1)



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


def ismonitorday():
	# refer to http://apistore.baidu.com/apiworks/servicedetail/1116.html
	url = 'http://apis.baidu.com/xiaogg/holiday/holiday?d=20160902'
	req = urllib2.Request(url)
	req.add_header("apikey", "6677fe3debefda50dd040fbf98d0d38b")
	resp = urllib2.urlopen(req)
	content = resp.read()
	if(content):
	    print(content)




	sql="select top 1 D from TSymbol where T>'05:00' ORDER BY id desc"
	lastday=ms.find_sql(sql)[0][0]
	lastday='20'+lastday[2:4]+lastday[5:7]+lastday[8:10]
	sql="select getdate()"
	nowD=ms.find_sql(sql)[0][0].strftime('%Y%m%d')
	sql="select datepart(weekday, getdate())"
	weekday=ms.find_sql(sql)[0][0]
	if  weekday in (2,3,4,5,6):
		return 1
	else:
		return 0






 
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
			#delete 
			sql="select kb.id from (select ISNULL(realuserID,userID) as userID,ISNULL(realstockID,stockID) as stockID,ISNULL(realposition,0) as realposition,ISNULL(position,0) as position,GETDATE() as nowtime from (select aaa.userID as realuserID,aaa.stockID as realstockID,aaa.position as realposition,aaa.inserttime as realinserttime,  bbb.* from (        select * from  (   select a.userID,a.stockID,(a.longhave-a.shorthave) as position,inserttime from [LogRecord].[dbo].[account_position] a inner join (     select MAX(time) as time  ,userid   FROM [LogRecord].[dbo].[account_position]  where date='%s' group by userid) b  on a.time=b.time and a.userID=b.userID     and a.date='%s')ka ) aaa full outer join (     select userID,stockID,sum(position)as position,MAX(inserttime)as inserttime  from [LogRecord].[dbo].[account_position_lilun]  group by userID,stockID ) bbb       on aaa.userID=bbb.userID and aaa.stockID=bbb.stockID  where aaa.position<>bbb.position or (bbb.userID is null and aaa.position<>0) or (aaa.userID is null and bbb.position<>0 ) and (bbb.userID in (select distinct userID from [LogRecord].[dbo].account_position))) gg) ka right join [LogRecord].[dbo].[account_position_temp_compare] kb on ka.userID=kb.userid and ka.stockID=kb.stockID where ka.userID is null" % (nowday,nowday)
			res=ms.dict_sql(sql)
			for item in res:
				id=item['id']
				sql="delete from [LogRecord].[dbo].[account_position_temp_compare] where id=%s" % (id)
				ms.insert_sql(sql)

			#update
			sql="select ka.*,kb.realposition as oldrealposition,kb.lilunposition as oldlilunposition, DATEDIFF(MINUTE, kb.inserttime,ka.nowtime) as timediff  from (select ISNULL(realuserID,userID) as userID,ISNULL(realstockID,stockID) as stockID,ISNULL(realposition,0) as realposition,ISNULL(position,0) as position,GETDATE() as nowtime from (select aaa.userID as realuserID,aaa.stockID as realstockID,aaa.position as realposition,aaa.inserttime as realinserttime,  bbb.* from (        select * from  (   select a.userID,a.stockID,(a.longhave-a.shorthave) as position,inserttime from [LogRecord].[dbo].[account_position] a inner join (     select MAX(time) as time  ,userid   FROM [LogRecord].[dbo].[account_position]  where date='%s' group by userid) b  on a.time=b.time and a.userID=b.userID     and a.date='%s')ka ) aaa full outer join (     select userID,stockID,sum(position)as position,MAX(inserttime)as inserttime  from [LogRecord].[dbo].[account_position_lilun]  group by userID,stockID ) bbb       on aaa.userID=bbb.userID and aaa.stockID=bbb.stockID  where aaa.position<>bbb.position or (bbb.userID is null and aaa.position<>0) or (aaa.userID is null and bbb.position<>0 ) and (bbb.userID in (select distinct userID from [LogRecord].[dbo].account_position))) gg) ka left join [LogRecord].[dbo].[account_position_temp_compare] kb on ka.userID=kb.userid and ka.stockID=kb.stockID" % (nowday,nowday)
			res=ms.dict_sql(sql)
			for item in res:
				if item['oldrealposition'] is None:
					sql="insert into [LogRecord].[dbo].[account_position_temp_compare]([userID]  ,[stockID] ,[realposition]  ,[lilunposition]  ,[inserttime]) values('%s',%s,%s,%s,getdate())" % (item['userID'],item['stockID'],item['realposition'],item['position'])
					ms.insert_sql(sql)
				else:
					if item['timediff']>2:
						# print '报警'
						# print "@@@@@@@@@@@@@ERROE@@@@@@@@@@@@@@"
						subject='实盘仓位与数据库不一致'
						msg='实盘仓位与数据库不一致'
						sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,msg,0,sendmessage)
						ms.insert_sql(sql)
						break
#阶梯1,2 AB仓位对比报警
def jieti_AB_isdistinct():
	#查询发件人
	(mailtolist,sendmessage)=get_messagelist()
	# print mailtolist
	#待检测的ABmachine列表
	sql="select item,starttime,endtime from [LogRecord].[dbo].[monitorconfig] where type='jieti_ab_position' and ismonitor=1"
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
			#delete 
			nowday=datetime.datetime.now().strftime('%Y%m%d')
			sql="select 'jieti1'as type,a.*,b.P as lilunP, b.tradetime as liluntime,c.P,c.tradetime,d.Symbol,b.TradName from (select st from P_BASIC where ac in (select f_ac from p_follow  where ac='StepMultiI300w' ))a left join [Future].[dbo].[for_backtest_Trading_logSymbol] b on a.ST=b.ST left join Future.dbo.Trading_logSymbol c on a.ST=c.ST left join Future.dbo.Symbol_ID d on cast(left(RIGHT(a.st,7),2) as int)=d.S_ID where d.Symbol not in ('AGN','AUN','CUN','Inight','Rbnight','MEZL','Pnight','LZL') and b.P<>c.P  union all 				select 'jieti2' as type, a.*,b.P as lilunP, b.tradetime as liluntime,c.P,c.tradetime,d.Symbol,b.TradName from (select st from P_BASIC where ac in (select f_ac from p_follow  where ac='StepMulti2' ))a left join [Future].[dbo].[for_backtest_Trading_logSymbol] b on a.ST=b.ST left join Future.dbo.Trading_logSymbol c on a.ST=c.ST left join Future.dbo.Symbol_ID d on cast(left(RIGHT(a.st,7),2) as int)=d.S_ID where d.Symbol not in ('AGN','AUN','CUN','Inight','Rbnight','MEZL','Pnight','LZL') and b.P<>c.P "
			res11=ms.dict_sql(sql)
			sql="select st,DATEDIFF(Minute,[inserttime],getdate()) as timediff from [LogRecord].[dbo].[jieti_AB_temp_compare]"
			tempstlist=ms.dict_sql(sql)
			stlist=[item1['st'] for item1 in tempstlist]
			newstlist=[item1['st'] for item1 in res11]
			for item in stlist:
				st=item
				if st not in newstlist:
					sql="delete from [LogRecord].[dbo].[jieti_AB_temp_compare] where st=%s" % (st)
					ms.insert_sql(sql)

			for item in res11:
				type=item['type']
				st=item['st']
				if st not in stlist:
					sql="insert into [LogRecord].[dbo].[jieti_AB_temp_compare](st,type,[realposition],[lilunposition],[inserttime]) values('%s','%s',%s,%s,getdate())" % (st,type,item['P'],item['lilunP'])
					ms.insert_sql(sql)
			for item1 in tempstlist:
				if item['st'] in newstlist and item1['timediff']>3:
						# print '报警'
						# print "@@@@@@@@@@@@@ERROE@@@@@@@@@@@@@@"
						subject='阶梯型策略AB信号出现差异'
						msg='阶梯型策略AB信号出现差异'
						sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,msg,0,sendmessage)
						ms.insert_sql(sql)
						break






if ismonitorday()==0:
	exit()

print "begin"

while(1):
	try:
		monitor_wenhua()
	except Exception,e:
		print e,"monitor_wenhua"
		pass
	try:
		monitor_AB()
	except Exception,e:
		print e,"monitor_AB"
		pass
	try:
		monitor_AB_st_day()
		monitor_AB_st_night()
	except Exception,e:
		print e,"monitor_AB_st_night"
		pass
	try:
		monitor_Thunder()
	except Exception,e:
		print e,"monitor_Thunder"
		pass
	try:
		account_database_isdistinct()
	except Exception,e:
		print e,"account_database_isdistinct"
		pass
	try:
		jieti_AB_isdistinct()
	except Exception,e:
		print e,"jieti_AB_isdistinct"
		pass
	break
	time.sleep(50)
	mytime=int(datetime.datetime.now().strftime('%H%M'))
	if (mytime>=2000 and mytime<=2010) or (mytime>=300 and mytime<=710):
		break