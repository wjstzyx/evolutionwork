#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

##此功能为通过acname获得ac相关的st号及所在的机器
acname="RBNtrend"
symbol='RB'
nowdate=datetime.datetime.now().strftime("%Y%m%d")
nowdate=int(nowdate)-20000000
def get_st_by_ac(acname,symbol):
	sql="  select p.AC,p.st,p.p_size,b.filename,b.machinename from P_Log p left join  [LogRecord].[dbo].[distinctst] b   on p.st=b.st and p.AC='%s' and p.symbol='%s' and p.D=%s   where p.AC='%s' and p.symbol='%s' and p.D=%s" % (acname,symbol,nowdate,acname,symbol,nowdate)	
  	res=ms.dict_sql(sql)
  	for item in res:
  		print item['AC'],'	',item['st'],'	',item['p_size'],'	',item['filename'],'	',item['machinename'],'	'


get_st_by_ac(acname,symbol)
