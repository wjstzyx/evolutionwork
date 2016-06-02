#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def delete_multi_st_report():
	sql="select top 1 SUM(1) as sum,max(id),P,PP,ST,D,T,stockdate,type from st_report group by P,PP,ST,D,T,stockdate,type having  sum(1)>1 order by sum desc"
	res=ms.dict_sql(sql)
	if res:
		totolnum=res[0]['sum']
		for  item in range(totolnum-1):
			sql="delete from st_report where id in (select max(id) as id from st_report group by P,PP,ST,D,T,stockdate,type having  sum(1)>1) "
			ms.insert_sql(sql)


try:
	delete_multi_st_report()
except Exception,e:
	print e

