#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import os 
import re
import shutil
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


def main_fun():
	sql="SELECT distinct address  FROM [LogRecord].[dbo].[ST_heart] where type =1 order by address"
	res=ms.dict_sql(sql)
	for item in res:
		print item 
		#sql="insert into [LogRecord].[dbo].[temp_afl_heart] select ac,F_ac,'%s' as address from p_follow where F_ac in (select distinct ac from P_BASIC where st in (select st from [LogRecord].[dbo].[ST_heart] where address='%s' ))" % (item['address'],item['address'])
		sql="insert into [LogRecord].[dbo].[temp_afl_heart] select distinct 'aa',ac,'%s' from P_BASIC where st in (select st from [LogRecord].[dbo].[ST_heart] where address='%s' )" % (item['address'],item['address'])
		ms.insert_sql(sql)
main_fun()