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
sql="select t.ST,t.P,t.tradetime, sys.fn_VarBinToHexStr(HashBytes('MD5',t.TradName))  as tradename from P_BASIC p inner join p_follow pp on p.AC=pp.F_ac and pp.AC='StepMultiI300w'inner join Trading_logSymbol t on p.ST=t.ST and pp.AC='StepMultiI300w'"
res=ms.dict_sql(sql)
print res 