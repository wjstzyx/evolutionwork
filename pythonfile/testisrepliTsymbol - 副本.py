#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms03 = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")

# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def test_replicate(ms):
	sql="select sum(1)as num ,StockDate,symbol  from TSymbol_15min group by StockDate,Symbol having sum(1)!=1"
	res=ms.dict_sql(sql)
	for item in res:
		StockDate=item['StockDate']
		symbol=item['symbol']
		sql="select id,O,C,H,L,V,OPI from TSymbol_15min where StockDate='%s' and symbol='%s' order by id desc " % (StockDate,symbol)
		record=ms.find_sql(sql)
		cankao=record[0][1:]
		for i in range(1,item['num']):
			if record[i][1:]==cankao:
				sql='delete from TSymbol_15min where id=%s' % (record[i][0])
				print sql
				ms.insert_sql(sql)
			else:
				print "--NOT SAME"
				print record[i]
				sql='delete from TSymbol_15min where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)



test_replicate(ms05)



