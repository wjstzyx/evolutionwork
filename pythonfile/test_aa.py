#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
import time
import sys, urllib, urllib2, json
import shutil
import os 
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
def gene_jieti():
	acnamedirtoor=['ruStepMulti','pStepMulti','lStepMulti','RBStepMulti','taStepMulti','mStepMulti','JStepMulti','jmStepMulti','maStepMulti','IStepMulti','srStepMulti','aStepMulti','ppStepMulti','cfStepMulti','fgStepMulti','oiStepMulti','alStepMulti','cuStepMulti','cStepMulti','zcStepMulti','buStepMulti','csStepMulti','niStepMulti','hcStepMulti','jdStepMulti','rmStepMulti','auStepMulti','YYStepMulti','znStepMulti','agStepMulti']
	s_id=[1,10,20,21,22,23,24,25,26,27,3,30,31,33,34,35,39,5,51,52,53,54,55,56,57,59,6,7,8,9]
	num1=len(acnamedirtoor)
	tempdict={}
	for  i in range(num1):
		tempdict[acnamedirtoor[i]]=s_id[i]
	#cerfity
	# for item in tempdict.keys():
	# 	symbol=item.split('StepMulti')[0]
	# 	sql="select s_id from [Future].[dbo].[Symbol_ID] where symbol='%s'" % (symbol)
	# 	res=ms.dict_sql(sql)
	# 	if res[0]['s_id']==tempdict[item]:
	# 		print symbol,'OK'
	# 	else:
	# 		print "@@@@@@@@@@@@@@@",symbol

	newfileroot=r'G:\add_afl\TEMP'
	# newfileroot=r'E:\test'
	for item in tempdict.keys():
		s_id=str(tempdict[item])
		if len(s_id)<2:
			s_id='0'+s_id
		s_id='101'+s_id


		#make symbol dir
		targetdir=newfileroot+"\\"+item+'2'
		if not os.path.exists(targetdir):
			os.makedirs(targetdir)
		#copy source to G:\add_afl\aflfiles
		dir=r'G:\add_afl\temp_source_forjieti'
		files=os.listdir(dir)
		for item1 in files:
			#copyfile(src, dst)
			shutil.copyfile(dir+"\\"+item1,r'G:\add_afl\aflfiles'+"\\"+item1)
		#python cmd
		cmd='python G:\\\\add_afl\\\\auto_add_ID.py %s day one' % (s_id)
		print cmd 
		os.system(cmd)
		#copy G:\add_afl\aflfiles to targetdir
		files=os.listdir(r'G:\add_afl\aflfiles')
		for item1 in files:
			shutil.copyfile(r'G:\add_afl\aflfiles'+"\\"+item1,targetdir+"\\"+item1)
		print item 






		# files = os.listdir(dir)
		# for item in files:
		# 	shutil.copyfile(newfilenamepath,oldfilenamepath)





gene_jieti()

