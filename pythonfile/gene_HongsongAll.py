#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")


def general_HongsongAll():
	sql="select max(date) as date from [LogRecord].[dbo].[AccountsBalance] where userid in ('HongsongStock','666061008') group by userid"
	res=ms.dict_sql(sql)
	monthday=int(datetime.datetime.now().strftime('%Y%m%d'))
	sql="select max(date) as date from [LogRecord].[dbo].[AccountsBalance] where userid ='HongsongAll'"
	maxHongsongAll=ms.dict_sql(sql)[0]['date']

	if res[0]['date']==res[1]['date'] and res[1]['date']>maxHongsongAll:
		sql="insert into [LogRecord].[dbo].[AccountsBalance] select date,'HongsongAll' as userid, 0 as prebalance, SUM(deposit) as deposit,SUM(Withdraw)as Withdraw,0 as CloseProfit,0 as PositionProfit,SUM(Commission) as Commission,SUM(CloseBalance) as CloseBalance  from [LogRecord].[dbo].[AccountsBalance] where userid in ('HongsongStock','666061008') and date>%s group by date " % (maxHongsongAll)
		ms.insert_sql(sql)

general_HongsongAll()





