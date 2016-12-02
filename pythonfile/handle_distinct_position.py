#coding=utf-8 
#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
from dbconn import MSSQL
ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
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

def handle_distinct_account_position(ms):
	nowtime=int(datetime.datetime.now().strftime('%H%M'))
	if nowtime>=1800 and nowtime<=1802:
		sql="SELECT distinct userID,stockID  FROM [LogRecord].[dbo].[account_position]"
		res=ms.dict_sql(sql)
		for item in res:
			userID=item['userID']
			stockID=item['stockID']
			#确认开始时间
			sql="select top (1) * from [LogRecord].[dbo].[account_position_distinct] where userid='%s' and stockID=%s order by inserttime desc" % (userID,stockID)
			tempres=ms.dict_sql(sql)
			if tempres:
				fromtime=tempres[0]['inserttime']
				longhave=tempres[0]['longhave']
				longsend=tempres[0]['longsend']
				shorthave=tempres[0]['shorthave']
				shortsend=tempres[0]['shortsend']
				lastlist=[longhave,longsend,shorthave,shortsend]
			else:
				fromtime='2015-01-01'
				lastlonghave=-999
				lastlongsend=-999
				lastshorthave=-999
				lastshortsend=-999
				lastlist=[-999,-999,-999,-999]

			sql="select * from [LogRecord].[dbo].[account_position] where userid='%s' and stockID=%s and inserttime>'%s'  order by inserttime" % (userID,stockID,fromtime)
			res1=ms.dict_sql(sql)
			#将有变化的存入
			i=0
			for item1 in res1:
				longhave=item1['longhave']
				longsend=item1['longsend']
				shorthave=item1['shorthave']
				shortsend=item1['shortsend']
				newlist=[longhave,longsend,shorthave,shortsend]

				if lastlist != newlist:
					# print 'lastlist',lastlist
					# print 'newlist',newlist
					sql="insert into [LogRecord].[dbo].[account_position_distinct](userID,time,stockID,longhave,longsend,shorthave,shortsend,date,inserttime) values('%s',%s,%s,%s,%s,%s,%s,%s,'%s')" % (userID,item1['time'],stockID,longhave,longsend,shorthave,shortsend,item1['date'],item1['inserttime'].strftime("%Y-%m-%d %H:%M:%S"))
					ms.insert_sql(sql)
					lastlist=newlist


		#删除20天前的历史记录
		sql='delete  FROM [future].[dbo].[map_backup]  where DATEDIFF(day,datetime,getdate())>15'
		ms.insert_sql(sql)



try:
	handle_distinct_record(ms105)
	handle_distinct_record_forquanyi(ms105)
except:
	pass
try:
	#实盘期货期货仓位入库 去重
	handle_distinct_account_position(ms05)
except:
	pass 





