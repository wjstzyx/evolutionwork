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
def testcanhavest(ac,symbol):
	# 清除临时表
	try:
		sql="drop table #temp_quanyi_new"
		ms.insert_sql(sql)
		sql="drop table #temp_p_log"
		ms.insert_sql(sql)
	except:
		pass
	# 产生临时p_log
	#sql="select * into #temp_p_log from (SELECT   aa.*, sid.Symbol, (YEAR(GETDATE()) - 2000) * 10000 + MONTH(GETDATE()) * 100 + DAY(GETDATE()) AS D from (select  p.AC, p.STOCK, p.type, p.ST, p.P_size, a.ratio from P_BASIC p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.type=a.type and p.AC='%s') as aa inner join Symbol_ID AS sid ON sid.S_ID = aa.STOCK where Symbol='%s') temp" % (ac,symbol)
	sql ="select * into #temp_p_log from (select '%s' as ac,temp1.STOCK,temp1.type,temp1.ST,temp1.P_size as P_size,temp1.ratio,temp1.Symbol,temp1.num from (select p.*,a.ratio,sid.Symbol,isnull(n.num,1)as num from P_BASIC p inner join AC_RATIO a on p.AC=a.AC and p.AC='%s' inner join Symbol_ID  AS sid ON p.STOCK=sid.S_ID left join [LogRecord].[dbo].[Ninone_config] n on n.st=p.st) temp1 where Symbol='%s' )aaa"% (ac,ac,symbol)
	#print sql 
	ms.insert_sql(sql)
	sql="select SUM(p_size*ratio/100*num) as totalsum from #temp_p_log"
	res=ms.dict_sql(sql)
	totalsum=res[0]['totalsum']

	#产生临时整个虚拟组st_report
	sql="select * into  #temp_quanyi_new from ( select p.ac,p.symbol,st_report.type,st_report.id,st_report.p,st_report.pp,p.p_size,p.ratio ,st_report.st,st_report.stockdate from st_report  inner join #temp_p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s')temp " % (ac,symbol)
	#print sql 
	ms.insert_sql(sql)
	#print 1,datetime.datetime.now()
	sql="select count(*)  as num from #temp_quanyi_new"
	res=ms.dict_sql(sql)
	if res[0]['num']<10:
		print ac,"  ",res[0]['num'] 



sql="SELECT id, [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isforbacktest]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where iscaculate=1 order by id desc "
res=ms.dict_sql(sql)
for item in res:
	positionsymbol=item['positionsymbol']
	quanyisymbol=item['quanyisymbol']
	testcanhavest(item['acname'],positionsymbol)
