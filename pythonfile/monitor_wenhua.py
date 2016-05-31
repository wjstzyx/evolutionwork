#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList




def monitor_wenhua():
	#查询发件人
	sql="select email from [LogRecord].[dbo].[mailtolist] where istomail=1"
	reslist=ms.find_sql(sql)
	mailtolist=''
	for item in reslist:
		mailtolist=mailtolist+','+item[0]
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
				if (getnow-lasttime).seconds>180:
					subject='%s文华数据采集产生延迟' % (symbol)
					msg='%s 文华数据采集产生延迟' % (symbol)
					sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime) values('%s','%s','%s',%s,getdate())" % (subject,mailtolist,msg,0)
					ms.insert_sql(sql)
		else:	
			# print starttime
			# print endtime
			# print nowtime
			pass



def monitor_AB():
	#查询发件人
	sql="select email from [LogRecord].[dbo].[mailtolist] where istomail=1"
	reslist=ms.find_sql(sql)
	mailtolist=''
	for item in reslist:
		mailtolist=mailtolist+','+item[0]
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
				print lasttime
				print getnow
				if (getnow-lasttime).seconds>50:
					subject='%s AB程序出错' % (symbol)
					msg='%s AB程序出错' % (symbol)
					sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime) values('%s','%s','%s',%s,getdate())" % (subject,mailtolist,msg,0)
					ms.insert_sql(sql)
		else:	
			# print starttime
			# print endtime
			# print nowtime
			pass



def monitor_Thunder():
	#查询发件人
	sql="select email from [LogRecord].[dbo].[mailtolist] where istomail=1"
	reslist=ms.find_sql(sql)
	mailtolist=''
	for item in reslist:
		mailtolist=mailtolist+','+item[0]
	# print mailtolist
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
			#检测最新更新时间与当时的时间差，如果相差60s就报警
			sql="SELECT TOP 1 UpdateTime   FROM [Future].[dbo].[Trading_ABMonitor] WHERE ComputerName='%s' and IFMonitor=1" % (symbol)
			res=ms.find_sql(sql)
			if res:
				lasttime=res[0][0]
				print lasttime
				print getnow
				if (getnow-lasttime).seconds>60:
					subject='%s Thunder程序出错' % (symbol)
					msg='%s Thunder程序出错' % (symbol)
					sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime) values('%s','%s','%s',%s,getdate())" % (subject,mailtolist,msg,0)
					ms.insert_sql(sql)
		else:	
			# print starttime
			# print endtime
			# print nowtime
			pass






while(1):
	monitor_wenhua()
	monitor_AB()
	time.sleep(60)