#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-



sql="select distinct D from p_log where D<160601 order by D"
res=ms.dict_sql(sql)
for item in res:
	D= item['D']
	sql="delete from p_log where D<=%s" % (D)
	ms.insert_sql(sql)
	print sql
	time.sleep(1)
