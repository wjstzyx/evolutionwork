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
stockdate='2016-06-28 00:00:01'
stockdate=datetime.datetime.strptime(stockdate,'%Y-%m-%d %H:%M:%S')

aa=time.mktime(stockdate.timetuple())
print aa


def test():

	bb=0
	i=0
	sum=0
	sql="SELECT id,[AC]  ,[inserttime]  FROM [LogRecord].[dbo].[errorstlist] order by id "
	res=ms.dict_sql(sql)
	for item in res:
		stockdate=item['inserttime']
		aa=time.mktime(stockdate.timetuple())
		print aa-bb
		bb=aa


test()

#1467043200.0