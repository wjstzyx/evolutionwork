#coding=utf-8 
#!/usr/bin/env python
###检测st_report 和P_LOG 的联合记录是否连续

import sys
import threading
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def change_lianxu(stname):
	sql="select top 1 stockdate from st_report where st=%s order by stockdate" % (stname)
	firsttime=ms.find_sql(sql)[0][0]
	sql="select 'update st_report set pp='+str(pp)+' where id='+str(id)+';' as script,pp,id,p from st_report where stockdate='%s' and st=%s" % (firsttime,stname)
	myscript=ms.find_sql(sql)[0]
	if myscript[1]!=0:
		print '--**** backup-script:'
		print myscript[0]
		print "--**** Need to do"
		sql="update st_report set pp=0 where id=%s" % (myscript[2])
		print sql
	lastpsig=myscript[3]
	sql="select stockdate,p,pp,id from st_report where st=%s and stockdate>'%s' order by stockdate" % (stname,firsttime)
	tiemres=ms.find_sql(sql)
	print "--************  Ready to Backup *************"
	for item in tiemres:
		if item[2]!=lastpsig:
			sql="update st_report set pp=%s where id=%s" % (lastpsig,item[3])
			ms.insert_sql(sql)
			tempsql="update st_report set pp=%s where id=%s;" % (item[2],item[3])
			print tempsql
		lastpsig=item[1]

def set_pp_zerp():
	sql="select id,p,pp,a.st,a.d,a.t from st_report a right join (select min(stockdate) as stockdate,st from st_report  group by st) temp on temp.ST=a.ST and temp.stockdate=a.stockdate where pp!=0 and PP is not null "
	res=ms.find_sql(sql)
	for item in res:
		if 	item[2]!=0:
			sql="update st_report set pp=%s where id=%s" % (item[2],item[0])
			print "--Ready to backup:"
			print sql
			sql="update st_report set pp=0 where id=%s" % (item[0])
			ms.insert_sql(sql)


def set_p_zerp():
	sql="select id,p,pp,a.st,a.d,a.t from st_report a right join (select max(stockdate) as stockdate,st from st_report  group by st) temp on temp.ST=a.ST and temp.stockdate=a.stockdate where p!=0 and P is not null and a.stockdate<='2016-04-1 09:49:00.000' order by a.stockdate "
	res=ms.find_sql(sql)
	for item in res:
		if 	item[1]!=0:
			sql="update st_report set p=%s where id=%s" % (item[1],item[0])
			print "--Ready to backup:"
			print sql
			sql="update st_report set p=0 where id=%s" % (item[0])
			ms.insert_sql(sql)





def fix_lianxu():
	sql="select * from (select SUM(P) as p,SUM(pp) as pp,SUM(p-pp) as aap,st from st_report group by st )aaa where aap!=0 order by st "
	#sql="select distinct ST_REPORT.ST from st_report inner join p_log p on p.st=st_report.st and p.ac='RbCX_QGtr' and p.symbol='RB' and p.d=st_report.d and st_report.type=0"
	res=ms.find_sql(sql)
	for item in res:
		print "--st: ",item[3]
		st=item[3]
		change_lianxu(st)




def test_ac_symbol_st_lianxu(ac,symbol,st):
	sql="select st_report.* from st_report inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and st_report.st=%s and p.d=st_report.d and st_report.type=0 order by stockdate" % (ac,symbol,st)
	itemres=ms.dict_sql(sql)
	lastpsig=itemres[0]['P']
	for item1 in itemres[1:]:
		thepp=item1['PP']
		if thepp!=lastpsig:
			print "***************************************************************"
			print ac,symbol,st,item1['stockdate']	
			print sql
			print "select * from st_report where st=%s order by stockdate" % (st)
			#change_lianxu(st)
			break
		else:
			lastpsig=item1['P']
			print "1"



def test_ac_symbol_lianxu(ac,symbol):
	sql="select distinct st_report.st from st_report inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and p.d=st_report.d and st_report.type=0 where st_report.st>415154 order by st" % (ac,symbol)
	print sql
	res=ms.dict_sql(sql)
	for item in res:
		st=item['st']
		sql="select st_report.* from st_report inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and st_report.st=%s and p.d=st_report.d and st_report.type=0 order by stockdate" % (ac,symbol,st)
		print sql
		itemres=ms.dict_sql(sql)
		lastpsig=itemres[0]['P']
		for item1 in itemres[1:]:
			thepp=item1['PP']
			if thepp!=lastpsig:
				print ac,symbol,item1['stockdate']	
				print "select * from st_report where st=%s order by stockdate" % (st)
				# change_lianxu(st)
				sql="insert into [LogRecord].[dbo].[errorstlist]([Symbol],[AC],[ST],[StockDate],[inserttime]) values('%s','%s','%s','%s',getdate())" % (ac,symbol,st,item1['stockdate'])
				ms.insert_sql(sql)
			else:
				lastpsig=item1['P']





