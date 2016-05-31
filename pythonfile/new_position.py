#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList


def writr_position_byday(D):
	sql="select * from st_report a inner join P_Log p on a.ST=p.st and p.AC='RBQGSTREV_TG' and p.symbol='RB' and p.D=160526"
	



def write_position():
	sql="select distinct D from p_log order by D"
	res=ms.find_sql(sql)
	for item in res:
		D=item[0]
		writr_position_byday(D)


D=160526
writr_position_byday(D)