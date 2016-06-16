#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
import datetime
import time
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
from sendmail import send_mail
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="LogRecord")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
#id	subject	mailtolist	msg	type	inserttime	updatetime
#1	dddddd2	794513386@qq.com,yuyang@evolutionlabs.com.cn,yuyang_998@sina.com	dfdfdd	1	2016-05-25 14:59:15.170	2016-05-25 14:59:16.887

def read_maillist():
	sql="select * from [LogRecord].[dbo].[maillist] where type=0 or type=2 "
	res=ms.dict_sql(sql)
	for item in res:
		sql="update [LogRecord].[dbo].[maillist] set type=3,updatetime=getdate() where id=%s" % (item['id'])
		ms.insert_sql(sql)
		mailtolist=item['mailtolist'].split(',')
		print mailtolist
		msg=item['msg']
		subject=item['subject']+datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
		msg=item['inserttime'].strftime('%Y-%m-%d %H-%M-%S')+'<br>message: '+item['msg']+'</br>'
		#一小时最多发10封
		sql="select top 1 * from [LogRecord].[dbo].[maillist] where msg='%s' and type=1 order by id desc " % (item['msg'])
		tempres=ms.find_sql(sql)
		print tempres,"222"
		if tempres:
			lasttime=tempres[0][6]
			seconds=(datetime.datetime.now()-lasttime).seconds
			print seconds,type(seconds)
			if seconds<310:
				print "时间少于半小时，不再发送"
				sql="update [LogRecord].[dbo].[maillist] set ms01g=msg+' 经过 %s 秒',updatetime=getdate() where id=%s" % (seconds,item['id'])
				ms.insert_sql(sql)
			else:
				print "时间大于半小时，准备发送"
				if send_mail(mailtolist,subject,msg):
					sql="update [LogRecord].[dbo].[maillist] set type=1,updatetime=getdate() where id=%s" % (item['id'])
					ms.insert_sql(sql)
					print "发送成功"  
				else:
					sql="update [LogRecord].[dbo].[maillist] set type=2,updatetime=getdate() where id=%s" % (item['id'])
					ms.insert_sql(sql)
					print "发送失败"
		else:
			print "else"
			if send_mail(mailtolist,subject,msg):
				sql="update [LogRecord].[dbo].[maillist] set type=1,updatetime=getdate() where id=%s" % (item['id'])
				ms.insert_sql(sql)
				print "发送成功"  
			else:
				sql="update [LogRecord].[dbo].[maillist] set type=2,updatetime=getdate() where id=%s" % (item['id'])
				ms.insert_sql(sql)
				print "发送失败"


i=0
while(1):
	read_maillist()
	time.sleep(2)	



