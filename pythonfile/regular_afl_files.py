# -*- coding: gb18030 -*- 
import string, os
import shutil
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
dir = r'C:\Users\YuYang\Desktop\test'

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




def pipei_regular(teststring):
	to_movelist=['Formulas/Custom/Helper/TradeHelper.afl','Formulas/Custom/helper/BacktestHelper.afl','Formulas/Custom/Helper/getPerformance.afl','Formulas/Custom/Helper/TRADEHelper.afl','getPSumTrade','getPSumDay','getPSumMonth','getTradingtimes','getWinRate','getProfit','getMaxDrawdown','AddColumn','Filter=1;','StrategyName =','StrategyID =','ProType = 1;','Trading_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);','Plot(0,StrategyName,colorBlack,styleNoLine);']
	istomovw=1
	for item in to_movelist:
		if item.lower() in teststring.lower():
			istomovw=0
	return istomovw

# pipei_regular()


def del_head_info(testlist,StrategyID):
	filepath=dir+'\\'+testlist
	filepathnew=dir+'\\'+testlist.split('.')[0]+'_new.afl'
	# print filepath
	# print filepathnew
	isbsig=0
	with open(filepath,'r') as f:
		with open(filepathnew,'w') as g:
			g.write('#include "Formulas/Custom/helper/BacktestHelper.afl";\r')
			g.write('#include "Formulas/Custom/Helper/TradeHelper.afl";\r')
			for line in f.readlines():
				linelist=line.split("\r")
				for item in linelist:
					if pipei_regular(item):
						g.write(item)
				if 'plotperformance(bsig,ssig,csig);' in line.lower():
					isbsig=1			
			#ADD tailf info
			g.write('StrategyName = "%s";\r' % (testlist.split('.')[0]))
			g.write('StrategyID = "%s";\r' % (StrategyID))
			g.write('ProType = 1;\r')
			g.write('Trading_log(BSIG,SSIG,CSIG,StrategyID,StrategyName,ProType);\r')
			g.write('Buy = BSIG;\r')
			g.write('Short = SSIG;\r')
			g.write('Sell = Cover = CSIG;\r')
	if isbsig==0:
		print testlist,"222"
	shutil.move(filepathnew, filepath)


def all_file():
	sql="select MAX(st)  as st from P_backtest_st_name"
	res=ms.dict_sql(sql)
	StrategyID=int(res[0]['st'])+1
	print StrategyID
	StrategyID=99210166
	filelists=get_filename_list()
	for item in filelists:
		if item.split('.')[1]=='afl':
			del_head_info(item,str(StrategyID))
			listname=item.split('.')[0].replace("'","")
			sql="insert into [Future].[dbo].[P_backtest_st_name](st,name,[inserttime]) values('%s','%s',getdate())" % (str(StrategyID),listname)
			print sql 
			ms.insert_sql(sql)
			StrategyID=StrategyID+1







all_file()

