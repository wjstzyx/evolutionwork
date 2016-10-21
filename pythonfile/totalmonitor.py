#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import datetime
import time
from sendSMSM import sendsms
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


#采集行情的心跳监测
#监控时间段：在crontab 设置 08:00---23:00,延迟2分钟报警
def monitor():
	nowtime=datetime.datetime.now().strftime("%H%M")
	nowtime=int(nowtime)
	dayOfWeek = datetime.datetime.now().weekday()
	if dayOfWeek in (0,1,2,3,4) and nowtime>=800 and nowtime<2330:
		sql="select DATEDIFF(MINUTE, updatetime, getdate()) as aaa from [LogRecord].[dbo].[quotes_python_heart]where type='quotes_python'  and name='catchquotesall'and isactive=1"
		res=ms.dict_sql(sql)
		if res[0]['aaa']>=2:
			sendmessage='13764504303'
			totalsubject="行情脚本没有心跳"
			smsresult=sendsms(sendmessage,totalsubject)
			print 'have send 1'
			# print smsresult


def monitor_future_account():
	nowtime=datetime.datetime.now().strftime("%H%M")
	nowtime=int(nowtime)
	dayOfWeek = datetime.datetime.now().weekday()
	if dayOfWeek in (0,1,2,3,4) and nowtime>=1430 and nowtime<1520:
		sql="select DATEDIFF(MINUTE, updatetime, getdate()) as aaa from [LogRecord].[dbo].[quotes_python_heart]where type='regular_task'  and name='future_account'and isactive=1"
		res=ms.dict_sql(sql)
		if res[0]['aaa']>=7:
			sendmessage='13764504303,13918972855'
			totalsubject="期货账户采集脚本停止"
			smsresult=sendsms(sendmessage,totalsubject)
			print 'have send 2'
		# print smsresult


monitor()
# monitor_future_account()



