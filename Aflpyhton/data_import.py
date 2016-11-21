#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

import os
from datetime import date
import time
from win32com.client import Dispatch
import shutil
import chardet
import re



ABautoroot=r'E:'
dirformat=r'D:\Program Files\AmiBroker\Formats\custom3.format'
database=r'D:\Program Files\AmiBroker\newlianxu'
ABprogramedir="D:\\Program Files\\AmiBroker"


def import_data(dirfrom,dirformat,database):
	ab = Dispatch("Broker.Application")	
	ab.LoadDatabase(database)
	ab.Import(0,dirfrom,dirformat)
	# ab.Documents.Open(Ticker)
	ab.SaveDataBase()
	print "数据成功导入"



def run_aflfile(ab,database,Ticker,aflfle,settingfile):
	ab.LoadDatabase(database)
	ab.Documents.Open(Ticker)
	# set apply to and range
	aa = ab.Analysis
	aa.ClearFilters()
	# MODIFY FOR YOUR SETUP: this runs against watchlist #1.  Note the VBScript/JScript
	# syntax shown in the docs doesn't work in Python.
	# aa.Filter(0, "watchlist", 0) #the last parameter is the watchlist #
	aa.ApplyTo = 1	 # use filters:2 watchlist #1
	isLoadFormul=aa.LoadFormula(aflfle)
	print "Successfully loaded AFL script:", aflfle
	isLoadSettings=aa.LoadSettings(settingfile)
	print "Successfully loaded setting file:",settingfile
	aa.RangeMode = 0
 	# aa.RangeMode = 3   
 	# aa.RangeFromDate ='2016/10/01'
 	# aa.RangeToDate = '2016/11/01'




	try:
		aa.Backtest(0)
		#time.sleep(5)
		#aa.Explore()
		#aa.Backtest(0)
		#resultFile = ResultFolder + "\\" + basename + "-ps.csv"
		#print "Explore file : " + resultFile
		#aa.Export(resultFile)
	except:
		print "=============================="
		print "Error: " + aflfle   
		print "=============================="
	ab.Documents.Close()






#将数据文件夹中的数据全部导入
def main_import_data():
	datafir=ABautoroot+"\\ABautofile\\datafile"
	datafiles = os.listdir(datafir)
	for file in datafiles:
		dirfrom=datafir+"\\"+file
		print dirfrom
		import_data(dirfrom,dirformat,database)



