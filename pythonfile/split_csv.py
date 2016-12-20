#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import os
import shutil
import csv
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

root=r'C:\Users\YuYang\Desktop\daynight'
if not os.path.exists(root+'\\fisrsttime'):
	os.makedirs(root+'\\'+'fisrsttime')
if not os.path.exists(root+'\\secondtime'):
	os.makedirs(root+'\\'+'secondtime')
if not os.path.exists(root+'\\thirdtime'):
	os.makedirs(root+'\\'+'thirdtime')


def split_data(fromdate,enddate,target):
	symbols=os.listdir(root)
	for symbol in symbols:
		print symbol
		if '.csv' in symbol:
			temproot=root+'\\'+target

			path=root+'\\'+symbol

			targetfile1=root+'\\'+target+'\\'+symbol.split('.csv')[0]+"-"+str(fromdate)+'-'+str(enddate)+'.csv'

			with open(path,"rb" ) as f:
				reader=csv.reader(f)
				with open(targetfile1,'wb') as t:
					for row in reader:
						if int(row[0])>=fromdate and int(row[0])<=enddate:
							spamwriter = csv.writer(t)
							spamwriter.writerow(row)
				t.close()
			f.close


split_data(20000101,20131201,'fisrsttime')
split_data(20131201,20151201,'secondtime')
split_data(20151201,20161231,'thirdtime')