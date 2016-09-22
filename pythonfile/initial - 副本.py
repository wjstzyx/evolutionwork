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
accountlist=[]
sql="select distinct f_ac from p_follow where f_ac not in (select distinct ac from p_follow where ac is not null) and F_ac not in (select distinct ac from P_BASIC)"
res=ms.dict_sql(sql)
for item in res:
	sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  [Future].[dbo].[p_follow] WHERE   f_ac='%s' UNION ALL SELECT   D.AC,D.F_ac,D.ratio FROM   Emp      INNER JOIN [Future].[dbo].[p_follow]d ON d.f_ac = Emp.ac  )     select distinct ac  from Emp " % (item['f_ac'])
	res1=ms.dict_sql(sql)
	for item1 in res1:
		accountlist.append(item1['ac'])
print len(accountlist)
accountlist=list(set(accountlist))
print len(accountlist)
for item in accountlist:
	print item 

