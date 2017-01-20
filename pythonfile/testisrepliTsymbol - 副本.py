#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms03 = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")
#ms07 = MSSQL(host="192.168.0.7",user="future",pwd="K@ra0Key",db="future")

# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def test_replicate(ms):
	sql="select sum(1)as num ,StockDate,symbol  from Tsymbol group by StockDate,Symbol having sum(1)!=1"
	res=ms.dict_sql(sql)
	for item in res:
		StockDate=item['StockDate']
		symbol=item['symbol']
		sql="select id,O,C,H,L,V,OPI,D,T from Tsymbol where StockDate='%s' and symbol='%s' order by id desc " % (StockDate,symbol)
		record=ms.find_sql(sql)
		cankao=record[0][1:]
		for i in range(1,item['num']):
			if record[i][1:]==cankao:
				sql='delete from Tsymbol where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)
			else:
				print "--NOT SAME"
				print record[i]
				sql='delete from Tsymbol where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)


def test_replicate_backup(ms):
	sql="select sum(1)as num ,StockDate,symbol  from TSymbol_quotes_backup group by StockDate,Symbol having sum(1)!=1"
	res=ms.dict_sql(sql)
	for item in res:
		StockDate=item['StockDate']
		symbol=item['symbol']
		sql="select id,O,C,H,L,V,OPI,D,T from TSymbol_quotes_backup where StockDate='%s' and symbol='%s' order by id desc " % (StockDate,symbol)
		record=ms.find_sql(sql)
		cankao=record[0][1:]
		for i in range(1,item['num']):
			if record[i][1:]==cankao:
				sql='delete from TSymbol_quotes_backup where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)
			else:
				print "--NOT SAME"
				print record[i]
				sql='delete from TSymbol_quotes_backup where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)


def test_replicate_alltime(ms):
	sql="select sum(1)as num ,StockDate,symbol  from TSymbol_alltime group by StockDate,Symbol having sum(1)!=1"
	res=ms.dict_sql(sql)
	for item in res:
		StockDate=item['StockDate']
		symbol=item['symbol']
		sql="select id,O,C,H,L,V,OPI,D,T from TSymbol_alltime where StockDate='%s' and symbol='%s' order by id desc " % (StockDate,symbol)
		record=ms.find_sql(sql)
		cankao=record[0][1:]
		for i in range(1,item['num']):
			if record[i][1:]==cankao:
				sql='delete from TSymbol_alltime where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)
			else:
				print "--NOT SAME"
				print record[i]
				sql='delete from TSymbol_alltime where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)

def test_replicate_TSymbol_allfuture(ms):
	sql="select sum(1)as num ,StockDate,symbol  from TSymbol_allfuture group by StockDate,Symbol having sum(1)!=1"
	res=ms.dict_sql(sql)
	for item in res:
		StockDate=item['StockDate']
		symbol=item['symbol']
		sql="select id,O,C,H,L,V,OPI,D,T from TSymbol_allfuture where StockDate='%s' and symbol='%s' order by id desc " % (StockDate,symbol)
		record=ms.find_sql(sql)
		cankao=record[0][1:]
		for i in range(1,item['num']):
			if record[i][1:]==cankao:
				sql='delete from TSymbol_allfuture where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)
			else:
				print "--NOT SAME"
				print record[i]
				sql='delete from TSymbol_allfuture where id=%s' % (record[i][0])
				#print sql
				ms.insert_sql(sql)



test_replicate_TSymbol_allfuture(ms05)


