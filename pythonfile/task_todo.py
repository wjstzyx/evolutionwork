#coding=utf-8 
#!/usr/bin/env python
import urllib, urllib2, json
import sys
import datetime
import os 
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


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

