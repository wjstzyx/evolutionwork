# -*- coding: gb18030 -*- 
import string, os
import shutil
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
dir = r'G:\add_afl\aflfiles'

def get_filename_list():
	filelists=[]
	files = os.listdir(dir)  
	for f in files:  
	    #print  f.decode('gbk') 
	    filelists.append(f.decode('gbk'))
	return filelists
	# for root, dirs, files in os.walk(dir):  
	#     for name in files:  
	#         print os.path.join(root, name)  



#need to del first
def pipei_regular(teststring):
	to_movelist=['Formulas/Custom/Helper/TradeHelper.afl',\
				 'Formulas/Custom/helper/BacktestHelper.afl',\
				 'Formulas/Custom/Helper/getPerformance.afl',\
				 'Formulas/Custom/Helper/TRADEHelper.afl',\
				 'OptimizerSetEngine("',\
				 'OptimizerSetOption("',\
				 'TickerNAME = Name();',\
				 'getPSumTrade','getPSumDay','getPSumMonth',\
				 'getTradingtimes','getWinRate','getProfit',\
				 'getMaxDrawdown',\
				 'AddColumn',\
				 'Filter=1;',\
				 'StrategyName =',\
				 'StrategyID =',\
				 'ProType = 1;',\
				 'Buy = BSIG;',\
				 'Short = SSIG;',\
				 'Sell= CSIG;',\
				 'Cover = CSIG;',\
				 'Sell = Cover = CSIG;',\
				 'Trading_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);',\
				 'Plot(0,StrategyName,colorBlack,styleNoLine);',\
				 'Trading_night_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);',\
				 'Trading_all_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);',\
				 'Trading_log_sumps(sumps,StrategyID,StrategyName,1);',\
				 'Trading_log_sumps_night(sumps,StrategyID,StrategyName,1);',\
				 'Trading_log_sumps_all(sumps,StrategyID,StrategyName,1);',\

				 ]
	istomovw=1
	for item in to_movelist:
		item=item.replace(" ","")
		teststring=teststring.replace(" ","")
		if item.lower() in teststring.lower():
			istomovw=0
	return istomovw

# pipei_regular()


def del_head_info(testlist,StrategyID,dayornight,sum_or_one):
	filepath=dir+'\\'+testlist
	filepathnew=dir+'\\'+testlist.split('.')[0]+'_new.afl'
	# print filepath
	# print filepathnew
	isbsig=0
	with open(filepath,'r') as f:
		with open(filepathnew,'w') as g:
			g.write('#include "Formulas/Custom/helper/BacktestHelper.afl";\r')
			g.write('#include "Formulas/Custom/helper/TradeHelper.afl";\r')
			g.write('OptimizerSetEngine("spso");\r')
			g.write('OptimizerSetOption("Runs", 1 );\r')
			g.write('OptimizerSetOption("MaxEval", 1000);\r')
			g.write('TickerNAME = Name();\r')

			for line in f.readlines():
				linelist=line.split("\r")
				for item in linelist:
					if pipei_regular(item):
						g.write(item)
				if 'plotperformance(bsig,ssig,csig);' in line.lower():
					isbsig=1			
			#ADD tailf info

			g.write('\rStrategyName = "%s";\r' % (testlist.split('.')[0]))
			g.write('StrategyID = "%s";\r' % (StrategyID))
			g.write('ProType = 1;\r')
			g.write('Buy = BSIG;\r')
			g.write('Short = SSIG;\r')
			g.write('Sell = Cover = CSIG;\r')
			isokey=0
			if dayornight=='day' and sum_or_one=='one':
				g.write('Trading_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);\r')
				isokey=1
			if dayornight=='night' and sum_or_one=='one':
				g.write('Trading_night_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);\r')
				isokey=1
			if dayornight=='all' and sum_or_one=='one':
				g.write('Trading_all_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);\r')
				isokey=1
			if dayornight=='day' and sum_or_one=='sum':
				g.write('Trading_log_sumps(sumps,StrategyID,StrategyName,1);\r')
				isokey=1
			if dayornight=='night' and sum_or_one=='sum':
				g.write('Trading_log_sumps_night(sumps,StrategyID,StrategyName,1);\r')
				isokey=1
			if dayornight=='all' and sum_or_one=='sum':
				g.write('Trading_log_sumps_all(sumps,StrategyID,StrategyName,1);\r')
				isokey=1
	if isokey==0:
		print "Didn't add Trading_log"
		exit()	
	if isbsig==0:
		print testlist,"222"
	shutil.move(filepathnew, filepath)


