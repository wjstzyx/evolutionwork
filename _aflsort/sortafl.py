#coding=utf-8 
#####################
#此功能进行统计的Afl去重，过滤作用
#####################
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import re
import hashlib
import time
import shutil
import csv
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")


root=r'C:\YYfiles\evolutionwork\_aflsort'


def put_info_intable():
	#将afl按照现在的文件夹格式重新生成路径
	filedir=os.listdir(root)
	for item in filedir:
		if os.path.isdir(item):
			fisrtdir=os.path.join(root,item)
			csvfile=os.path.join(fisrtdir,'on_afl_st.csv')
			f=open(csvfile,'r')
			content=csv.reader(f,delimiter=',')
			tempc=[]
			for aa in content:
				tempc.append(aa)
			content=tempc
			for aa in content:
				st=aa[0]
				if len(aa)==2:
					aafiledir=aa[1]
				else:
					aafiledir =",".join(aa[1:])
				#重新组建路径
				aafiledir=aafiledir.split("D:\\machinename\\")[1]
				newfilepath=os.path.join(fisrtdir,aafiledir)
				print newfilepath
				newfilepath=newfilepath.replace("'","''")
				machine='192.168.0.'+item.split('_')[1]
				filename=os.path.basename(newfilepath)
				temp=os.path.dirname(newfilepath)
				firstparent=os.path.basename(temp)
				temp=os.path.dirname(temp)		
				secondparent=os.path.basename(temp)
				temp=os.path.dirname(temp)	
				thirdparent=os.path.basename(temp)
				sql="insert into [LogRecord].[dbo].[afl_filepath_sort]([st] ,[filepath],[machine],[basename]  ,[firstparent]  ,[secondparent]   ,[thirdparent]) values('%s','%s','%s','%s','%s','%s','%s')" % (st,newfilepath,machine,filename,firstparent,secondparent,thirdparent)
				ms.insert_sql(sql)
			f.close()



def compare_different_st():
	sql="select distinct st from [LogRecord].[dbo].[afl_filepath_sort] where isactive=0 order by st"
	stlist=ms.dict_sql(sql)
	for item in stlist:
		print item 
		issame=1
		st=item['st']
		sql="select distinct [filepath],id from [LogRecord].[dbo].[afl_filepath_sort] where st='%s'" % (st)
		tempcontent=""
		res=ms.dict_sql(sql)
		for con in res:
			file=con['filepath']
			f=open(file,'r')
			temp=f.read()
			temp=temp.replace('//PlotPerformance(bsig,ssig,Csig);','PlotPerformance(bsig,ssig,Csig);')
			temp=temp.replace('Trading_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);','')

			# m2 = hashlib.md5()   
			# m2.update(temp)   
			# md5value=m2.hexdigest()
			# sql="update [LogRecord].[dbo].[afl_filepath_sort] set [md5value]='%s' where id=%s" % (md5value,con['id'])
			# ms.insert_sql(sql)

			if tempcontent!="" and temp!=tempcontent:
				issame=0
				print 'not same',item,file
				break
			tempcontent=temp
		if issame==1:
			sql="update [LogRecord].[dbo].[afl_filepath_sort] set [isactive]=1 where st='%s'" % (st)
			ms.insert_sql(sql)









# put_info_intable()
compare_different_st()