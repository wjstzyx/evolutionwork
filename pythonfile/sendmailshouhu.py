#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import os
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

cmd="ps -ef|grep 'read_maillist.py'|grep -v 'grep'"
output=os.popen(cmd)
res=output.read()
print res,type(res)
if res=='':
	cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/read_maillist.py &'
	os.system(cmd)
	


