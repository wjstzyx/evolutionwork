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
# print resList
sql="select max(stockdate) as stockdate FROM [Future].[dbo].[quanyi_log_groupby] where ac='RU2v7' and symbol='RU1'"
res=ms.dict_sql(sql)[0]
print res
if res['stockdate'] == None:
	print 111
else:
	print 22
