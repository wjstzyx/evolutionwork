#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
try:
	ms03 = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")
except:
	pass






# try:
# 	mscloud = MSSQL(host="139.196.190.246",user="future",pwd="K@ra0Key",db="future")
# except:
# 	pass

# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

try:
	cmd='sudo ntpdate pool.ntp.org'
	os.system(cmd)
except:
	pass
print 'Next task'



try:
	sql="delete from [Future].[dbo].[TSymbol] where DATEDIFF(day,[StockDate],GETDATE())>130"
	ms03.insert_sql(sql)
	# ms07.insert_sql(sql)
	# mscloud.insert_sql(sql)
except Exception,e:
	ms1 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	subject="清理Tsymbol定时任务出错"+datetime.datetime.now().strftime("%H:%M:%S")
	mailtolist="yuyang@evolutionlabs.com.cn"
	message=str(e).replace("'",'#')
	sendmessage="13764504303"
	sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,message,0,sendmessage)
	ms1.insert_sql(sql)