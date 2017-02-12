#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime
import time
import os
import numpy as np
import pandas as pd
from openpyxl.writer.excel import ExcelWriter
from pandas.tseries import offsets
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
#ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms = MSSQL(host="27.115.14.62:3888",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

global lilun_total
global real_total
global lilun_total_ZL
global real_total_ZL
global totalroot
global totalresult_df1
global totalresult_df2
global totalresult_df3
step_acname='StepMultiI300w_up'
replacestr='StepMultiI_up'
account='666061010'
totalratio=2.2
equity_day='2017-01-20'
lilun_result=[]
real_account_result=[]
real_huibao_result=[]




lilun_total=[]
real_total=[]
lilun_total_ZL=[]
real_total_ZL=[]
endtime=equity_day+" 16:00:00"
sql="select  distinct top (4) convert(nvarchar(10),stockdate,120) as day from TSymbol where StockDate<='%s' order by day desc" % (equity_day)
beginday=ms.find_sql(sql)
begintime=beginday[-1][0]
filepath = os.path.split(os.path.realpath(__file__))[0]
totalroot = os.path.dirname(filepath)
if not totalroot+"\\all_future_position\\results":
	os.makedirs(totalroot+"\\all_future_position\\results")
totalresults=pd.DataFrame()

excel_file=totalroot+"\\all_future_position\\results\\"+str(equity_day)+".xls"




def write_position_csv(type,symbol,endtime='2017-11-12',df1=1):
	filepath = os.path.split(os.path.realpath(__file__))[0]
	parentpath = os.path.dirname(filepath)
	newpath=parentpath+'\\all_future_position\\'+type+"\\"+str(endtime)+"\\"+type+"_"+str(symbol)+'.csv'
	a_parent=os.path.dirname(newpath)
	if  not os.path.isdir(a_parent):
		os.makedirs(a_parent)
	df1.to_csv(newpath,sep=',',index=False)
	#print '## generate  position file ',symbol,newpath




#################general steps ########################
### setp 1 获取原始仓位序列 #####
def get_origin_position_list(p_followac,acname,ratio=1):
	sql="select q.ClosePrice,q.stockdate,round(q.totalposition*mr.ratio*%s,0) as totalposition ,q.symbol,sid.S_ID from p_follow p inner join quanyi_log_groupby_v2 q on p.F_ac=q.AC and p.AC='%s' inner join LogRecord.dbo.test_margin mr on q.symbol=mr.symbol inner join symbol_id sid on q.symbol=sid.Symbol where q.AC='%s' and stockdate>='%s' and stockdate<='%s' order by stockdate" % (ratio,p_followac,acname,begintime,endtime)

	res1=ms.dict_sql(sql)
	if res1:
		symbol=res1[0]['symbol']
		sql="select MAX(StockDate) as stockdate from TSymbol where symbol='%s' and StockDate>='%s' and StockDate<='%s' and t<='15:30'group by D order by D" % (symbol,begintime,endtime)
		insertstockdate=ms.dict_sql(sql)
		insertstockdate_pd=pd.DataFrame(insertstockdate)
		postionpd=pd.DataFrame(res1)
		postionpd=postionpd.append(insertstockdate_pd,ignore_index=True)
		postionpd=postionpd.sort_values(['stockdate'])
		postionpd = postionpd.fillna(method='ffill')
		return postionpd,symbol
	else:
		return pd.DataFrame(columns=['ClosePrice','S_ID','stockdate','symbol','totalposition']),'no'


