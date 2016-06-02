#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import os
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

nowtimehour=datetime.datetime.now().strftime("%H")
print nowtimehour



cmd="ps -ef|grep 'read_maillist.py'|grep -v 'grep'|awk '{print $2}'"
output=os.popen(cmd)
res=output.read()
print res,type(res)
if res and (nowtimehour==11 or nowtimehour==20):
	processid=res
	print processid
	cmd="kill %s" % (processid)
	os.system(cmd)
	cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/read_maillist.py &'
	os.system(cmd)
if res=='':
	cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/read_maillist.py &'
	os.system(cmd)
	

cmd="ps -ef|grep 'monitor_wenhua.py'|grep -v 'grep'|awk '{print $2}'"
output=os.popen(cmd)
res=output.read()
print res,type(res)
if res and (nowtimehour==11 or nowtimehour==20):
	processid=res
	print processid
	cmd="kill %s" % (processid)
	os.system(cmd)
	cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/monitor_wenhua.py &'
	os.system(cmd)
if res=='':
	cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/monitor_wenhua.py &'
	os.system(cmd)
	

