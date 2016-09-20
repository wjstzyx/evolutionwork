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

ms03 = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")
ms07 = MSSQL(host="192.168.0.7",user="future",pwd="K@ra0Key",db="future")
mscloud = MSSQL(host="139.196.190.246",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

sql="delete  from TSymbol where DateName(second,stockdate)<>0"
ms03.insert_sql(sql)
ms07.insert_sql(sql)
mscloud.insert_sql(sql)

