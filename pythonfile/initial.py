#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
def ismonitorday():
	sql="select top 1 D from TSymbol where T>'08:00' ORDER BY id desc"
	lastday=ms.find_sql(sql)[0][0]
	lastday='20'+lastday[2:4]+lastday[5:7]+lastday[8:10]
	sql="select getdate()"
	nowD=ms.find_sql(sql)[0][0].strftime('%Y%m%d')
	sql="select datepart(weekday, getdate())"
	weekday=ms.find_sql(sql)[0][0]
	print nowD
	print lastday
	print weekday
	if nowD==lastday and weekday in (2,3,4,5,6):
		return 1
	else:
		return 0

print ismonitorday()