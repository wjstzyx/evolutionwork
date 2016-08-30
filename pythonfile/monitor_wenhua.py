#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList


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
			print "have waring"
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
			print "have waring"
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
	sql="select top 1 D from TSymbol ORDER BY id desc"
	lastday=ms.find_sql(sql)[0][0]
	lastday='20'+lastday[2:4]+lastday[5:7]+lastday[8:10]
	sql="select getdate()"
	nowD=ms.find_sql(sql)[0][0].strftime('%Y%m%d')
	if nowD==lastday:
		return 1
	else:
		return 0


if ismonitorday()==0:
	exit()

print "begin"
while(1):
	try:
		monitor_wenhua()
	except:
		pass
	try:
		monitor_AB()
	except:
		pass
	try:
		monitor_AB_st_day()
		monitor_AB_st_night()
	except Exception,e:
		print e
		pass
	try:
		monitor_Thunder()
	except Exception,e:
		print e
		pass
	time.sleep(50)
	mytime=int(datetime.datetime.now().strftime('%H%M'))
	if (mytime>=2000 and mytime<=2010) or (mytime>=300 and mytime<=710):
		break