def get_Tsymbol_by_symbol(symbol,postionpd):
	sql="select stockdate,C from TSymbol_allfuture where symbol='%s' and StockDate>='%s' and StockDate<='%s' order by StockDate" % (symbol,begintime,endtime)
	quotes=ms.dict_sql(sql)
	quotes_pd=pd.DataFrame(quotes)
	fisrsttime=postionpd['stockdate'].iloc[[0]].values[0]
	quotes_pd = quotes_pd[quotes_pd['stockdate']>=fisrsttime]
	#add 主力价格
	sql="select stockdate,C as CZL from TSymbol_ZL where symbol='%s' and StockDate>='%s' and StockDate<='%s' order by StockDate" % (symbol,begintime,endtime)
	quotes_zl=ms.dict_sql(sql)
	quotes_pd_zl=pd.DataFrame(quotes_zl)
	# 主力价格 和指数价格合在一起
	quotes_pd=pd.merge(quotes_pd,quotes_pd_zl,'outer',left_on='stockdate',right_on='stockdate')
	total=pd.merge(quotes_pd,postionpd,'outer',left_on='stockdate',right_on='stockdate')
	#排序
	total=total.sort_values(['stockdate'])
	total['C']=total['C'].fillna(method='ffill')
	total['CZL'] = total['CZL'].fillna(method='ffill')
	total=total[pd.notnull(total['totalposition'])]
	total=total.drop_duplicates()
	total=total[['stockdate','C','CZL','totalposition']]
	return total










def cal_equity(symbol,totalpo):
	#compute commvalue  pointvalue
	symbolto=symbol
	commvalue=1
	pointvalue=1
	sql="SELECT [symbol]  ,[multi] as [pointvalue]  ,[comm] as [commision] FROM [Future].[dbo].[Symbol_ID] where Symbol='%s'" % (symbolto)
	res=ms.dict_sql(sql)
	if res:
		pointvalue=res[0]['pointvalue']
		commvalue=res[0]['commision']
	#print pointvalue,commvalue
	totalpo['profit']=(totalpo['totalposition'].round()).shift()*(totalpo['C']-totalpo['C'].shift())*pointvalue
	totalpo['profit_ZL']=(totalpo['totalposition'].round()).shift()*(totalpo['CZL']-totalpo['CZL'].shift())*pointvalue
	totalpo['comm']=abs((totalpo['totalposition'].round())-(totalpo['totalposition'].shift().round()))*commvalue
	totalpo['equity']=totalpo['profit']-totalpo['comm']
	totalpo['equity_ZL']=totalpo['profit_ZL']-totalpo['comm']
	newtotalpo=totalpo
	return  newtotalpo
def cal_equity_huibao(symbol,totalpo):
	#compute commvalue  pointvalue
	symbolto=symbol
	commvalue=1
	pointvalue=1
	sql="SELECT [symbol]  ,[multi] as [pointvalue]  ,[comm] as [commision] FROM [Future].[dbo].[Symbol_ID] where Symbol='%s'" % (symbolto)
	res=ms.dict_sql(sql)
	if res:
		pointvalue=res[0]['pointvalue']
		commvalue=res[0]['commision']
	#print pointvalue,commvalue
	totalpo['profit']=(totalpo['totalposition'].round()).shift()*(totalpo['C']-totalpo['C'].shift())*pointvalue
	#totalpo['profit_ZL']=(totalpo['totalposition'].round()).shift()*(totalpo['CZL']-totalpo['CZL'].shift())*pointvalue
	totalpo['comm']=abs((totalpo['totalposition'].round())-(totalpo['totalposition'].shift().round()))*commvalue
	totalpo['equity']=totalpo['profit']-totalpo['comm']
	#totalpo['equity_ZL']=totalpo['profit_ZL']-totalpo['comm']
	newtotalpo=totalpo
	return  newtotalpo



def equity_resharp(newtotalpo):
	deltatime=offsets.DateOffset(hours=6)
	newtotalpo['stockdate']=newtotalpo['stockdate']+deltatime
	newtotalpo['day']=newtotalpo['stockdate'].apply(lambda x: x.strftime('%Y%m%d'))
	day_equity=pd.groupby(newtotalpo,'day').sum()
	return day_equity[['profit','comm','equity','profit_ZL','equity_ZL']]




	pass






	##############################
	pass