def test_ac_symbol_pp(ac,symbol):
	sql="select st_report.ST,MIN(stockdate) as stockdate from st_report inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and p.d=st_report.d and st_report.type=0 group by st_report.ST" % (ac,symbol)
	res=ms.dict_sql(sql)
	for item in res:
		ST=item['ST']
		stockdate=item['stockdate']
		sql="select min(stockdate) as stockdate from st_report where st=%s" % (ST)
		minstockdate=ms.dict_sql(sql)[0]['stockdate']
		if minstockdate!=stockdate:
			print "ST:minstockdate is not the same "
			print "stname: %s" % (ST)
			print "st_report: %s" % (minstockdate)
			print "p_log: %s" % (stockdate)








def main_test_sig():
	i=0
	RBlist=('Rb_QGpLud','RbCX_QGRev','RbCX_QGtr','RB_CXVolume','RB_Daybreaker','RB_LiangtuPipei','RB_LRC_Trend','RB_LUD','RB_MT','RB_RBreaker','RB_RSI','RB_ST_Reversal','RB_ST_Trend','RB_VPIN','RB_ZhixianPipei','CH4RBZS','DAYGAPRB','RBHAL','PUDRB','RBSV','UDKRB','V7RB')
	CUlist=('CUDUDHL','ESPcu','CU-LKVCU1','CU-LKVCU2','CUPUDCU','QCU18MIN','QPMCU','CUVk2CU','CUVK3')
	AGlist=('9AGOLD','9AGVD05','9AGVD06','AGNEW4','AGNEW6','AGNEW8','AGNEW19','AGNEWLVO')
	IClist=('YEEXIC','YEOTIC','YETRIC','YEZHIC')
	IFlist=('9CPPUD','9DayBrIF','9Distance','9DUD1','9DUDHL','9DUDRV','9EXR1410','9EXV1410','9FORCE','9FQS1','9HAL','9HAL2','9HAL3','9HALMA','9HUITIAO','9HUITIAO2','9HUITIAO3','9HUITIAO4','9KDHDAY','9KDHPM','9Linerate','9RATE','9MALONGK','9MiddayTrend','9MinVolPbuy','9MONDAY','9MORNINGOUT','9MT','9MVRATE','9NHL','9NOON','9OpenBet','9QMA','9QPMIF','9Reversal','9Reversal2','9Reversal3','9V4EIV','9VK1','9VK3','9VPINVOl_L','9VPINVOl_S','9VPINVOl_S2','9wb','9weipan','9WeipanREV','9WeipanStatics','9YAP01','9YY2','9YYMA','9LUD','9LUD2CH','9LUD3','9LUD4','9LUD5','9LUD6','9LUD7','9LUD8','9LUD10','9LUD11V2','9LUD13','9LUD14','9LUD16','9LUDCH1','9LUDCH4','9LUDCH5','9LUDCH6','9LUDCH8','LUD52015','LUD62015','LUD72015','LUD82015','TimeV2Pm','TimeV3DtaPm','TimeV3HLAm','TimeV3HLPm','V4EIVelements','V4EIVNEW','IFQG1310','IFQGEX','IFQGOT','9QGBombma2','IFQGTB','IFQGTR','IFQGWB','YEQGTR','YEQGEX','YEQGOT','YEQGZH211')
	# for item in IFlist[88:]:
	# 	ac=item
	# 	symbol='IF'
	# 	print i,ac,symbol
	# 	test_ac_symbol_lianxu(ac,symbol)

	for item in IClist[2:]:
		ac=item
		symbol='IC'
		print i,ac,symbol
		i=i+1
		test_ac_symbol_lianxu(ac,symbol)

	# for item in AGlist:
	# 	ac=item
	# 	symbol='AG'
	# 	print i,ac,symbol
	# 	i=i+1
	# 	test_ac_symbol_lianxu(ac,symbol)

	# for item in CUlist:
	# 	ac=item
	# 	symbol='CU'
	# 	print i,ac,symbol
	# 	i=i+1
	# 	test_ac_symbol_lianxu(ac,symbol)
	# for item in RBlist:
	# 	ac=item
	# 	symbol='RB'
	# 	print i,ac,symbol
	# 	i=i+1
	# 	test_ac_symbol_lianxu(ac,symbol)








#set_pp_zerp()
#set_p_zerp()
# fix_lianxu()
#change_lianxu('423612')
#test_ac_symbol_pp('RbCX_QGtr','RB')
# change_lianxu(423615)
main_test_sig()
# test_ac_symbol_lianxu('YEQGTR','IF')