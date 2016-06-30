#coding=utf-8 
#!/usr/bin/env python
import sys
import time
import datetime
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
a='160828'
stockdate='2016-06-28 00:00:00'
stockdate=datetime.datetime.strptime(stockdate,'%Y-%m-%d %H:%M:%S')
def range_quanyi_byyepan(stockdate):
	D=stockdate.strftime('%Y%m%d')
	thisday=str(int(D)-20000000)
	D=datetime.datetime.strptime(D,'%Y%m%d')
	beforeday=D-datetime.timedelta(hours=10)
	beforeday=beforeday.strftime('%Y%m%d')
	beforeday=str(int(beforeday)-20000000)
	Dcenter=D+datetime.timedelta(hours=24)
	timedelta1 = Dcenter - stockdate
	timedelta1=abs(timedelta1.total_seconds())
	if timedelta1<3600*5:
		return thisday
	else:
		return beforeday
print range_quanyi_byyepan(stockdate)