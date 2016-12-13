#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

def main_fun():
	now=datetime.datetime.now().strftime('%H%M%S')
	now=int(now)
	print now
	if now>=180000 and now<=180200:		
		sql="  select  a.D from (  select distinct  REPLACE(D,'/','') as D from TSymbol)a   left join [LogRecord].[dbo].[get_quotes_date] b   on a.D=b.date    WHERE b.date is null   order by a.D DESC"
		res=ms.dict_sql(sql)
		for item in res[2:]:
			newD= item['D']
			cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/get_quotes_from_ftp_daily.py %s' % (newD)
			sql="select * from [LogRecord].[dbo].[task_todo] where type='datafix' and cmd='%s' and status=0" % (cmd)
			print sql 
			res=ms.dict_sql(sql)
			if res:
				msg="已经插入过该补全数据任务，该任务将在16:00执行"
			else:
				sql="insert into [LogRecord].[dbo].[task_todo](type,cmd,todotime,status) values('datafix','%s','1550',0)" % (cmd)
				ms.insert_sql(sql)
				msg="成功插入定时任务，任务将在16:00执行"
main_fun()