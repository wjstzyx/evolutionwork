#coding=utf-8 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import re


root=sys.path[0]
# root=r'C:\Users\YuYang\Desktop\old虚拟组'
uroot=unicode(root,'utf-8')
a=os.walk(uroot)


for path,d,filelist in a:
	for item in filelist:
		if item[-4:]=='.afl':
			pattern=r'StrategyID\s*=\s*"*(.*)"*;'
			tempfile=path+"\\"+item
			f=open(tempfile,'r')
			content=f.read()
			match=re.findall(pattern,content)
			if len(match)==1:
				st=match[0]
				print st,tempfile
			if len(match)>1:
				print "#################find more st num", match,tempfile
			f.close()

	# print d
	# print filelist
# str='StrategyID = 1013000013;StrategyID = 1013000013;StrategyID = 1013000013;'
# pattern1=r'StrategyID\s*=\s*(210098);'
# pattern2=r'StrategyID\s*=\s*"*(1013000013)"*;'
# match=re.findall(pattern2,str)
# if match:
# 	print match
