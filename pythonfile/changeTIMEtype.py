#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList




def changeTimetype():
	sql="select id,D,T,stockdate,symbol from Tsymbol where stockdate>'2015-05-20 13:00:00.000'"
	res=ms.dict_sql(sql)
	for item in res:
		stockdate=str(item['stockdate'])
		newD=stockdate[0:4]+'/'+stockdate[5:7]+'/'+stockdate[8:10]
		newT=stockdate[11:16]
		if len(item['D'])!=10 or len(item['T'])!=5 or newD!=item['D'] or newT!=item['T']:
			print item['symbol'] 
			sql="update Tsymbol set D='%s',T='%s' where id=%s" % (newD,newT,item['id'])
			ms.insert_sql(sql)
			scroptsql="update Tsymbol set D='%s',T='%s' where id=%s and symbol='%s' ;" % (item['D'],item['T'],item['id'],item['symbol'])
			print scroptsql
			


def changeTimetype(ms,tablename):
	if tablename in ('Tsymbol','TSymbol_alltime','TSymbol_quotes_backup','TSymbol_allfuture'):
		sql="select distinct symbol from %s order by symbol" % (tablename)
		symbollist=ms.dict_sql(sql)
		for item in symbollist:
			print item['symbol']
			sql="select id,D,T,stockdate,symbol from %s where symbol='%s' and stockdate>'2015-05-20 13:00:00.000'" % (tablename,item['symbol'])
			res=ms.dict_sql(sql)
			totalsql=""
			ii=0
			for item in res:
				stockdate=str(item['stockdate'])
				newD=stockdate[0:4]+'/'+stockdate[5:7]+'/'+stockdate[8:10]
				newT=stockdate[11:16]
				if len(item['D'])!=10 or len(item['T'])!=5 or newD!=item['D'] or newT!=item['T']:
					print item['symbol'] 
					sql="update %s set D='%s',T='%s' where id=%s;" % (tablename,newD,newT,item['id'])
					print sql 
					totalsql=totalsql+sql
					ii=ii+1
					if ii>1000:
						print ii
						ms.insert_sql(totalsql)
						totalsql=""
						ii=0
			if len(totalsql)>10:
				print 'do'
				ms.insert_sql(totalsql)
				totalsql=""
				ii=0


# changeTimetype()
# ('Tsymbol','TSymbol_alltime','TSymbol_quotes_backup','TSymbol_allfuture')
changeTimetype(ms,"TSymbol_allfuture")
# changeTimetype("TSymbol_alltime")