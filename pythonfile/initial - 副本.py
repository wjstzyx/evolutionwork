#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import os 
import re
import shutil
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-


sourcedir=r'C:\Users\YuYang\Desktop\TEMP'
targetdir=r'C:\Users\YuYang\Desktop\TEMPtar'
aflfiles=os.listdir(sourcedir)
for item in aflfiles:
	filemame= item.decode('gb2312').encode('utf-8')
	print filemame
	if os.path.isdir(sourcedir+'\\'+item):
		matchObj = re.match( r'(.*)StepMulti2', item, re.M|re.I)
		if matchObj:
			symbol=matchObj.group(1).strip(" ")
		else:
			print "no symbol",targetdir+'\\'+filemame
			exit()

		secondaflfiles=os.listdir(sourcedir+'\\'+item)
		for item1 in secondaflfiles:
			newfilename=symbol+"-"+item1
			oldfile=sourcedir+"\\"+item+"\\"+item1
			newfile=targetdir+"\\"+newfilename
			shutil.copyfile(oldfile,newfile)
	print filemame,'文件夹'