def equity_resharp_huibao(newtotalpo):
	deltatime=offsets.DateOffset(hours=6)
	newtotalpo['stockdate']=newtotalpo['stockdate']+deltatime
	newtotalpo['day']=newtotalpo['stockdate'].apply(lambda x: x.strftime('%Y%m%d'))
	day_equity=pd.groupby(newtotalpo,'day').sum()
	return day_equity[['profit','comm','equity']]




	pass






	##############################
	pass



# postionpd,symbol=get_origin_position_list('StepMultigaosheng1','csStepMultigaosheng1',1)
# totalpo=get_Tsymbol_by_symbol(symbol,postionpd)
# newtotalpo=cal_equity(symbol,totalpo)
# day_equity=equity_resharp(newtotalpo)
# print day_equity
# print 1
# exit()

def account_get_origin_position_list(account,symbolid,symbol):
	sql="SELECT 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and inserttime>='%s' and stockid=%s " % (account,endtime,begintime,symbolid)
	res1=ms.dict_sql(sql)
	if res1:
		postionpd=pd.DataFrame(res1)
		symbol=res1[0]['symbol']
	else:
		postionpd=pd.DataFrame([{'ClosePrice':0,'stockdate':datetime.datetime.strptime(begintime+" 00:00:00",'%Y-%m-%d %H:%M:%S'),'totalposition':0,'Symbol':symbol,'S_ID':symbolid}])
	sql="select MAX(StockDate) as stockdate from TSymbol where symbol='%s' and StockDate>='%s' and StockDate<='%s' and t<='15:30'group by D order by D" % (symbol,begintime,endtime)
	insertstockdate=ms.dict_sql(sql)
	insertstockdate_pd=pd.DataFrame(insertstockdate)

	postionpd=postionpd.append(insertstockdate_pd,ignore_index=True)
	postionpd=postionpd.sort_values(['stockdate'])
	postionpd = postionpd.fillna(method='ffill')
	return postionpd,symbol





