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

# sql="select * from [LogRecord].[dbo].[AccountsBalance] where [deposit]>0 and date='20161014'  order by userid"
# res=ms.dict_sql(sql)
# for item in res:
# 	deposit=item['deposit']
# 	sql="update [LogRecord].[dbo].[AccountsBalance] set [Withdraw]=Withdraw-%s,[CloseBalance]=[CloseBalance]+%s where userid='%s' and date<20161014"  % (deposit,deposit,item['userid'])
# 	print sql 
# 	ms.insert_sql(sql)

def aaaa():
	sql="select distinct userid from [LogRecord].[dbo].[AccountsBalance] where date<=20161013 order by userid"
	res=ms.dict_sql(sql)
	for item1 in res:
		userid=item1['userid']
		sql="select * from [LogRecord].[dbo].[AccountsBalance] where date<=20161013 and userid='%s' order by date" % (userid)
		res1=ms.dict_sql(sql)
		firstvalue=res1[0]['CloseBalance']
		for item in res1[1:]:
			numid=item['numid']
			newdoposit=round(item['CloseBalance']+item['Withdraw']+item['Commission']-item['PositionProfit']-firstvalue,1)
			firstvalue=item['CloseBalance']
			sql="update [LogRecord].[dbo].[AccountsBalance] set deposit=%s where numid=%s" % (newdoposit,numid)
			ms.insert_sql(sql)
			print sql 


aaaa()




