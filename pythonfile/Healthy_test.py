#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms03 = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")
ms07 = MSSQL(host="192.168.0.7",user="future",pwd="K@ra0Key",db="future")
mscloud = MSSQL(host="139.196.190.246",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


#判断虚拟组配置是否正确
def is_acname_ok():
	sql="select distinct p.ac from p_basic p left join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock where a.AC is null order by p.ac"
	res=ms05.dict_sql(sql)
	if res:
		print "以下虚拟组在 P_basic 中存在，在 AC_RATIO 中不存在，请确认配置是否正确"
		for item in res:
			print item['ac']
	else:
		print "is_acname_ok OK"

#Tsymbol 是否存在重复
def is_Tsymbol_multi(ms,type=""):
	sql="select sum(1)as num ,StockDate,symbol  from Tsymbol group by StockDate,Symbol having sum(1)!=1"
	res=ms.dict_sql(sql)
	if res:
		print " %s Tsymbol 中存在重复的行" % (type)
	sql="select sum(1)as num ,StockDate,symbol  from TSymbol_quotes_backup group by StockDate,Symbol having sum(1)!=1"
	res=ms.dict_sql(sql)
	if res:
		print " %s TSymbol_quotes_backup 中存在重复的行" % (type)
	sql="select sum(1)as num ,StockDate,symbol  from TSymbol_alltime group by StockDate,Symbol having sum(1)!=1"
	res=ms.dict_sql(sql)
	if res:
		print " %s TSymbol_alltime 中存在重复的行" % (type)


#p_basic与p_follow配置是否有冗余，删除p_basic中没有，而p_follow中存在的记录
def is_rongyu():
	sql="select * from p_follow where f_ac in (select distinct F_ac from p_follow where F_ac not in (select distinct ac from p_follow) and  F_ac not in (select distinct ac from P_BASIC ))"
	res=ms05.dict_sql(sql)
	for item in res:
		print "冗余配置信息"
		print item 
	# sql="delete from p_follow where f_ac in (select distinct F_ac from p_follow where F_ac not in (select distinct ac from p_follow) and  F_ac not in (select distinct ac from P_BASIC ))"
	# ms05.inert_sql(sql)

is_acname_ok()
is_Tsymbol_multi(ms05,type="05")
is_Tsymbol_multi(ms03,type="03")
is_Tsymbol_multi(ms07,type="07")
is_Tsymbol_multi(mscloud,type="mscloud")
is_rongyu()