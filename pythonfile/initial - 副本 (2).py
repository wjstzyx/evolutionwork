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
sql="SELECT[primarymoney],[future_company],userid,[beizhu] FROM [LogRecord].[dbo].[Future_AccountsBalance]  where userid='红松股票' order by [ordernum]"
res=ms.dict_sql(sql)
returnlist=[]
print res 
for item in res:
	userid=item['userid']
	print "userid",userid