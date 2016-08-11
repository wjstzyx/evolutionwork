#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime

from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import sqlite3
#conn = sqlite3.connect('test.db')


def ac_position(tablename,sourcefile="",newfile=""):
	sourcefile=r"C:\YYfiles\NewEL\allEl170_0810\1470585600.sgRet.txt"
	newfile=r"C:\YYfiles\NewEL\targetfile\1470585600.sgRet.txt"
	#创建临时存储表
	conn = sqlite3.connect(':memory:')
	print "Opened database successfully"
	sql="create table if not exists mytable(name char(100),mytime datetime,position real)"
	conn.execute(sql)
	sql="delete from mytable"
	conn.execute(sql)
	sql="drop index if exists idx_name_mytime"
	conn.execute(sql)
	sql="create unique index idx_name_mytime on mytable(name,mytime)"
	conn.execute(sql)
	# 第一步去重复,将流水线中的重复行去掉
	file=open(sourcefile,'r')
	filecontent=file.readlines()
	file.close()
	newlist=list(set(filecontent[1:]))
	file=open(newfile,'w')
	# print filecontent[1:4]
	file.write(filecontent[0])
	for item in newlist:
		file.write(item)
	file.close()
	#将行信息表示成list
	sortednewlist=[]
	for item in newlist:
		itemlist=item.split('\n')[0].split('\t')
		name=itemlist[0]
		mytime=datetime.datetime.strptime(itemlist[1],"%Y-%m-%d %H:%M:%S")
		position=itemlist[2]
		if mytime.hour<=14 and mytime.hour>=9:
			templist=[name,mytime,position]
			sortednewlist.append(templist)
	#获取虚拟组名字
	namelist=[item[0] for item in sortednewlist]
	namelist=list(set(namelist))
	# 初始化bigdata--
	bigdata={}
	for item in namelist:
		bigdata[item]={}
	#将记录按时间从小到大排序
	sortednewlist=sorted(sortednewlist, key=lambda student: student[1]) 
	#按照分钟级别去重复（即将秒去掉）
	for item in sortednewlist:
		temptime=item[1].strftime("%Y-%m-%d %H:%M")
		temptime=datetime.datetime.strptime(temptime,"%Y-%m-%d %H:%M")
		bigdata[item[0]][temptime]=item[2]
	#将记录存入临时表
	for name in namelist:
		#对于一个虚拟组，按照时间序列排序
		nameconten=sorted(bigdata[name].iteritems(),key=lambda d:d[0],reverse = False)
		lastposition=9999
		for item in nameconten:
			# print name,item 
			if item[1]!=lastposition:
				lastposition=item[1]
				sql="insert into mytable values('%s','%s',%s)" % (name,item[0],item[1])
				conn.execute(sql)
				conn.commit()
	#查看记录总数
	# sql="select count(*) from mytable"
	# cursor=conn.execute(sql)
	# for item in cursor:
	# 	print item 
	# exit()
	#将记录存入固定数据库
	sql="select distinct name from mytable"
	cursor =conn.execute(sql)
	for name in cursor:
		sql="select * from mytable where name='%s' order by mytime" % (name[0])
		cursor1=conn.execute(sql)
		totalnum=0
		tempvalue=""
		#sql="select max(stockdate) as stockdate from [LogRecord].[dbo].[A_ac_position] where name='%s'" % (name[0])
		sql="select max(stockdate) as stockdate from [LogRecord].[dbo].[%s] where name='%s'" % (tablename,name[0])
		res=ms.dict_sql(sql)
		if res[0]['stockdate'] is not None:
			stockdate=res[0]['stockdate'].strftime("%Y-%m-%d %H:%M:00")
		else:
			stockdate="2005-10-01 13:00"
		for item in cursor1:
			if item[1]>stockdate:
				# print item,stockdate
				value=",('%s','%s',%s)" % (item[0],item[1],item[2])
				tempvalue=tempvalue+value
				totalnum=totalnum+1
			if totalnum>700:
				tempvalue=tempvalue.strip(',')
				sql="insert into [LogRecord].[dbo].[%s] values%s" % (tablename,tempvalue)
				ms.insert_sql(sql)
				tempvalue=""
				totalnum=0
		if tempvalue!="":
			tempvalue=tempvalue.strip(',')
			sql="insert into [LogRecord].[dbo].[%s] values%s" % (tablename,tempvalue)
			ms.insert_sql(sql)


		
ac_position("A_ac_position")