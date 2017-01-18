#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import os 
import re
import shutil
import csv
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-




sourcedir=r'G:\add_afl\TEMP'
symboldir=os.listdir(sourcedir)
p_basic_csv=csv.writer(file('p_basic_csv.csv', 'wb'))
ac_ratio_csv=csv.writer(file('ac_ratio_csv.csv', 'wb'))
p_follow_csv=csv.writer(file('p_follow_csv.csv', 'wb'))
for item in symboldir:
	if os.path.isdir(sourcedir+'\\'+item):
		matchObj = re.match( r'(.*)(StepMulti.*)', item, re.M|re.I)
		if matchObj:
			symbol=matchObj.group(1).strip(" ")
			acname=matchObj.group(2).strip(" ")

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
					#getratio
					sql="SELECT [ratio]  FROM [LogRecord].[dbo].[all_st_list] where st='%s'" % (st)
					res=ms.dict_sql(sql)
					myratio=res[0]['ratio']
					#print p_basic
					#p_basic=item+','+str(s_id)+','+str(st)+','+str(1)+','+str(1)
					p_basic=[item,str(s_id),str(st),round(myratio,4),round(myratio,4)]
					p_basic_csv.writerow(p_basic)

			#print p_follow
			# print 'StepMultituji1,'+item+',1,1,'+str(s_id)+',1'
			# 300W CASH
			myf_ac=symbol+"StepMultiI_up"
			sql="SELECT ratio  FROM [Future].[dbo].[p_follow]   where ac = 'StepMultiI300w_up' and F_ac='%s'" % (myf_ac)
			res=ms.dict_sql(sql)
			myratio1=res[0]['ratio']
			p_follow=[acname,item,myratio1,myratio1,s_id,1]
			p_follow_csv.writerow(p_follow)

			# sql=" insert into p_follow select 'StepMultigaosheng1' as ac, left(f_ac,CHARINDEX('StepMulti',f_ac)-1)+'StepMultigaosheng1',ratio,Pratio,stock,type,'AB' from p_follow where ac = 'StepMultiI300w_up'"
			# test "select * from p_follow  pf  inner join AC_RATIO a  on pf.F_ac=a.AC and pf.AC='StepMultigaosheng1'  left join P_BASIC p  on pf.F_ac=p.AC"
			#ac_ratio
			aflnum=6
			#print item+','+str(s_id)+',1,'+str(round(10.0/aflnum*100,3))+','+str(round(10.0/aflnum*100))+',AB'
			ac_ratio=[item,str(s_id),1,100,100,'AB']
			ac_ratio_csv.writerow(ac_ratio)


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
