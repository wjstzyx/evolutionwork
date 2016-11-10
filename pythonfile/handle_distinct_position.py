#coding=utf-8 
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
from dbconn import MSSQL
#ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms105 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

def handle_distinct_record(ms):
	nowtime=int(datetime.datetime.now().strftime('%H%M'))
	if nowtime>=1800 and nowtime<=1802:
		#删除20天前的历史记录
		sql='delete  FROM [future].[dbo].[map_backup]  where DATEDIFF(day,datetime,getdate())>20'
		ms.insert_sql(sql)

	sql="select distinct name from [future].[dbo].[map_backup] order by name"
	res=ms.dict_sql(sql)
	for item in res:
		name=item['name']
		#确认开始时间
		sql="select top 1 datetime,vp from [future].[dbo].[real_map_backup] where name='%s' order by datetime desc" % (name)
		tempres=ms.dict_sql(sql)
		if tempres:
			fromtime=tempres[0]['datetime']
			lastvp=tempres[0]['vp']
		else:
			fromtime='2015-01-01'
			lastvp=-9999
		print fromtime,name

		sql="select * from [future].[dbo].[map_backup] where name='%s' and datetime>'%s'  order by datetime" % (name,fromtime)
		res1=ms.dict_sql(sql)
		#将有变化的存入
		for item1 in res1:
			vp=item1['vp']
			if vp!=lastvp:
				sql="insert into [future].[dbo].[real_map_backup](name,datetime,vp,rp) values('%s','%s',%s,%s) " % (name,item1['datetime'],vp,item1['rp'])
				ms.insert_sql(sql)
			lastvp=vp



def handle_distinct_record_forquanyi(ms):
	nowtime=int(datetime.datetime.now().strftime('%H%M'))
	sql="select distinct name from [future].[dbo].[real_map_backup] order by name"
	res=ms.dict_sql(sql)
	for item in res:
		name=item['name']
		#确认开始时间
		sql="select top 1 datetime,rp from [future].[dbo].[real_map_backup_forquanyi] where name='%s' order by datetime desc" % (name)
		tempres=ms.dict_sql(sql)
		if tempres:
			fromtime=tempres[0]['datetime']
			lastvp=tempres[0]['rp']
		else:
			fromtime='2015-01-01'
			lastvp=-9999
		print fromtime,name

		sql="select * from [future].[dbo].[real_map_backup] where name='%s' and datetime>'%s'  order by datetime" % (name,fromtime)
		res1=ms.dict_sql(sql)
		#将有变化的存入
		for item1 in res1:
			vp=item1['rp']
			if vp!=lastvp:
				sql="insert into [future].[dbo].[real_map_backup_forquanyi](name,datetime,vp,rp) values('%s','%s',%s,%s) " % (name,item1['datetime'],item1['vp'],item1['rp'])
				ms.insert_sql(sql)
			lastvp=vp



handle_distinct_record(ms105)
handle_distinct_record_forquanyi(ms105)







