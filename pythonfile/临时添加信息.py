#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import os
import shutil
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-
dir = r'E:\ABautofile\aflfile'
def get_filename_list():
	filelists=[]
	files = os.listdir(dir)  
	for f in files:  
	    #print  f.decode('gbk') 
	    filelists.append(f.decode('gbk'))
	return filelists
filelists=get_filename_list()

def main():
	for item in filelists:
		filepath=dir+'\\'+item
		filepathnew=dir+'\\'+item.split('.')[0]+'_new.afl'
		with open(filepath,'r') as f:
			with open(filepathnew,'w') as g:
				for line in f.readlines():
					linelist=line.split("\r")
					for item in linelist:
						g.write(item)
				g.write('Buy = 0;\r')
				g.write('Short = 0;\r')
				g.write('Sell = Cover = 0;\r')
		shutil.move(filepathnew, filepath)
main()