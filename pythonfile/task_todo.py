#coding=utf-8 
#!/usr/bin/env python
import urllib, urllib2, json
import sys
import datetime
from sendSMSM import sendsms
import os 
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

def monitor_position_change(acname):
	sql="select '%s' as name, Expr1  from [Future].[dbo].View_%s" % (acname,acname)
	res=ms.dict_sql(sql)
	nowposition=res[0]['Expr1']
	sql="SELECT   [lastposition]  FROM [LogRecord].[dbo].[mytemp_position] where acname='%s'" % (acname)
	res=ms.dict_sql(sql)
	if res:
		lastposition=res[0]['lastposition']
		sql=" update [LogRecord].[dbo].[mytemp_position] set lastposition=%s,inserttime=GETDATE() where acname='%s'" % (nowposition,acname)
		ms.insert_sql(sql)
	else:
		lastposition=0
		sql="insert into [LogRecord].[dbo].[mytemp_position](acname,lastposition) values('%s',%s)" % (acname,nowposition)
		ms.insert_sql(sql)


	if nowposition!=lastposition:
		print 'nowposition',nowposition
		print 'lastposition',lastposition
		#发送邮件
		subject=" %s 仓位为 %s " % (acname,nowposition)+datetime.datetime.now().strftime("%H:%M:%S")
		# mailtolist="yuyang@evolutionlabs.com.cn"
		message=subject
		sendmessage=["13764504303"]
		smsresult=sendsms(sendmessage,message)
		print 'smsresult',smsresult
		# sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,message,0,sendmessage)
		# ms.insert_sql(sql)
	else:
		print 'OK'







def istasktodo(type):
	sql="select * FROM [LogRecord].[dbo].[task_todo] where type='%s' and status=0 " % (type)
	res=ms.dict_sql(sql)
	nowtime=datetime.datetime.now().strftime('%H%M')
	print nowtime
	for item in res:
		if nowtime>=item['todotime']:
			cmd=item['cmd']
			print '%s &' % (cmd)
			os.system('%s &' % (cmd))
			#置状态
			id=item['id']
			sql="update [LogRecord].[dbo].[task_todo] set status=1 where id=%s" % (id)
			ms.insert_sql(sql)
		print item 

istasktodo('datafix')
monitor_position_change('test_Pselect')
