#coding=utf-8 
#!/usr/bin/env python
import sys
import time
import datetime
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
#sql="SELECT distinct st  FROM [LogRecord].[dbo].[Trading_logTrade] where  systemtime>'2016-07-07 15:31:00.000' "
# sql="select distinct st from   [LogRecord].[dbo].[Trading_logTrade] where   systemtime>'2016-07-07 15:31:00.000' and systemtime<'2016-07-07 18:31:00.000' "
# res=ms.dict_sql(sql)
# for item in res:
# 	sql="select p from [LogRecord].[dbo].[Trading_logTrade] where st='%s' and systemtime <'2016-07-07 16:00:03.000' order by  systemtime desc" % (item['st'])
# 	res1=ms.dict_sql(sql)
# 	if res1:
# 		sql="select top 1 p from [Future].[dbo].[Trading_logSymbol] where st='%s'" % (item['st'])
# 		res2=ms.dict_sql(sql)[0]['p']
# 		if res1[0]['p']!=res2:
# 			print item['st']

		# sql="update [Future].[dbo].[Trading_logSymbol] set P=%s where st=%s" % (res1[0]['p'],item['st'])
		# print sql 
		#ms.insert_sql(sql)

mytime=int(datetime.datetime.now().strftime('%H%M'))
print mytime

