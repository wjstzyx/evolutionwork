#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
import time
import datetime
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
from sendmail import send_mail
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# mailreslut=send_mail(mailtolist,totalsubject,totalmsg)
def st_heart():
	##报警超过3分钟的st
	sql="SELECT  [id]     ,[st]    ,DATEDIFF(MINUTE, [stockdate], getdate()) as timediff   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3  order by timediff desc"
	res=ms.dict_sql(sql)
	message=''
	mailtolist=['yuyang@evolutionlabs.com.cn','beilei@evolutionlabs.com.cn']
	totalsubject='AB策略卡死报警'+datetime.datetime.now().strftime("%H:%M:%S")
	if res:
		for item in res:
			st=item['st']
			timediff=item['timediff']
			message=message+'策略号 '+str(st)+': '+' 卡死时间: '+str(timediff)+'(分钟)'
	if message !='':
		totalmsg=message
		mailreslut=send_mail(mailtolist,totalsubject,totalmsg)
		print mailreslut

while(1):
	st_heart()
	print 1
	time.sleep(90)