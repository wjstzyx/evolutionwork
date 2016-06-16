#coding=utf-8 
#!/usr/bin/env python
import sys
import os
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def read_txt():
	machinename='9.txt'
	filepath="C:\Users\YuYang\Desktop\\%s" % (machinename)
	f=open(filepath,"r")
	content=f.readlines()
	i=0
	for item in content:
		i=i+1
		item.replace('"','')
		temp=item.split(';')[0]
		temp=temp.split('\\')[-1]
		# print temp
		path=temp.split(':')[0]
		st_id=temp.split('=')[-1]
		if "Param" in st_id:
			st_id=st_id.split(',')[1]
		print path,st_id
		sql="select * from [LogRecord].[dbo].[distinctst] where st=%s" % (st_id)
		res=ms.dict_sql(sql)
		if res:
			if path==res[0]['filename'] and machinename==res[0]['machinename']:
				sql="update [LogRecord].[dbo].[distinctst] set number=number+1 where st=%s" % (st_id)
			else:
				sql="""insert into [LogRecord].[dbo].[distinctst](filename,st,number,machinename) values('%s',%s,%s,'%s')""" % (path.replace("'","''"),st_id,1,machinename)
		else:
			sql="""insert into [LogRecord].[dbo].[distinctst](filename,st,number,machinename) values('%s',%s,%s,'%s')""" % (path.replace("'","''"),st_id,1,machinename)
		ms.insert_sql(sql)
	print i

	f.close()



def is_time_right():
	ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")
	sql="select getdate()"
	res=ms1.find_sql(sql)
	print res[0][0]
	res=ms.find_sql(sql)
	print res[0][0]
	print datetime.datetime.now()


is_time_right()