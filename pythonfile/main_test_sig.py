#coding=utf-8 
#!/usr/bin/env python
###检测st_report 和P_LOG 和Tsymbol的联合记录是否连续

import sys
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
	sql="select stockdate,p,pp,id from st_report where st=%s and stockdate>'%s' order by stockdate,id" % (stname,firsttime)
	tiemres=ms.find_sql(sql)
	print "--************  Ready to Backup *************"
	for item in tiemres:
		if item[2]!=lastpsig:
			sql="update st_report set pp=%s where id=%s" % (lastpsig,item[3])
			ms.insert_sql(sql)
			tempsql="update st_report set pp=%s where id=%s;" % (item[2],item[3])
			print tempsql
		lastpsig=item[1]



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
	sql="select distinct st_report.st from st_report inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and p.d=st_report.d and st_report.type=0  order by st" % (ac,symbol)
	res=ms.dict_sql(sql)
	i=0
	for item in res:
		st=item['st']
		i=i+1
		print 'stnum:',i,st
		sql="select st_report.* from st_report inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and st_report.st=%s and p.d=st_report.d and st_report.type=0 order by stockdate,st_report.id" % (ac,symbol,st)
		itemres=ms.dict_sql(sql)
		lastpsig=itemres[0]['P']
		for item1 in itemres[1:]:
			thepp=item1['PP']
			if thepp!=lastpsig:
				print ac,symbol,item1['stockdate']	
				print "not lianxu"
				print "select * from st_report where st=%s order by stockdate,id" % (st)
				print sql
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



def test_record_num(ac,symbol):
	sql1="select st_report.id,st_report.p,st_report.pp,p.symbol,st_report.stockdate,st_report.st,p.p_size,p.ac,p.ratio,p.d from st_report  inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and p.d=st_report.d and st_report.type=0 ORDER by stockdate,st,id" % (ac,symbol)
	# print sql
	st_log_record=ms.find_sql(sql1)
	sql2="select temp.* from Tsymbol o inner join  (select st_report.id,st_report.p,st_report.pp,p.symbol,st_report.stockdate,st_report.st,p.p_size,p.ac,p.ratio,p.d from st_report  inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and p.d=st_report.d and st_report.type=0) temp on temp.stockdate=o.stockdate and o.symbol=temp.symbol ORDER by stockdate,st,id" % (ac,symbol)
	# print sql
	st_log_Tsymbol_record=ms.find_sql(sql2)
	if len(st_log_record)==len(st_log_Tsymbol_record):
		# print ac,symbol,"test_record_num Ok"
		return 1
	else:
		print sql1
		print sql2
		tempres=list(set(st_log_record).difference(set(st_log_Tsymbol_record)))
		print "************Difference Time:*******************"
		for item in tempres:
			print item[4]
		return 0






def sub_test_itemlist(itemlist,symbol):
	i=0
	for item in itemlist:
		ac=item
		i=i+1
		print i,ac,symbol
		numresult=test_record_num(ac,symbol) # st_report P_log 的联合记录和 st_report P_log Tsymbol的联合记录比较
		if numresult==1 or 1==1:
			test_ac_symbol_lianxu(ac,symbol) # 测试st_report P_log Tsymbol的联合记录 st是否信号连续








def main_test_sig():
	i=0
	TAlist=('CH4tazs','DayBrTA','DayTALineRrate')
	RUlist=('RUDTA','RUMY','RUV4E','RUv4ehc','RUV7','RUWEEKLY')
	RBlist=('Rb_QGpLud','RbCX_QGRev','RbCX_QGtr','RB_CXVolume','RB_Daybreaker','RB_LiangtuPipei','RB_LRC_Trend','RB_LUD','RB_MT','RB_RBreaker','RB_RSI','RB_ST_Reversal','RB_ST_Trend','RB_VPIN','RB_ZhixianPipei','CH4RBZS','DAYGAPRB','RBHAL','RBPUD','RBSV','UDKRB','V7RB')
	CUlist=('CUDUDHL','ESPcu','LKVCU1','LKVCU2','PUDCU','QCU18MIN','QPMCU','Vk2CU','CUVK3')
	AGlist=('9AGOLD','9AGVD05','9AGVD06','AGNEW4','AGNEW6','AGNEW8','AGNEW19','AGNEWLVO')
	IClist=('YEEXIC','YEOTIC','YETRIC','YEZHIC')
	IFlist=('9CPPUD','DayBrIF','9Distance','9DUD1','9DUDHL','9DUDRV','9EXR1410','9EXV1410','9FORCE','9FQS1','9HAL','9HAL2','9HAL3','9HALMA','9HUITIAO','9HUITIAO2','9HUITIAO3','9HUITIAO4','9KDHDAY','9KDHPM','9Linerate','9RATE','9MALONGK','9MiddayTrend','9MinVolPbuy','9MONDAY','9MORNINGOUT','9MT','9MVRATE','9NHL','9NOON','9OpenBet','9QMA','9QPMIF','9Reversal','9Reversal2','9Reversal3','9V4EIV','9VK1','9VK3','9VPINVOl_L','9VPINVOl_S','9VPINVOl_S2','9wb','9weipan','9WeipanREV','9WeipanStatics','9YAP01','9YY2','9YYMA','9LUD','9LUD2CH','9LUD3','9LUD4','9LUD5','9LUD6','9LUD7','9LUD8','9LUD10','9LUD11V2','9LUD13','9LUD14','9LUD16','LUDch1','LUDch4','LUDch5','LUDch6','LUDch8','LUD52015','LUD62015','LUD72015','LUD82015','TimeV2Pm','TimeV3DtaPm','TimeV3HLAm','TimeV3HLPm','V4EIVelements','V4EIVNEW','IFQG1310','IFQGEX','IFQGOT','9QGBombma2','IFQGTB','IFQGTR','IFQGWB','YEQGTR','YEQGEX','YEQGOT','YEQGZH211')
	# sub_test_itemlist(TAlist,'TA')
	# sub_test_itemlist(RUlist,'RU')
	# sub_test_itemlist(RBlist,'RB')
	# sub_test_itemlist(CUlist,'CU')
	# sub_test_itemlist(AGlist,'AG')
	sub_test_itemlist(IClist,'IC')
	# sub_test_itemlist(IFlist,'IF')



main_test_sig()




# change_lianxu(50037)
# test_ac_symbol_lianxu('9AGOLD','AG')

def update_pp():
	sql="select a.* from st_report a inner join (select MIN(stockdate) as stockdate ,st_report.st from st_report  inner join p_log p on p.st=st_report.st and p.ac='IFQGWB' and p.symbol='IF' and p.d=st_report.d and st_report.type=0 group by st_report.st ) temp on a.stockdate = temp.stockdate and a.st=temp.ST "
	res=ms.dict_sql(sql)
	i=0
	for item in res:
		if item['PP']!=0:
			i=i+1
			# print i
			sql1="update st_report set pp=%s where id=%s" % (item['PP'],item['id'])
			print sql1
			sql="update st_report set pp=0 where id=%s" % (item['id'])
			ms.insert_sql(sql)
# update_pp()