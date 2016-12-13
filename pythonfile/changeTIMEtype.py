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
			


def changeTimetype(tablename):
	if tablename in ('Tsymbol','TSymbol_alltime','TSymbol_quotes_backup'):
		sql="select id,D,T,stockdate,symbol from %s where stockdate>'2015-05-20 13:00:00.000'" % (tablename)
		res=ms.dict_sql(sql)
		for item in res:
			stockdate=str(item['stockdate'])
			newD=stockdate[0:4]+'/'+stockdate[5:7]+'/'+stockdate[8:10]
			newT=stockdate[11:16]
			if len(item['D'])!=10 or len(item['T'])!=5 or newD!=item['D'] or newT!=item['T']:
				print item['symbol'] 
				sql="update Tsymbol set D='%s',T='%s' where id=%s" % (newD,newT,item['id'])
				print sql 
				ms.insert_sql(sql)
				scroptsql="update Tsymbol set D='%s',T='%s' where id=%s and symbol='%s' ;" % (item['D'],item['T'],item['id'],item['symbol'])
				# print scroptsql
			




# changeTimetype()
# ('Tsymbol','TSymbol_alltime','TSymbol_quotes_backup')
changeTimetype("TSymbol_quotes_backup")
# changeTimetype("TSymbol_alltime")