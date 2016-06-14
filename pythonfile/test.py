#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

sql="  select st from [LogRecord].[dbo].[Trading_logTrade]   group by st   order by SUM(1) desc"
res=ms.find_sql(sql)
str=""
for item in res:
	temp=item[0]
	str=str+" "+temp
print str