# 计算 成交回报记录
def get_delta_info(symbol,symbolid):
	#获取成交回报
	sql="  select Future.dbo.m_getstr([InstrumentID]) as symbol,Direction,[Volume],  Price,convert(datetime,substring(TradeDate,0,5)+'-'+substring(TradeDate,5,2)+'-'+substring(TradeDate,7,2)+' '+[TradeTime],120) as stockdate from [Future].[dbo].[test_tradelog] where Future.dbo.m_getstr([InstrumentID])='%s' and convert(datetime,substring(TradeDate,0,5)+'-'+substring(TradeDate,5,2)+'-'+substring(TradeDate,7,2)+' '+[TradeTime],120)>='%s' order by stockdate " % (symbol,begintime)
	res=ms.dict_sql(sql)
	#如果一条记录都没有如何处理,选择最早的一条仓位信息
	abegintime=datetime.datetime.strptime(begintime,'%Y-%m-%d')
	sql="SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account,abegintime,symbolid)
	tempres=ms.dict_sql(sql)
	if tempres:
		alastposition=tempres[0]['totalposition']
		atime_position=tempres[0]['stockdate']
	else:
		print symbol,'不存在期货账户仓位信息'
		exit()
	sql="SELECT top 1 C  FROM [Future].[dbo].[TSymbol_ZL] where symbol='%s' and stockdate<='%s' order by stockdate desc" % (symbol,atime_position)
	# 如果找不到记录，则另 C=0
	tempres=ms.dict_sql(sql)
	if tempres:
		atime_price=ms.dict_sql(sql)[0]['C']
	else:
		atime_price=0

	addline={'stockdate':atime_position,'Direction':0,'Volume':0,'symbol':symbol,'Price':atime_price}
	if res:
		firsttime=res[0]['stockdate']
		if firsttime>abegintime:
			res.append(addline)
	else:
		res.append(addline)

	deltapd=pd.DataFrame(res)
	deltapd['deltaposition']=deltapd['Direction']*deltapd['Volume']
	# #get initial position
	# abegintime=res[0]['stockdate']
	# #  如果 这段时间没有成交记录，则选择开始时间的仓位信息
	# abegintime=min(abegintime,datetime.datetime.strptime(begintime,'%Y-%m-%d'))
	# sql="SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account,abegintime,symbolid)
	# alastposition=0
	# tempres=ms.dict_sql(sql)
	# alastposition=tempres[0]['totalposition']
	# atime_position=tempres[0]['stockdate']
	# sql="SELECT top 1 C  FROM [Future].[dbo].[TSymbol_ZL] where symbol='%s' and stockdate<='%s' order by stockdate desc" % (symbol,atime_position)
	# # 如果找不到记录，则另 C=0
	# tempres=ms.dict_sql(sql)
	# if tempres:
	# 	atime_price=ms.dict_sql(sql)[0]['C']
	# else:
	# 	atime_price=0
	# addline=pd.DataFrame([{'stockdate':atime_position,'deltaposition':0,'symbol':symbol,'Price':atime_price,}])
	# deltapd=deltapd.append(addline,ignore_index=True)
	deltapd['myindex']=deltapd.index
	deltapd=deltapd.sort_values(['stockdate','myindex'])



	deltapd['totalposition'] = deltapd['deltaposition'].cumsum()+alastposition
	# add everyday edntime
	sql="select stockdate,C as Price from [TSymbol_ZL] where symbol='%s' and stockdate in ( select MAX(StockDate) as stockdate from [TSymbol_ZL] where symbol='%s' and StockDate>='%s' and StockDate<='%s' and t<='15:30'group by D )" % (symbol,symbol,begintime,endtime)
	insertstockdate=ms.dict_sql(sql)
	insertstockdate_pd=pd.DataFrame(insertstockdate)
	deltapd=deltapd.append(insertstockdate_pd,ignore_index=True)
	deltapd=deltapd.sort_values(['stockdate','myindex'])
	deltapd = deltapd.fillna(method='ffill')
	deltapd['C']=deltapd['Price']
	deltapd=deltapd[deltapd['stockdate']<=endtime]
	return deltapd[['C','stockdate','symbol','totalposition']]





def merge_position_price(df1,df2):
	df2=df2[(df2['stockdate']<=endtime) & (df2['stockdate']>=begintime+' 01:00:00')]
	#df1 is [stockdate        C  totalposition  profit  comm  equity]
	#df2 is [stockdate symbol    price  deltapoint]
	aa=pd.merge(df1,df2,'outer',left_on=['stockdate'],right_on=['stockdate'])
	aa =aa.sort_values('stockdate')
	aa.to_csv(r'D:\test\bbb.csv',sep=',')






# postionpd,symbol=account_get_origin_position_list(account,1,'ru')
# totalpo = get_Tsymbol_by_symbol(symbol, postionpd)
# print 1
# exit()







def cal_ac_day_equity(p_followac,acname,ratio=1):
	postionpd, symbol = get_origin_position_list(p_followac, acname, ratio)
	#获取 指数 价格 系列权益
	totalpo = get_Tsymbol_by_symbol(symbol, postionpd)
	newtotalpo = cal_equity(symbol, totalpo)
	write_position_csv(type='Lilun', symbol=symbol, endtime=equity_day, df1=newtotalpo)
	day_equity = equity_resharp(newtotalpo)
	lastday_equity=day_equity['equity'][-1]
	lastday_equity_ZL=day_equity['equity_ZL'][-1]
	cal_day=day_equity.index[-1]
	lilun_total.append(lastday_equity)
	lilun_total_ZL.append(lastday_equity_ZL)
	print cal_day,acname,lastday_equity,lastday_equity_ZL
	lilun_result.append([cal_day,acname,lastday_equity,lastday_equity_ZL])


