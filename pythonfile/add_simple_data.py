#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList





def add_for_item_CU_before(symbol,time):
	#IFICIH
	sql=" select  a.T as at,temp.* from [timebenchmarke] a left join (select * from TSymbol where d='%s' and Symbol='%s') temp on a.T=temp.T where a.type='CU' order by a.t;" % (time,symbol)

	res=ms.dict_sql(sql)
	firstrecord=res[0]
	if firstrecord['T'] is None:
		StockDate=time+" "+firstrecord['at']
		sql="select top 1 [Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc] from Tsymbol where StockDate<'%s' and Symbol='%s' order by StockDate desc" % (StockDate,symbol)
		print sql
		lastrecord=ms.dict_sql(sql)[0]
		sql="insert into Tsymbol ([Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc])values('%s',%s,%s,%s,%s,0,%s,'%s','%s','%s',%s)" % (lastrecord['Symbol'],lastrecord['O'],lastrecord['C'],lastrecord['H'],lastrecord['L'],lastrecord['OPI'],time,firstrecord['at'],StockDate,lastrecord['C'])
		print sql
		ms.insert_sql(sql)

def add_for_item_IF_before(symbol,time):
	#IFICIH
	sql=" select  a.T as at,temp.* from [timebenchmarke] a left join (select * from TSymbol where d='%s' and Symbol='%s') temp on a.T=temp.T where a.type='IF' order by a.t;" % (time,symbol)

	res=ms.dict_sql(sql)
	firstrecord=res[0]
	if firstrecord['T'] is None:
		StockDate=time+" "+firstrecord['at']
		sql="select top 1 [Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc] from Tsymbol where StockDate<'%s' and Symbol='%s' order by StockDate desc" % (StockDate,symbol)
		print sql
		lastrecord=ms.dict_sql(sql)[0]
		sql="insert into Tsymbol ([Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc])values('%s',%s,%s,%s,%s,0,%s,'%s','%s','%s',%s)" % (lastrecord['Symbol'],lastrecord['O'],lastrecord['C'],lastrecord['H'],lastrecord['L'],lastrecord['OPI'],time,firstrecord['at'],StockDate,lastrecord['C'])
		print sql
		ms.insert_sql(sql)

def add_for_item_IF(symbol,time):
	#IFICIH
	sql=" select  a.T as at,temp.* from [timebenchmarke] a left join (select * from TSymbol where d='%s' and Symbol='%s') temp on a.T=temp.T where a.type='IF' order by a.t;" % (time,symbol)

	res=ms.dict_sql(sql)
	lastrecord=res[0]
	for item in res[1:]:
		if item['T'] is None and lastrecord['T'] is not None:
			StockDate=str(lastrecord['D'])+" "+item['at']
			sql="insert into Tsymbol ([Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc])values('%s',%s,%s,%s,%s,0,%s,'%s','%s','%s',%s)" % (lastrecord['Symbol'],lastrecord['O'],lastrecord['C'],lastrecord['H'],lastrecord['L'],lastrecord['OPI'],lastrecord['D'],item['at'],StockDate,lastrecord['C'])
			print sql
			ms.insert_sql(sql)
		else:
			lastrecord=item


def add_for_item_CU(symbol,time):
	#IFICIH
	sql="select  a.T as at,temp.* from [timebenchmarke] a left join (select * from TSymbol where d='%s' and Symbol='%s') temp on a.T=temp.T where a.type='CU' order by a.t;" % (time,symbol)

	res=ms.dict_sql(sql)
	lastrecord=res[0]
	for item in res[1:]:
		if item['T'] is None and lastrecord['T'] is not None:
			StockDate=str(lastrecord['D'])+" "+item['at']
			sql="insert into Tsymbol ([Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc])values('%s',%s,%s,%s,%s,0,%s,'%s','%s','%s',%s)" % (lastrecord['Symbol'],lastrecord['O'],lastrecord['C'],lastrecord['H'],lastrecord['L'],lastrecord['OPI'],lastrecord['D'],item['at'],StockDate,lastrecord['C'])
			print sql
			ms.insert_sql(sql)
		else:
			lastrecord=item




def fix_data_IF(Date):
	sql=" select SUM(1)as sum,Symbol,D from TSymbol where symbol in ('if','ic','ih','T','TF','TFZL')AND D<='%s' group by Symbol,D having SUM(1)<270 and sum(1)>220  ORDER BY d" % (Date)
	res=ms.dict_sql(sql)
	for item in res:
		symbol=item['Symbol']
		time=item['D']
		print symbol,time
		add_for_item_IF_before(symbol,time)
		add_for_item_IF(symbol,time)


def fix_data_CU(Date):
	#sql=" select SUM(1)as sum,Symbol,D from TSymbol   where symbol in ('AG','AU','BBZL','BU','C','CF','CS','CU','FBZL','FG','HC','I','IZL','J','JMZL','JZL','L','LZL','M','MA','MEZL','NI','p','PP','RB','RBZL','RMZL','RU','SR','TA','YY','ZC','ZN')  AND D<='2016/03/23' group by Symbol,D having SUM(1) not in (225,1,2,18,3,4,5,6,7)  and SUM(1)>100 and SUM(1)<225 ORDER BY d"
	sql=" select SUM(1)as sum,Symbol,D from TSymbol   where symbol in ('AG','AU','BBZL','BU','C','CF','CS','CU','FBZL','FG','HC','I','IZL','J','JMZL','JZL','L','LZL','M','MA','MEZL','NI','p','PP','RB','RBZL','RMZL','RU','SR','TA','YY','ZC','ZN')  AND D<='%s' and D>='2015/01/23' group by Symbol,D having SUM(1) not in (225,1) and  SUM(1)<225 ORDER BY d " % (Date)
	res=ms.dict_sql(sql)
	for item in res:
		symbol=item['Symbol']
		time=item['D']
		print symbol,time
		add_for_item_CU_before(symbol,time)
		add_for_item_CU(symbol,time)






Date='2016/05/13'
# fix_data_IF(Date)
# fix_data_CU(Date)
# symbol='J'
# time='2015/02/06'
# print symbol,time
# add_for_item_CU(symbol,time)
# add_for_item_CU_before('p','2016/05/13')
# add_for_item_CU('p','2016/05/13')