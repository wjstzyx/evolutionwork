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

nowtimehour=datetime.datetime.now().strftime("%H:%M")
print nowtimehour



def gene_bar(ms,period):
	try:
		cmd="ps -ef|grep 'generate_merge_bars_index_2.py %s %s' |grep -v 'grep' |awk '{print $2}'" % (ms,period)
		output=os.popen(cmd)
		res=output.read()
		print res,type(res)
		if res and (nowtimehour=='11:46' or nowtimehour=='19:46'):
			processid=res
			print processid
			cmd="kill %s" % (processid)
			os.system(cmd)
			cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/generate_merge_bars_index_2.py %s %s &' % (ms,period)
			os.system(cmd)
		if res=='':
			cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/generate_merge_bars_index_2.py %s %s &' % (ms,period)
			os.system(cmd)
	except:
		pass



try:
	cmd="ps -ef|grep 'read_maillist.py'|grep -v 'grep'|awk '{print $2}'"
	output=os.popen(cmd)
	res=output.read()
	if res and (nowtimehour=='11:46' or nowtimehour=='19:46'):
		processid=res
		print processid
		cmd="kill %s" % (processid)
		print cmd
		os.system(cmd)
		cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/read_maillist.py &'
		os.system(cmd)
	if res=='':
		cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/read_maillist.py &'
		os.system(cmd)
except:
	pass
	
try:
	cmd="ps -ef|grep 'monitor_wenhua.py'|grep -v 'grep'|awk '{print $2}'"
	output=os.popen(cmd)
	res=output.read()
	if res and (nowtimehour=='11:46' or nowtimehour=='19:46'):
		processid=res
		print processid
		cmd="kill %s" % (processid)
		os.system(cmd)
		cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/monitor_wenhua.py &'
		os.system(cmd)
	if res=='':
		cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/monitor_wenhua.py &'
		os.system(cmd)
except:
	pass	


gene_bar('ms05',5)
gene_bar('ms03',5)
gene_bar('ms05',15)
gene_bar('ms03',15)
gene_bar('ms05',30)








# nohup python /home/yuyang/myfile/evolutionwork/website1/elmanager/manage.py runserver 0.0.0.0:9001 &

try:
	cmd="ps -ef|grep 'manage.py runserver 0.0.0.0:9001' |grep -v 'grep' |awk '{print $2}'"
	output=os.popen(cmd)
	res=output.read()
	res=res.replace('\n',' ')
	print res,type(res)
	if res and (nowtimehour=='11:46' or nowtimehour=='19:46'):
		processid=res
		print processid
		cmd="kill %s" % (processid)
		os.system(cmd)
		cmd='python /home/yuyang/myfile/evolutionwork/website1/elmanager/manage.py runserver 0.0.0.0:9001 &'
		print 1,cmd
		os.system(cmd)
	if res=='':
		cmd='python /home/yuyang/myfile/evolutionwork/website1/elmanager/manage.py runserver 0.0.0.0:9001 &'
		print 2,cmd
		os.system(cmd)
except:
	pass