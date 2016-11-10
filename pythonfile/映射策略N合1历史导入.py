#coding=utf-8 
#!/usr/bin/env python
import re
import sys
import os 
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
import chardet
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms105 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-
# 将正则表达式编译成Pattern对象



# IF_YG8HT10
# IFYD
# IFYD_WP
# IFYD_YS
# LUD
# LUD_2YD
# LUD_3YD
# LUD_3YD2
# LUD_5YD

#每次需要修改路径
dir=r"C:\Users\YuYang\Desktop\映射程序\LUD_5YD\输出文件"




tempdir=dir.split("\\")
name=tempdir[-2]+"_0"
print name
totalvalue=""
inum=0

dir = unicode(dir , "utf8")
def get_filename_list():
	filelists=[]
	files = os.listdir(dir)  
	for f in files:  
	    #print  f.decode('gbk')
	    filelists.append(f)
	return filelists



def read_one_file(filename,date='',name=''):
	#filename = unicode(filename , "utf8")
	with open(filename,'r') as f:
		for line in f.readlines():
			detectedEncodingDict = chardet.detect(line)
			#if detectedEncodingDict['encoding']  not in ('GB2312','ascii'):
			#	print 'detectedEncodingDict=',detectedEncodingDict['encoding']
			#line=line.decode(detectedEncodingDict['encoding']).encode('utf-8')
			try:
				line=line.decode(detectedEncodingDict['encoding']).encode('utf-8')
			except:
				print "@@@@@coding error"
				line=line.decode('windows-1252').encode('utf-8')
			get_one_line(line,date,name)
	# totalvalue=totalvalue.strip(",")
	# sql=sql="insert into [future].[dbo].[test_map_backup](name,datetime,vp,rp) values%s" % (totalvalue)
	# ms105.insert_sql(sql)
	# totalvalue=""
	# inum=0


	
		#ADD tailf info




def get_one_line(line,date='',name=''):
	isdone=0
	#matchObj = re.match( r'(.*):(.*):(.*)--当前虚拟仓位:(.*)--实际仓位:(.*)', line, re.M|re.I)
	matchObj = re.match( r'(.*):(.*):(.*)--当前虚拟总仓位:(.*)--实际仓位:(.*)', line, re.M|re.I)
	if matchObj:
		#print "matchObj.group() : ", matchObj.group()
		#print "matchObj.group(1) : ", matchObj.group(1)
		#print "matchObj.group(2) : ", matchObj.group(2)
		#print "matchObj.group(3) : ", matchObj.group(3)
		#print "matchObj.group(4) : ", matchObj.group(4)
		#print "matchObj.group(5) : ", matchObj.group(5)
		#写入库
		#date='20161102'
		mydatetime=str(date)+' '+str(matchObj.group(1))+":"+str(matchObj.group(2))+":"+str(matchObj.group(3)).split('.')[0]
		mydatetime=datetime.datetime.strptime(mydatetime,"%Y%m%d %H:%M:%S")
		# try:
		# 	mydatetime=datetime.datetime.strptime(mydatetime,"%Y%m%d %H:%M:%S")
		# 	isdone=1
		# except:
		# 	isdone=0
			#将line记录下来
			# print date
			# print line
		if isdone==1 or 1==1:
			vp=matchObj.group(4).split("--")[0]
			rp=matchObj.group(5)
			if ('还没有出现有效信号' not in rp):
				sql="insert into [future].[dbo].[test_map_backup](name,datetime,vp,rp) values('%s','%s','%s','%s')" % (name,mydatetime,vp,rp)
				try:
					ms105.insert_sql(sql)
				except:
					pass





def handle_file(filelist):
	for item in filelist:
		namelist=item.split("-")
		if  namelist[0]=='查询持仓' or 1==1:
			date=namelist[1].split(".")[0]
			filename=dir+"\\"+item
			print filename.encode("utf-8")
			read_one_file(filename,date,name)


def move_signal():
	sql="select MAX(datetime) as datetime from [future].[dbo].[test_map_backup]  where name='%s' " % (name)
	res=ms105.dict_sql(sql)
	if res[0]['datetime'] is not None:
		print res[0]
		sptime=res[0]['datetime'].strftime("%Y-%m-%d")
		print sptime
	else:
		sptime='2016-11-07'
		print sptime
		print "请手动删除"
		print "delete from [future].[dbo].[test_map_backup] where name='%s' and datetime>='%s'" % (name,sptime)
		print "delete from [future].[dbo].[map_backup] where name='%s' and datetime>='%s'" % (name,sptime)
		print "insert into [future].[dbo].[map_backup] SELECT [name] ,[datetime]  ,[vp]  ,[rp] FROM [future].[dbo].[test_map_backup] where name='%s'" % (name)
		exit()
	sql="delete from [future].[dbo].[test_map_backup] where name='%s' and datetime>='%s'" % (name,sptime)
	ms105.insert_sql(sql)
	sql="delete from [future].[dbo].[map_backup] where name='%s' and datetime<'%s'" % (name,sptime)
	ms105.insert_sql(sql)
	sql="insert into [future].[dbo].[map_backup] SELECT [name] ,[datetime]  ,[vp]  ,[rp] FROM [future].[dbo].[test_map_backup] where name='%s'" % (name)
	ms105.insert_sql(sql)
	sql="delete  FROM [Future].[dbo].[dailyquanyi_V2] where ac='%s'" % (name)
	ms.insert_sql(sql)
	sql="delete  FROM [future].[dbo].[real_map_backup] where name='%s'" % (name)
	ms105.insert_sql(sql)
	sql="delete  FROM [future].[dbo].[real_map_backup_forquanyi] where name='%s'" % (name)
	ms105.insert_sql(sql)
	sql="truncate table [future].[dbo].[test_map_backup]"
	ms105.insert_sql(sql)



def handle_distinct_record(ms,name):
	nowtime=int(datetime.datetime.now().strftime('%H%M'))
	sql="select distinct name from [future].[dbo].[map_backup] where name='%s' order by name" % (name)
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
	if nowtime>=1800 and nowtime<=1802 or 1==1:
		#删除20天前的历史记录
		sql='delete  FROM [future].[dbo].[map_backup]  where DATEDIFF(day,datetime,getdate())>20'
		ms.insert_sql(sql)


def handle_distinct_record_forquanyi(ms,name):
	nowtime=int(datetime.datetime.now().strftime('%H%M'))
	sql="select distinct name from [future].[dbo].[map_backup] where name='%s' order by name" % (name)
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





def cmd_new_cal():
	cmd="python C:\\YYfiles\\evolutionwork\\pythonfile\\new_cal_quayi_V2_for_yingshe.py %s" % (name)
	print cmd 
	os.system(cmd)





filelist=get_filename_list()
handle_file(filelist)
print 'move_signal'
move_signal()
print 'handle_distinct_record'
handle_distinct_record(ms105,name)
handle_distinct_record_forquanyi(ms105,name)
print cmd_new_cal()
cmd_new_cal()

