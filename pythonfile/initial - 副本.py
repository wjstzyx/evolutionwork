#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


def get_symbol_quotes(symbol,num=3):
	sql="SELECT top(%s) [Symbol]  ,[O]  ,[C]  ,[H]  ,[L]  ,[V]  ,[OPI]  ,[D]  ,[T]  ,[StockDate]   ,[refc] FROM [Future].[dbo].[TSymbol] where symbol='%s' order by StockDate " % (num,symbol)
	res=ms.dict_sql(sql)
	print res 
	return res

def write_signal(p,st,stockdate,price,TradName,Period,TickNum,mysymbol):
	# _a_Trading_signal_python @p,@st,@stockdate,@price,@TradName,@Period,@TickNum,@mysymbol
	#建议将上百个SQL 用‘;’分隔 拼接后 执行
	sql="_a_Trading_signal_python %s,'%s','%s',%s,'%s',%s,'%s','%s'" % (p,st,stockdate,price,TradName,Period,TickNum,mysymbol)
	print sql 
	#ms.insert_sql(sql)

get_symbol_quotes('rb')
write_signal(1,10012,'2016-01-01 10:32:00',233,'2222232ds',21,'095610','rb')
