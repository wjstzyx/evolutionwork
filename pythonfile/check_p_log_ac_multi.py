#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def check_p_log_ac_multi(acname):
	sql="select top 1 SUM(1) as sum, max(id)as id,AC,STOCK,type,st,p_size,ratio,symbol,D from p_log where ac='%s' group by AC,STOCK,type,st,p_size,ratio,symbol,D having SUM(1)>1" % (acname)
	res=ms.dict_sql(sql)
	if res:
		print "***********************************"
		print "Find multirecord:"
		print "AC: %s" % (acname)
		print sql




