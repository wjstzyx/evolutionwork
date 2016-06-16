#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
import datetime
import time
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
from sendmail import send_mail
from sendSMSM import sendsms
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="LogRecord")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
#id	subject	mailtolist	msg	type	inserttime	updatetime
#1	dddddd2	794513386@qq.com,yuyang@evolutionlabs.com.cn,yuyang_998@sina.com	dfdfdd	1	2016-05-25 14:59:15.170	2016-05-25 14:59:16.887

def read_maillist():
	sql="select * from [LogRecord].[dbo].[maillist] where type=0 "
	res=ms.dict_sql(sql)
	##组织待发送的内容
	mailtolist=''
	sendmessage=''
	totalmsg=''
	totalsubject=''
	for item in res:
		sql="update [LogRecord].[dbo].[maillist] set type=3,updatetime=getdate() where id=%s" % (item['id'])
		ms.insert_sql(sql)
		mailtolist=item['mailtolist'].split(',')
		sendmessage=item['sendmessage']
		msg=item['msg']
		totalsubject=totalsubject+'\r\n'+item['subject']
		totalmsg=totalmsg+'<br>'+item['msg']+'</br>'
	totalmsg=totalmsg+datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
	totalsubject=totalsubject[:45]+'\r\n'+datetime.datetime.now().strftime('%m-%d %H:%M:%S')
	totalsubject=totalsubject.strip('\r\n')


	#一小时最多发12封
	if mailtolist!='':
		sql="select top 1 * from [LogRecord].[dbo].[maillist] where type=1 order by id desc "
		tempres=ms.dict_sql(sql)
		if tempres:
			lasttime=tempres[0]['updatetime']
			seconds=(datetime.datetime.now()-lasttime).seconds
			print seconds,type(seconds)
			if seconds<310:
				print "时间少于5分钟,不再发送"
				sql="update [LogRecord].[dbo].[maillist] set type=4,updatetime=getdate() where type=3"
				ms.insert_sql(sql)
			else:
				print "时间大于5分钟，准备发送"
				mailreslut=send_mail(mailtolist,totalsubject,totalmsg)
				smsresult=sendsms(sendmessage,totalsubject)

				if smsresult==1:
					sql="update [LogRecord].[dbo].[maillist] set type=1,updatetime=getdate() where type=3"
					ms.insert_sql(sql)
					print "发送成功"  
				else:
					sql="update [LogRecord].[dbo].[maillist] set type=2,updatetime=getdate() where type=3"
					ms.insert_sql(sql)
					print "发送失败"
		else:
			print "else"
			mailreslut=send_mail(mailtolist,totalsubject,totalmsg)
			smsresult=sendsms(sendmessage,totalsubject)
			if smsresult==1:
				sql="update [LogRecord].[dbo].[maillist] set type=1,updatetime=getdate() where type=3"
				ms.insert_sql(sql)
				print "发送成功1"  
			else:
				sql="update [LogRecord].[dbo].[maillist] set type=2,updatetime=getdate() where type=3"
				ms.insert_sql(sql)
				print "发送失败1"


i=0
while(1):
	read_maillist()
	time.sleep(2)	



