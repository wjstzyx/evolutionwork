#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

#变化量变成累积量
sql="SELECT SUM(1)as sum,userid,date  FROM [LogRecord].[dbo].[AccountsBalance] group by userid,date having SUM(1) =2"
res=ms.dict_sql(sql)
for item in res:
	sql="select top 2 * from [LogRecord].[dbo].[AccountsBalance] where userid='%s' and date='%s'" % (item['userid'],item['date'])
	res1=ms.dict_sql(sql)
	print res1
