#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

#test

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



def test_issignal():
	print datetime.datetime.now()
	sql="SELECT id,p,st,systemtime  FROM [Future].[dbo].[Trading_logSymbol] where ((DATEPART(hour,systemtime)>15 and DATEPART(hour,systemtime)<=20) or (DATEPART(hour,systemtime)=15 and DATEPART(MINUTE,systemtime)>30)) and systemtime>'2016-07-09' order by systemtime desc"
	res=ms.dict_sql(sql)
	if res:
		for item in res:
			id=item['id']
			p=item['p']
			st=item['st']
			systemtime=item['systemtime']
			backupsql="update [Future].[dbo].[Trading_logSymbol] set p=%s where id=%s and st='%s'" % (p,id,st)
			#查找真实的记录
			sql="SELECT TOP 1 P,ST,systemtime  FROM [LogRecord].[dbo].[Trading_logTrade] where st='%s'  and systemtime<'%s'  and (DATEPART(HOUR,systemtime)<15 or DATEPART(HOUR,systemtime)=15 and DATEPART(MINUTE,systemtime)<=30)order by id  desc" % (st,systemtime)
			res1=ms.dict_sql(sql)
			if res1:
				originP=res1[0]['P']
				todosql="update [Future].[dbo].[Trading_logSymbol] set p=%s where id=%s and st='%s'" % (originP,id,st)
				ms.insert(todosql)
				print backupsql
		return 1
	else:
		return 0





def sendmsgfun():
	(mailtolist,sendmessage)=get_messagelist()
	subject='收盘后有信号写入'+datetime.datetime.now().strftime("%H:%M:%S")
	refsql="SELECT id,p,st,systemtime  FROM [Future].[dbo].[Trading_logSymbol] where ((DATEPART(hour,systemtime)>15 and DATEPART(hour,systemtime)<=20) or (DATEPART(hour,systemtime)=15 and DATEPART(MINUTE,systemtime)>30)) and systemtime>2016-07-09 order by systemtime desc"
	message="收盘后有信号写入,具体请参考日志\r\n"+refsql
	sql="insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject,mailtolist,message,0,sendmessage)
	ms.insert_sql(sql)



# test_issignal()

#检测是否在15:30--20:00之间有变化
#如果有变化则将信号置为15:30前最新的那个信号，并将恢复脚本保存下来
#短信通知仓位有变动
#检测频率  crontab 控制


result=test_issignal()
if result==1:
	sendmsgfun()