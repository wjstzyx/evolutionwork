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


sourcedir=r'C:\Users\YuYang\Desktop\gaosheng2'
symboldir=os.listdir(sourcedir)
for item in symboldir:

	if os.path.isdir(sourcedir+'\\'+item):
		matchObj = re.match( r'(.*)StepMultigaosheng2', item, re.M|re.I)
		if matchObj:
			symbol=matchObj.group(1).strip(" ")

			sql="select s_id from symbol_id where symbol='%s'" % (symbol)
			res=ms.dict_sql(sql)
			s_id=res[0]['s_id']
			# print symbol,s_id
			aflfiles=os.listdir(sourcedir+'\\'+item)
			for files in aflfiles:
				ff=open(sourcedir+'\\'+item+'\\'+files,'r')
				con=ff.read()
				patt=r'StrategyID = "(.*)";'
				mma=re.search(patt,con)
				if mma:
					st= mma.group(1)
					#print p_basic
					#print item+','+str(s_id)+','+str(st)+','+str(1)+','+str(1)
			#print p_follow
			# print 'StepMultituji1,'+item+',1,1,'+str(s_id)+',1'
			# sql=" insert into p_follow select 'StepMultigaosheng1' as ac, left(f_ac,CHARINDEX('StepMulti',f_ac)-1)+'StepMultigaosheng1',ratio,Pratio,stock,type,'AB' from p_follow where ac = 'StepMultiI300w_up'"
			# test "select * from p_follow  pf  inner join AC_RATIO a  on pf.F_ac=a.AC and pf.AC='StepMultigaosheng1'  left join P_BASIC p  on pf.F_ac=p.AC"
			#ac_ratio
			aflnum=6
			#print item+','+str(s_id)+',1,'+str(round(10.0/aflnum*100,3))+','+str(round(10.0/aflnum*100))+',AB'

		else:
			print "no symbol",targetdir+'\\'+filemame
			exit()

	# 	secondaflfiles=os.listdir(sourcedir+'\\'+item)
	# 	for item1 in secondaflfiles:
	# 		newfilename=symbol+"-"+item1
	# 		oldfile=sourcedir+"\\"+item+"\\"+item1
	# 		newfile=targetdir+"\\"+newfilename
	# 		shutil.copyfile(oldfile,newfile)
	# print filemame,'文件夹'
