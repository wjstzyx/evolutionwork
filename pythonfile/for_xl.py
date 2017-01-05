#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


def get_close():
	sql="select distinct symbol from Tsymbol order by symbol"
	res=ms.dict_sql(sql)
	quotes={}
	for item in res:
		sql="select top 2 symbol,C from Tsymbol where symbol='%s' order by stockdate" % (item['symbol'])
		tempres=ms.dict_sql(sql)
		quotes[item['symbol']]=[round(tempres[0]['C'],2),round(tempres[1]['C'],2)]
	print quotes
	#[last,pre]

def get_last_position():
	sql="select symbol,P  FROM [Future].[dbo].[Trading_logSymbolTest] where st like '%CCIreversal_5_stair1_'"
	res=ms.dict_sql(sql)
	print res


get_close()
get_last_position()