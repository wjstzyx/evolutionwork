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

def read_maillist():
	sql="select * from [LogRecord].[dbo].[maillist] where type !=1 "
	res=ms.dict_sql(sql)
	if res:
		mailtolist=res[0]['mailtolist'].split(',')
		print mailtolist
		totalmsg=''
		idlist=[]
		for item in res:
			msg=item['msg']
			idlist.append(item['id'])
			totalmsg=totalmsg+'<br>'+item['inserttime'].strftime('%Y-%m-%d %H-%M-%S')+'<br>subject : '+item['subject']+'<br>message: '+item['msg']+'</br>'
		print totalmsg
		if send_mail(mailtolist,"夜盘报警提醒",totalmsg):
			for item in idlist:
				sql="update [LogRecord].[dbo].[maillist] set type=1,updatetime=getdate() where id=%s" % (item)
				ms.insert_sql(sql)
			print "发送成功"  
		else:
			for item in idlist:
				sql="update [LogRecord].[dbo].[maillist] set type=2,updatetime=getdate() where id=%s" % (item)
				ms.insert_sql(sql)
			print "发送失败"


i=0
while(1):
	read_maillist()
	time.sleep(2)	