#获得afl 和配置文件的对应关系
def main_run_afl():
	#todo:解析symbl 直接赋值给Ticker
	aflfiledir=ABautoroot+"\\ABautofile\\aflfile"
	aflfiles=os.listdir(aflfiledir)
	ab = Dispatch("Broker.Application")

	totalconfig=[]
	for file in aflfiles:
		fileparts = file.split(".")
		if len(fileparts) >= 2 and fileparts[-1].lower() == "afl":
			basename = fileparts[0]
			timeperiod=basename.split('-')[1].strip(" ")
			if timeperiod in ('1min','2min','3min','4min','5min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a1_5"
			if timeperiod in ('6min','7min','8min','9min','10min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a6_10"
			if timeperiod in ('11min','12min','13min','14min','15min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a11_15"
			if timeperiod in ('16min','17min','18min','19min','20min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a16_20"
			if timeperiod in ('21min','22min','23min','24min','25min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a21_25"
			if timeperiod in ('26min','27min','28min','29min','30min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a26_30"
			itemfile=aflfiledir+"\\"+file
			settingfile=itemsettingdir+"\\"+timeperiod+".ABS"
			Ticker=basename.split('-')[0].strip(" ")
			totalconfig.append([itemsettingdir,itemfile,settingfile,Ticker])



	totalconfig=sorted(totalconfig, key=lambda student: student[0])
	tempdir=""
	for item in totalconfig:
		if item[0]!=tempdir:
			print item 
			print tempdir
			oldfilenamepath=ABprogramedir+"\\"+"broker.prefs"
			newfilenamepath=item[0]+"\\"+"broker.prefs"
			if os.path.isfile(oldfilenamepath): 
				if os.path.isfile(ABprogramedir+"\\"+"broker_backups.prefs"):
					os.remove(ABprogramedir+"\\"+"broker_backups.prefs")
				os.rename(oldfilenamepath,ABprogramedir+"\\"+"broker_backups.prefs")
				#os.remove(oldfilenamepath)
			shutil.copyfile(newfilenamepath,oldfilenamepath)

			cmd='taskkill /F /IM Broker.exe'
			os.system(cmd)
			ab = Dispatch("Broker.Application")
			tempdir=item[0]
		aflfle=item[1]
		settingfile=item[2]
		Ticker=item[3]
		run_aflfile(ab,database,Ticker,aflfle,settingfile)



#从数据库中将数据保存csv 并放入规定文件夹
def gere_datafile(starttime):
	sql="select distinct symbol from TSymbol"
	res1=ms.dict_sql(sql)
	for symbol in res1:
		sql="select CONVERT(varchar(20),StockDate,111) as data, CONVERT(varchar(20),StockDate,8) as time,O,H,L,C,V,OPI from TSymbol_quotes_backup where Symbol='%s' and stockdate>='%s'  order by StockDate" % (symbol['symbol'],starttime)
		rows=ms.dict_sql(sql)
		datafir=ABautoroot+"\\ABautofile\\datafile"
		import csv
		fieldnames = ['data', 'time', 'O', 'H', 'L', 'C', 'V', 'OPI']
		dict_writer = csv.DictWriter(file(datafir+'\\%s.csv' % (symbol['symbol']), 'wb'), fieldnames=fieldnames)
		# dict_writer.writerow(fieldnames)
		dict_writer.writerows(rows)
	print "gere_datafile finished"


#根据虚拟组名字选择规定的afl文件放入制定文件夹
def choose_aflfile(acname):
	dirroot=r'E:\ABautofile\sortalffile'
	targetroot=r'E:\ABautofile\aflfile'
	#监测虚拟组元素是否全
	sql="  select p.ST from P_BASIC p  left join [LogRecord].[dbo].[aflfile_st_symbol_time] b  on p.ST=b.st   where p.AC='%s'  and b.symbol is null" % (acname)
	res=ms.dict_sql(sql)
	if res:
		print "%s 虚拟组元素缺少,添加后重新进行" % (acname),res
		exit()
	else:
		sql="  select p.ST,b.symbol,b.time from P_BASIC p  left join [LogRecord].[dbo].[aflfile_st_symbol_time] b  on p.ST=b.st   where p.AC='%s'" % (acname)
		res1=ms.dict_sql(sql)
		for item in res1:
			filename=dirroot+"\\"+item['symbol']+"\\"+item['time']+"\\"+item['ST']+".afl"
			targetfilename=targetroot+"\\"+item['symbol']+"-"+item['time']+"-"+item['ST']+".afl"
			shutil.copyfile(filename,targetfilename)


# choose_aflfile('dd')



#根据账号选择afl文件
def choose_aflfile_byaccount(account):
	sql="select distinct f_ac from p_follow where ac='%s'" % (account)
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['f_ac']
		choose_aflfile(acname)

# choose_aflfile_byaccount('StepMultiI300w')

# filepath=r'E:\ABautofile\totalAflfile'
#afl文件重命名，加入symbol
def rename_afl(filepath):
	aflfiles=os.listdir(filepath)
	for file in aflfiles:
		print file
		oldfilename=filepath+"\\"+file
		temp=file.split('min-')[0]
		if file.split('min-')>=2:
			newfile=temp+"min-RB-"+''.join(file.split('-')[1:])
			newfilename=filepath+"\\"+newfile
			print oldfilename
			print newfilename
			os.rename(oldfilename,newfilename)
# rename_afl(filepath)



#检测st_repoet_test中的策略是不是虚拟组有且唯一的策略号
def test_is_all_ac_st():
	sql="select SUM(1) as sum from P_BASIC where st in (select distinct st from st_report_test)"
	res1=ms.dict_sql(sql)
	sql="select SUM(1) as sum from P_BASIC where ac in (select distinct ac from P_BASIC where st in (select distinct st from st_report_test))"
	res2=ms.dict_sql(sql)
	print 'begin '
	if res1[0]['sum']==res2[0]['sum']:
		sql="delete from st_report where st in (select distinct st from st_report_test)"
		ms.insert_sql(sql)
		sql="insert into st_report([P],[PP],[ST],[D],[T],[stockdate],[type]) select [P],[PP],[ST],[D],[T],[stockdate] ,0 as type  from st_report_test"
		ms.insert_sql(sql)
		print "success 已经将st_report_test 信息导入 st_report"
		
	else:
		print "fail 不完成，请检查"
		sql="  select b.AC,b.ST from (  select  * from P_BASIC where st in (select distinct st from st_report_test)) a right join (  select  * from P_BASIC where ac in (select distinct ac from P_BASIC where st in (select distinct st from st_report_test))) b  on a.AC=b.AC and a.ST=b.ST  where a.AC is null"
		res=ms.dict_sql(sql)
		print "as follows:"
		for item in res:
			print item['AC'],item['ST']


# test_is_all_ac_st()

#将正确命名的alf文件正确分布在文件夹

def sort_afl_file(tempfilepath='',targetroot=''):
	tempfilepath=r'E:\ABautofile\tempfile'
	targetroot=r'E:\ABautofile\sortalffile'
	aflfiles=os.listdir(tempfilepath)
	for item in aflfiles:
		# i=i+1
		# print i 
		# detectedEncodingDict = chardet.detect(item)
		# print detectedEncodingDict
		filemame= item.decode('gb2312').encode('utf-8')
		put_in_target_position(filemame,targetroot,tempfilepath,item)


def put_in_target_position(filemame,targetroot,tempfilepath,item):
	symbol=filemame.split('-')[0].strip(" ").lower()
	timeinterval=filemame.split('-')[1].strip(" ").lower()
	symboldir=targetroot+"\\"+symbol
	symbol_time_dir=symboldir+"\\"+timeinterval
	# print symbol,timeinterval
	# print symboldir,symbol_time_dir
	if not os.path.isdir(symboldir):
		os.mkdir(symboldir)
	if not os.path.isdir(symbol_time_dir):
		os.mkdir(symbol_time_dir)
	#获取st号码
	st='nost'
	with open(tempfilepath+"\\"+item,'r') as f:
		for line in f.readlines():
			#if detectedEncodingDict['encoding']  not in ('GB2312','ascii'):
			#	print 'detectedEncodingDict=',detectedEncodingDict['encoding']
			#line=line.decode(detectedEncodingDict['encoding']).encode('utf-8')
			matchObj = re.match( r'.*StrategyID = \"(.*)\";', line, re.M|re.I)
			if matchObj:
				# print "matchObj.group(1) : ", matchObj.group(1)
				st=matchObj.group(1).strip(" ")
	if st == 'nost':
		print filemame,"未查询到st号，请确认"
		exit()
	else:
		newfilename=symbol_time_dir+"\\"+st+".afl"
		shutil.copyfile(tempfilepath+"\\"+item,newfilename)
		#对应关系存数据库
		sql="select 1 as a from [LogRecord].[dbo].[aflfile_st_symbol_time] where st='%s'" % (st)
		res=ms.dict_sql(sql)
		if res:
			sql="update [LogRecord].[dbo].[aflfile_st_symbol_time] set symbol='%s',time='%s',inserttime=getdate() where st='%s'" % (symbol,timeinterval,st)
			ms.insert_sql(sql)
			print "重复的ID ",st,filemame
		else:
			sql="insert into [LogRecord].[dbo].[aflfile_st_symbol_time](st,symbol,time) values('%s','%s','%s')" % (st,symbol,timeinterval)
			ms.insert_sql(sql)



# sort_afl_file()


#对制定文件夹afl加前缀
def add_prename(symbol='',tieminteval=''):
	targetdir=r'E:\ABautofile\z_change_prename'
	aflfiles=os.listdir(targetdir)
	for item in aflfiles:
		filemame= item.decode('gb2312').encode('utf-8')
		print filemame
		if os.path.isdir(targetdir+'\\'+item):
			matchObj = re.match( r'(.*)StepMultiI', item, re.M|re.I)
			if matchObj:
				symbol=matchObj.group(1).strip(" ")
			else:
				print "no symbol",targetdir+'\\'+filemame
				exit()

			secondaflfiles=os.listdir(targetdir+'\\'+item)
			for item1 in secondaflfiles:
				newfilename=symbol+"-"+item1
				oldfile=targetdir+"\\"+item+"\\"+item1
				newfile=targetdir+"\\"+item+"\\"+newfilename
				copufilename=r'E:\ABautofile\tempfile'+"\\"+newfilename
				shutil.move(oldfile,newfile)
				shutil.copyfile(newfile,copufilename)
		print filemame,'文件夹'

# add_prename()



##########
##运行步骤(有些步骤是可以每天定时做的 #1  #2 )
##########
# gere_datafile(starttime='2015-02-01')
# main_import_data()

#3  choose_aflfile(acname)
# main_run_afl()
#5  

#检测st_repoet_test中的策略是不是虚拟组有且唯一的策略号
test_is_all_ac_st()
