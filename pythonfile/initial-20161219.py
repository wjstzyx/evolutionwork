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


def main_fun():
	sql="select distinct ac from dailyquanyi_V2 where ac  in (select f_ac from p_follow where ac ='StepMultiI300w')and D in ('161202','161205')"
	res=ms.dict_sql(sql)
	for item in res:
		sql="select quanyi*ratio/10*2 as quanyi from dailyquanyi_V2 a inner join p_follow p on a.ac=p.f_AC  where a.ac='%s' and p.AC='StepMultiI300w' and a.D in ('161202','161205') order by a.D desc" % (item['ac'])
		temp=ms.dict_sql(sql)
		firstv=0
		secondv=0
		diffv=0
		diffv=round(temp[0]['quanyi']-temp[1]['quanyi'],0)
		print item['ac']+','+str(diffv)



main_fun()