def cal_ac_day_equity_real(account,symbolid,symbol):
	postionpd, symbol = account_get_origin_position_list(account, symbolid,symbol)
	totalpo = get_Tsymbol_by_symbol(symbol, postionpd)
	newtotalpo = cal_equity(symbol, totalpo)
	write_position_csv(type='Account', symbol=symbol, endtime=equity_day, df1=newtotalpo)
	day_equity = equity_resharp(newtotalpo)
	lastday_equity=day_equity['equity'][-1]
	lastday_equity_ZL=day_equity['equity_ZL'][-1]
	cal_day=day_equity.index[-1]
	real_total.append(lastday_equity)
	real_total_ZL.append(lastday_equity_ZL)
	print cal_day,symbol,lastday_equity,lastday_equity_ZL
	real_account_result.append([cal_day,symbol,lastday_equity,lastday_equity_ZL])


def cal_ac_day_equity_huibao(account, symbolid, symbol):
	#step 1
	postionpd = get_delta_info(symbol,symbolid)

	newtotalpo = cal_equity_huibao(symbol, postionpd)
	write_position_csv(type='huibao', symbol=symbol, endtime=equity_day, df1=newtotalpo)
	day_equity = equity_resharp_huibao(newtotalpo)
	lastday_equity = day_equity['equity'][-1]
	cal_day = day_equity.index[-1]
	real_total.append(lastday_equity)
	print cal_day, symbol,symbolid, lastday_equity
	real_huibao_result.append([cal_day, symbol,symbolid, lastday_equity])


def main_get_lilun(step_acname,replacestr,totalratio):
	sql="select * from (select distinct f_ac from p_follow where ac='%s') a order by replace(f_ac,'%s','')" % (step_acname,replacestr)
	myres=ms.dict_sql(sql)
	for myitem in myres:
		#print myitem
		cal_ac_day_equity(step_acname,myitem['f_ac'],totalratio)

	print '####lilun_total',sum(lilun_total)
	totalresult_df1=pd.DataFrame(lilun_result)




def main_get_account_position(account,step_acname,replacestr):
	sql="select replace(f_ac,'%s','') as symbol ,Stock from p_follow where ac='%s' order by replace(f_ac,'%s','')" % (replacestr,step_acname,replacestr)
	myres2=ms.dict_sql(sql)
	for myitem in myres2:
		#print 'begin:',myitem['Stock'],myitem['symbol']
		cal_ac_day_equity_real(account,myitem['Stock'],myitem['symbol'])
	print '#####real_total',sum(real_total)
	print '#####real_total_ZL',sum(real_total_ZL)
	totalresult_df2=pd.DataFrame(real_account_result)

def main_get_huibao_position(account,step_acname,replacestr):
	sql="select replace(f_ac,'%s','') as symbol ,Stock from p_follow where ac='%s' order by replace(f_ac,'%s','')" % (replacestr,step_acname,replacestr)
	myres2=ms.dict_sql(sql)
	for myitem in myres2:
		#print 'begin:',myitem['Stock'],myitem['symbol']
		cal_ac_day_equity_huibao(account,myitem['Stock'],myitem['symbol'])
	print '#####real_total',sum(real_total)
	totalresult_df3=pd.DataFrame(real_huibao_result)



# cal_ac_day_equity('StepMultiI300w_up','srStepMultiI_up',2.2)
# cal_ac_day_equity_real(account,3,'sr')
# cal_ac_day_equity_huibao(account,1,'ru')

# 计算理论当天权益
main_get_lilun(step_acname,replacestr,totalratio)
#
# 计算期货账户仓位 当天权益
main_get_account_position(account,step_acname,replacestr)
#
#计算成交回报 当天权益
main_get_huibao_position(account,step_acname,replacestr)


# 写整个EXCEL

# totaldf=pd.concat([totalresult_df1,totalresult_df2,totalresult_df3],axis=1)
# write_position_csv('result','',endtime='2017-11-12',df1=1)
# print 1