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
def import_data(dirfrom,dirformat,database):
	ab = Dispatch("Broker.Application")	
	ab.LoadDatabase(database)
	ab.Import(0,dirfrom,dirformat)
	# ab.Documents.Open(Ticker)
	ab.SaveDataBase()
	print "数据成功导入"



def run_aflfile(database,Ticker,aflfle,settingfile):
	ab = Dispatch("Broker.Application")
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
	aa.RangeMode = 0	# all data
	try:
		aa.Backtest(0)
		# time.sleep(5)
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





ABautoroot=r'E:'
dirformat=r'D:\Program Files\AmiBroker\Formats\custom3.format'
database=r'D:\Program Files\AmiBroker\newlianxu'
ABprogramedir="D:\\Program Files\\AmiBroker"


#将数据文件夹中的数据全部导入
def main_import_data():
	datafir=ABautoroot+"\\ABautofile\\datafile"
	datafiles = os.listdir(datafir)
	for file in datafiles:
		dirfrom=datafir+"\\"+file
		print dirfrom
		import_data(dirfrom,dirformat,database)



#获得afl 和配置文件的对应关系
def main_run_afl(Ticker):
	#todo:解析symbl 直接赋值给Ticker
	aflfiledir=ABautoroot+"\\ABautofile\\aflfile"
	aflfiles=os.listdir(aflfiledir)

	totalconfig=[]
	for file in aflfiles:
		fileparts = file.split(".")
		if len(fileparts) >= 2 and fileparts[1].lower() == "afl":
			basename = fileparts[0]
			timeperiod=basename.split('-')[0]
			if timeperiod in ('1min','2min','3min','4min','5min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a1_5"
			if timeperiod in ('6min','7min','8min','9min','10min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a6_10"
			if timeperiod in ('11min','12min','13min','14min','15min'):
				itemsettingdir=ABautoroot+"\\ABautofile\\setting\\a11_15"
			itemfile=aflfiledir+"\\"+file
			settingfile=itemsettingdir+"\\"+timeperiod+".ABS"
			totalconfig.append([itemsettingdir,itemfile,settingfile])



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
			tempdir=item[0]
		aflfle=item[1]
		settingfile=item[2]
		run_aflfile(database,Ticker,aflfle,settingfile)



#从数据库中将数据保存csv 并放入规定文件夹
def gere_datafile(daynight,endtime):
	pass

#根据虚拟组名字选择规定的afl文件放入制定文件夹
def choose_aflfile(acname):
	pass






##########
##运行步骤
##########
#1  gere_datafile(daynight,endtime)
#2  main_import_data()

#3  choose_aflfile(acname)
#4  main_run_afl('HC')



