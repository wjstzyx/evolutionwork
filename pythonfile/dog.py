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


def is_monitor_info():
	sql="SELECT a.id,a.[type],a.[item]+'_'+b.Symbol as item  ,a.[msg], b.Symbol,classcode ,convert(nvarchar,[inserttime],120) as updatetime FROM [LogRecord].[dbo].[all_monitor_info] a inner join symbol_id b on substring(a.item,CHARINDEX('_',a.item)+1,3)=b.S_ID and len(b.Symbol)<3 where isactive=1 and issolved=0 order by updatetime"
	res=ms.dict_sql(sql)
	if res:
		return 1
	else:
		return 0

print is_monitor_info()