def all_file(numtpe,dayornight,sum_or_one):
	#get max StrategyID
	lenth1=len(numtpe)
	newnum=numtpe
	for i in range(10-lenth1):
		newnum=str(newnum)+'0'
	print 	numtpe,newnum

	sql="select top 1 max(st) as st from [LogRecord].[dbo].[all_st_list] where st like '%s%%' and st>='%s'" % (numtpe,newnum)
	res=ms.dict_sql(sql)
	if res[0]['st'] is not None:
		StrategyID1=int(res[0]['st'])+1
	else:
		StrategyID1='no'
	sql="select top 1 max(st) as st from [Future].[dbo].[Trading_logSymbol] where st like '%s%%' and st>='%s'" % (numtpe,newnum)
	res=ms.dict_sql(sql)
	if res[0]['st'] is not None:
		StrategyID2=int(res[0]['st'])+1
	else:
		StrategyID2='no'
	sql="select top 1 max(st) as st from [Future].[dbo].[P_BASIC] where st like '%s%%' and st>='%s'" % (numtpe,newnum)
	res=ms.dict_sql(sql)
	if res[0]['st'] is not None:
		StrategyID3=int(res[0]['st'])+1
	else:
		StrategyID3='no'
	#get max
	if StrategyID1=='no' and StrategyID2=='no' and StrategyID3=='no':
		print "##########################"
		print "this is new stnum "
		print "##########################"
		if len(numtpe)==10:
			StrategyID=int(numtpe)
		else:
			print "##########################"
			print "error:Please input the right ST(length equals 10 )"
			print "##########################"
			exit()
	else:
		if StrategyID1=='no':
			StrategyID1=0
		if StrategyID2=='no':
			StrategyID2=0
		if StrategyID3=='no':
			StrategyID3=0
		StrategyID=max(StrategyID1,StrategyID2,StrategyID3)
		if len(str(StrategyID))<8:
                        print "##########################"
			print "Find short-lenth StrategyID %s" % (StrategyID)
			print "Please input Number with more than 7 numbers"
			print "##########################"
			exit()
	print StrategyID


	#StrategyID=99210166
	filelists=get_filename_list()
	isreplicate=0
	for item in filelists:
		#if st is unique:
		sql="select top 1 st from [LogRecord].[dbo].[all_st_list] where st='%s'" % (StrategyID)
		res1=ms.dict_sql(sql)
		if res1:
			isreplicate=1
			print "There already exits the ST:",StrategyID
			exit()
		else:
			if item.split('.')[1]=='afl':
				del_head_info(item,str(StrategyID),dayornight,sum_or_one)
				listname=item.split('.')[0].replace("'","")
				sql="insert into [LogRecord].[dbo].[all_st_list](st,[filename],[inserttime]) values('%s','%s',getdate())" % (str(StrategyID),listname)
				# print sql 
				ms.insert_sql(sql)
				StrategyID=StrategyID+1





numtpe=sys.argv[1]
#numtpe='10621'
dayornight=sys.argv[2]
#dayornight=day day;dayornight=night night;dayornight=all all

sum_or_one=sys.argv[3]
#sum_or_one=one;sum_or_one=sum




all_file(numtpe,dayornight,sum_or_one)

