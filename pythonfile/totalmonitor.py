#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import datetime
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
	sql="select DATEDIFF(MINUTE, updatetime, getdate()) as aaa from [LogRecord].[dbo].[quotes_python_heart]where type='quotes_python' and isactive=1"
	res=ms.dict_sql(sql)
	if res[0]['aaa']>=2:
		sendmessage='13764504303'
		totalsubject="行情脚本没有心跳"
		smsresult=sendsms(sendmessage,totalsubject)
		# print smsresult



monitor()



