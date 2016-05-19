#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def test_replicate():
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
				print sql
				ms.insert_sql(sql)
			else:
				print "--NOT SAME"
				print record[i]
				sql='delete from Tsymbol where id=%s' % (record[i][0])
				print sql
				ms.insert_sql(sql)



test_replicate()


# def backup_AU():
# 	#Symbol='AU' and StockDate>'2015-05-22 11:10:00.000'
# 	sql="select id,D,StockDate from Tsymbol where symbol='AU' and StockDate>='2015-06-19 11:23:00.000' order by StockDate"
# 	#sql="select a.id,a.D,a.StockDate from Tsymbol a inner join (select top 20 sum(1)as num ,StockDate,symbol  from Tsymbol group by StockDate,Symbol having sum(1)!=1) temp on a.Symbol=temp.Symbol and a.StockDate=temp.StockDate"
# 	res=ms.dict_sql(sql)
# 	for item in res:
# 		if item['D']=='2015/05/22':
# 			StockDate=item['StockDate']
# 			sql="select year('%s')" % (StockDate)
# 			year=ms.find_sql(sql)[0][0]
# 			sql="select month('%s')" % (StockDate)
# 			month=ms.find_sql(sql)[0][0]
# 			sql="select day('%s')" % (StockDate)
# 			day=ms.find_sql(sql)[0][0]
# 			newD=str(year)+'/'+str(month).zfill(2)+'/'+str(day).zfill(2)
# 			sql="update Tsymbol set D='%s' where id=%s and symbol='AU' and StockDate='%s'" % (newD,item['id'],StockDate)
# 			# print sql
# 			ms.insert_sql(sql)




# backup_AU()
