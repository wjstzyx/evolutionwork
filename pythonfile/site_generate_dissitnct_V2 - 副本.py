#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime
import time
import os
import numpy as np
import pandas as pd
#from openpyxl.writer.excel import ExcelWriter
from pandas.tseries import offsets
from pandas import  Timestamp
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
#ms = MSSQL(host="27.115.14.62:3888",user="future",pwd="K@ra0Key",db="future")
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


accountlist={"257188832":['StepMultiI300w_up',2.2],"666061010":['StepMultiI300w_up',2.2],"1636737":['StepMultigaosheng1',1]}

# step_acname='StepMultiI300w_up'
# account='666061010'
# totalratio=1
# backday=40
# equity_day='2017-02-15'

account='1636737'
step_acname=accountlist[account][0]

nowday=datetime.datetime.now().strftime("%Y-%m-%d")
equity_day=nowday
lastbar=equity_day+" 14:59:00"
sql="select top 30 * from TSymbol_ZL where stockdate='%s'" % (lastbar)
res=ms.dict_sql(sql)
if len(res)==30:
	pass
else:
	print 'Please input data first!!!!'
	exit()

totalratio=accountlist[account][1]

backday=40
cache_num=35
#mytype= 'lilun' 'position' 'huibao'





lilun_result=[]
real_account_result=[]
real_huibao_result=[]




lilun_total=[]
real_total=[]
lilun_total_ZL=[]
real_total_ZL=[]
endtime=equity_day+" 16:00:00"
sql="select  distinct top (%s) convert(nvarchar(10),stockdate,120) as day from TSymbol where StockDate<='%s' order by day desc" % (backday,equity_day)
beginday=ms.find_sql(sql)
begintime=beginday[-1][0]
filepath = os.path.split(os.path.realpath(__file__))[0]
totalroot = os.path.dirname(filepath)
if not totalroot+"\\all_future_position\\results":
	os.makedirs(totalroot+"\\all_future_position\\results")
totalresults=pd.DataFrame()

excel_file=totalroot+"\\all_future_position\\results\\"+str(equity_day)+".xls"


def write_to_database_symbol_equity_lilun(account,acname,df1,cache_num=3):
	# replace Nan with 0
	df1=df1.iloc[-cache_num:]
	print df1
	df1=df1.fillna(0)
	alist=df1.as_matrix()
	sql="select date,round([lilun_zhishu],1)   ,round([lilun_zhuli],1)  from [LogRecord].[dbo].[account_lilun_distinct_acname] where [account]='%s' and [acname]='%s' order by date" % (account,acname)
	res=ms.find_sql(sql)
	datalist=[item[0] for item in res]

	for item in alist:
		value=(item[5],round(item[2],1),round(item[4],1))
		if value in res:
			pass
		else:
			if item[5] in datalist:
				sql="update [LogRecord].[dbo].[account_lilun_distinct_acname] set lilun_zhishu=%s ,[lilun_zhuli]=%s ,[inserttime]=getdate() where account='%s' and acname='%s' and date='%s'" % (value[1],value[2],account,acname,value[0])
			else:
				sql="insert into [LogRecord].[dbo].[account_lilun_distinct_acname]([account],[acname],[date],[lilun_zhishu],[lilun_zhuli],[inserttime]) values('%s','%s','%s',%s,%s,getdate())" % (account,acname,value[0],value[1],value[2])
			print sql
			ms.insert_sql(sql)





def write_to_database_symbol_equity_account(account,acname,df1,cache_num=3):
	# replace Nan with 0
	df1 = df1.iloc[-cache_num:]
	df1=df1.fillna(0)
	alist=df1.as_matrix()
	sql="select date,round(position_zhishu,1)   ,round([position_zhuli],1)  from [LogRecord].[dbo].[account_lilun_distinct_acname] where [account]='%s' and [acname]='%s' order by date" % (account,acname)
	res=ms.find_sql(sql)
	datalist=[item[0] for item in res]

	for item in alist:
		value=(item[5],round(item[2],1),round(item[4],1))
		if value in res:
			pass
		else:
			if item[5] in datalist:
				sql="update [LogRecord].[dbo].[account_lilun_distinct_acname] set [position_zhishu]=%s ,position_zhuli=%s ,[inserttime]=getdate() where account='%s' and acname='%s' and date='%s'" % (value[1],value[2],account,acname,value[0])
			else:
				sql="insert into [LogRecord].[dbo].[account_lilun_distinct_acname]([account],[acname],[date],position_zhishu,position_zhuli,[inserttime]) values('%s','%s','%s',%s,%s,getdate())" % (account,acname,value[0],value[1],value[2])
			print sql
			ms.insert_sql(sql)



def write_to_database_symbol_equity_huibao(account,acname,df1,cache_num=3):
	# replace Nan with 0
	df1 = df1.iloc[-cache_num:]

	print df1
	df1=df1.fillna(0)
	alist=df1.as_matrix()
	sql="select date,round([account_zhuli],1)  from [LogRecord].[dbo].[account_lilun_distinct_acname] where [account]='%s' and [acname]='%s' order by date" % (account,acname)
	res=ms.find_sql(sql)
	datalist=[item[0] for item in res]

	for item in alist:
		value=(item[3],round(item[2],1))
		if value in res:
			pass
		else:
			if item[3] in datalist:
				sql="update [LogRecord].[dbo].[account_lilun_distinct_acname] set [account_zhuli]=%s ,[inserttime]=getdate() where account='%s' and acname='%s' and date='%s'" % (value[1],account,acname,value[0])
			else:
				sql="insert into [LogRecord].[dbo].[account_lilun_distinct_acname]([account],[acname],[date],[account_zhuli],[inserttime]) values('%s','%s','%s',%s,getdate())" % (account,acname,value[0],value[1])
			print sql
			ms.insert_sql(sql)









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
	sql="select q.ClosePrice,q.stockdate,round(q.totalposition*mr.ratio*%s,0) as totalposition ,q.symbol,sid.S_ID from p_follow p inner join real_quanyi_log_groupby_v2 q on p.F_ac=q.AC and p.AC='%s' inner join LogRecord.dbo.test_margin mr on q.symbol=mr.symbol inner join symbol_id sid on q.symbol=sid.Symbol where q.AC='%s' and stockdate>='%s' and stockdate<='%s' order by stockdate" % (ratio,p_followac,acname,begintime,endtime)

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


def shift_time(stockdate,deltahours=4):
	if stockdate.strftime("%H%M")>='21:00':
		newstockdate=stockdate+datetime.timedelta(hours=deltahours-24)
		return newstockdate
	else:
		return stockdate



def get_delta_info(symbol,symbolid,account):
	#ms1 = MSSQL(host="192.168.0.8", user="future", pwd="K@ra0Key", db="HF_Future")
	#获取成交回报
	if symbol.lower()=='yy':
		symbol1='y'
		sql = "  select 'yy' as symbol,Direction,[Volume],  Price,convert(datetime,substring(TradeDate,0,5)+'-'+substring(TradeDate,5,2)+'-'+substring(TradeDate,7,2)+' '+[TradeTime],120) as stockdate from [Future].[dbo].[test_tradelog] where Future.dbo.m_getstr([InstrumentID])='%s' and convert(datetime,substring(TradeDate,0,5)+'-'+substring(TradeDate,5,2)+'-'+substring(TradeDate,7,2)+' '+[TradeTime],120)>='%s' order by stockdate " % (symbol, begintime)
	else:
		symbol1=symbol
		sql = "  select Future.dbo.m_getstr([InstrumentID]) as symbol,Direction,[Volume],  Price,convert(datetime,substring(TradeDate,0,5)+'-'+substring(TradeDate,5,2)+'-'+substring(TradeDate,7,2)+' '+[TradeTime],120) as stockdate from [Future].[dbo].[test_tradelog] where Future.dbo.m_getstr([InstrumentID])='%s' and convert(datetime,substring(TradeDate,0,5)+'-'+substring(TradeDate,5,2)+'-'+substring(TradeDate,7,2)+' '+[TradeTime],120)>='%s' order by stockdate " % (symbol, begintime)
	res=ms.dict_sql(sql)

	#如果有记录，则加上初始仓位，算出总仓位
	if res:
		afirsttime=res[0]['stockdate']
	else:
		afirsttime =datetime.datetime.strptime(begintime,'%Y-%m-%d')

	sql = "SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account, afirsttime, symbolid)
	tempres = ms.dict_sql(sql)
	if tempres:
		alastposition = tempres[0]['totalposition']
		atime_position = tempres[0]['stockdate']
	else:
		print symbol, '不存在期货账户仓位信息'
		exit()
	sql = "SELECT top 1 C  FROM [Future].[dbo].[TSymbol_ZL] where symbol='%s' and stockdate<='%s' order by stockdate desc" % (symbol, atime_position)
	tempres = ms.dict_sql(sql)
	if tempres:
		atime_price = ms.dict_sql(sql)[0]['C']
	else:
		atime_price = 0
	addline = {'stockdate': atime_position, 'Direction': 2, 'Volume': 0, 'symbol': symbol, 'Price': atime_price}
	res.append(addline)

	deltapd=pd.DataFrame(res)
	#偏移夜盘的时间至加上4小时-24
	deltapd['stockdate']=deltapd['stockdate'].apply(lambda x: shift_time(x))

	deltapd['deltaposition']=deltapd['Direction']*deltapd['Volume']
	deltapd['myindex']=deltapd.index
	deltapd=deltapd.sort_values(['stockdate','myindex'])
	deltapd['totalposition'] = deltapd['deltaposition'].cumsum()+alastposition

	# add everyday edntime
	sql="select stockdate,C as Price from [TSymbol_ZL] where symbol='%s' and stockdate in ( select MAX(StockDate) as stockdate from [TSymbol_ZL] where symbol='%s' and StockDate>='%s' and StockDate<='%s' and t<='15:30'group by D )" % (symbol,symbol,begintime,endtime)
	insertstockdate=ms.dict_sql(sql)
	#计算出对应的仓位
	lastonetime=insertstockdate[-1]['stockdate']
	lasttwotime=insertstockdate[-2]['stockdate']
	sql = "SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account, lastonetime, symbolid)
	tempres = ms.dict_sql(sql)
	if tempres:
		alastposition = tempres[0]['totalposition']
		atime_position = tempres[0]['stockdate']
	else:
		print symbol, '不存在期货账户仓位信息'
		exit()
	insertstockdate[-1]['totalposition']=alastposition
	sql = "SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account, lasttwotime, symbolid)
	tempres = ms.dict_sql(sql)
	if tempres:
		alastposition = tempres[0]['totalposition']
		atime_position = tempres[0]['stockdate']
	else:
		print symbol, '不存在期货账户仓位信息'
		exit()
	insertstockdate[-2]['totalposition']=alastposition

	insertstockdate_pd=pd.DataFrame(insertstockdate)
	deltapd=deltapd.append(insertstockdate_pd,ignore_index=True)


	deltapd=deltapd.sort_values(['stockdate','myindex'])
	deltapd = deltapd.fillna(method='ffill')
	deltapd['C']=deltapd['Price']
	deltapd=deltapd[deltapd['stockdate']<=endtime]
	#如果现在存在totalposition NAN 则需要手动补全
	nanvalue=deltapd[deltapd['totalposition'].isnull()]
	if len(nanvalue)==0:
		return deltapd[['C', 'stockdate', 'symbol', 'totalposition']]

	atime=nanvalue['stockdate'].values[-1]
	atime=Timestamp(atime)
	sql = "SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account, atime, symbolid)
	tempres = ms.dict_sql(sql)
	if tempres:
		alastposition = tempres[0]['totalposition']
		atime_position = tempres[0]['stockdate']
	else:
		print symbol, '不存在期货账户仓位信息1'
		exit()
	sql = "SELECT top 1 C  FROM [Future].[dbo].[TSymbol_ZL] where symbol='%s' and stockdate<='%s' order by stockdate desc" % (symbol, atime_position)
	tempres = ms.dict_sql(sql)
	if tempres:
		atime_price = ms.dict_sql(sql)[0]['C']
	else:
		atime_price = 0
	aa=pd.DataFrame([{'stockdate':atime_position,'totalposition':alastposition,'C':atime_price,'symbol':symbol}])
	deltapd = deltapd.append(aa,ignore_index=True)
	deltapd=deltapd.sort_values(['stockdate','myindex'])
	deltapd = deltapd.fillna(method='ffill')

	return deltapd[['C','stockdate','symbol','totalposition']]





def get_delta_info_from_database(account,symbol,symbolid):
	ms1 = MSSQL(host="192.168.0.8", user="future", pwd="K@ra0Key", db="HF_Future")
	#获取成交回报
	if symbol.lower()=='yy':
		symbol1='y'
		sql="select 'yy' as symbol,case when Direction='buy' then 1 else -1 end as Direction,[Volume],  Price,convert(datetime,convert(nvarchar(10),[Databasetime],20) +' '+[TradeTime],120) as stockdate from [HF_Future].[dbo].[tradelog] where [HF_Future].dbo.m_getstr([InstrumentID]) = '%s' and [InvestorID]='%s' and convert(datetime,convert(nvarchar(10),[Databasetime],20) +' '+[TradeTime],120)>='%s' order by stockdate " % (symbol1,account,begintime)
	else:
		symbol1=symbol
		sql="select [HF_Future].dbo.m_getstr([InstrumentID]) as symbol,case when Direction='buy' then 1 else -1 end as Direction,[Volume],  Price,convert(datetime,convert(nvarchar(10),[Databasetime],20) +' '+[TradeTime],120) as stockdate from [HF_Future].[dbo].[tradelog] where [HF_Future].dbo.m_getstr([InstrumentID]) = '%s' and [InvestorID]='%s' and convert(datetime,convert(nvarchar(10),[Databasetime],20) +' '+[TradeTime],120)>='%s' order by stockdate " % (symbol1,account,begintime)
	res=ms1.dict_sql(sql)

	#如果有记录，则加上初始仓位，算出总仓位
	if res:
		afirsttime=res[0]['stockdate']
	else:
		afirsttime =datetime.datetime.strptime(begintime,'%Y-%m-%d')

	sql = "SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account, afirsttime, symbolid)
	tempres = ms.dict_sql(sql)
	if tempres:
		alastposition = tempres[0]['totalposition']
		atime_position = tempres[0]['stockdate']
	else:
		print symbol, '不存在期货账户仓位信息'
		exit()
	sql = "SELECT top 1 C  FROM [Future].[dbo].[TSymbol_ZL] where symbol='%s' and stockdate<='%s' order by stockdate desc" % (symbol, atime_position)
	tempres = ms.dict_sql(sql)
	if tempres:
		atime_price = ms.dict_sql(sql)[0]['C']
	else:
		atime_price = 0
	addline = {'stockdate': atime_position, 'Direction': 0, 'Volume': 0, 'symbol': symbol, 'Price': atime_price}
	res.append(addline)
	deltapd=pd.DataFrame(res)

	#偏移夜盘的时间至加上4小时-24
	deltapd['stockdate']=deltapd['stockdate'].apply(lambda x: shift_time(x))
	deltapd['deltaposition']=deltapd['Direction']*deltapd['Volume']
	deltapd['myindex']=deltapd.index
	deltapd=deltapd.sort_values(['stockdate','myindex'])
	deltapd['totalposition'] = deltapd['deltaposition'].cumsum()+alastposition

	# add everyday edntime
	sql="select stockdate,C as Price from [TSymbol_ZL] where symbol='%s' and stockdate in ( select MAX(StockDate) as stockdate from [TSymbol_ZL] where symbol='%s' and StockDate>='%s' and StockDate<='%s' and t<='15:30'group by D )" % (symbol,symbol,begintime,endtime)
	insertstockdate=ms.dict_sql(sql)
	#计算出对应的仓位
	lastonetime=insertstockdate[-1]['stockdate']
	lasttwotime=insertstockdate[-2]['stockdate']
	sql = "SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account, lastonetime, symbolid)
	tempres = ms.dict_sql(sql)
	if tempres:
		alastposition = tempres[0]['totalposition']
		atime_position = tempres[0]['stockdate']
	else:
		print symbol, '不存在期货账户仓位信息'
		exit()
	insertstockdate[-1]['totalposition']=alastposition
	sql = "SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account, lasttwotime, symbolid)
	tempres = ms.dict_sql(sql)
	if tempres:
		alastposition = tempres[0]['totalposition']
		atime_position = tempres[0]['stockdate']
	else:
		print symbol, '不存在期货账户仓位信息'
		exit()
	insertstockdate[-2]['totalposition']=alastposition

	insertstockdate_pd=pd.DataFrame(insertstockdate)
	deltapd=deltapd.append(insertstockdate_pd,ignore_index=True)


	deltapd=deltapd.sort_values(['stockdate','myindex'])
	deltapd = deltapd.fillna(method='ffill')
	deltapd['C']=deltapd['Price']
	deltapd=deltapd[deltapd['stockdate']<=endtime]
	#如果现在存在totalposition NAN 则需要手动补全
	nanvalue=deltapd[deltapd['totalposition'].isnull()]
	if len(nanvalue)==0:
		return deltapd[['C', 'stockdate', 'symbol', 'totalposition']]

	atime=nanvalue['stockdate'].values[-1]
	atime=Timestamp(atime)
	sql = "SELECT top (1) 0 as ClosePrice,convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition,bb.Symbol as symbol,  stockID as S_ID FROM [LogRecord].[dbo].[account_position]aa inner join Future.dbo.symbol_id bb on aa.stockID=bb.S_ID and len(bb.symbol)<3  where userid='%s'   and inserttime<='%s' and stockid=%s order by [inserttime] desc " % (account, atime, symbolid)
	tempres = ms.dict_sql(sql)
	if tempres:
		alastposition = tempres[0]['totalposition']
		atime_position = tempres[0]['stockdate']
	else:
		print symbol, '不存在期货账户仓位信息1'
		exit()
	sql = "SELECT top 1 C  FROM [Future].[dbo].[TSymbol_ZL] where symbol='%s' and stockdate<='%s' order by stockdate desc" % (symbol, atime_position)
	tempres = ms.dict_sql(sql)
	if tempres:
		atime_price = ms.dict_sql(sql)[0]['C']
	else:
		atime_price = 0
	aa=pd.DataFrame([{'stockdate':atime_position,'totalposition':alastposition,'C':atime_price,'symbol':symbol}])
	deltapd = deltapd.append(aa,ignore_index=True)
	deltapd=deltapd.sort_values(['stockdate','myindex'])
	deltapd = deltapd.fillna(method='ffill')

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
	tempdf=day_equity
	tempdf['day']=day_equity.index
	write_position_csv(type='Lilun_dayli_equity', symbol=symbol, endtime=equity_day, df1=tempdf)
	write_to_database_symbol_equity_lilun(account, acname, tempdf,cache_num)
	lastday_equity=day_equity['equity'][-1]
	lastday_equity_ZL=day_equity['equity_ZL'][-1]
	cal_day=day_equity.index[-1]
	lilun_total.append(lastday_equity)
	lilun_total_ZL.append(lastday_equity_ZL)
	print cal_day,acname,lastday_equity,lastday_equity_ZL
	lilun_result.append([cal_day,acname,lastday_equity,lastday_equity_ZL])


def cal_ac_day_equity_real(account,symbolid,symbol,acanme):
	postionpd, symbol = account_get_origin_position_list(account, symbolid,symbol)
	totalpo = get_Tsymbol_by_symbol(symbol, postionpd)
	newtotalpo = cal_equity(symbol, totalpo)
	write_position_csv(type='Account', symbol=symbol, endtime=equity_day, df1=newtotalpo)
	day_equity = equity_resharp(newtotalpo)
	tempdf=day_equity
	tempdf['day']=day_equity.index
	write_position_csv(type='Account_dayli_equity', symbol=symbol, endtime=equity_day, df1=tempdf)
	write_to_database_symbol_equity_account(account, acanme, tempdf,cache_num)
	lastday_equity=day_equity['equity'][-1]
	lastday_equity_ZL=day_equity['equity_ZL'][-1]
	cal_day=day_equity.index[-1]
	real_total.append(lastday_equity)
	real_total_ZL.append(lastday_equity_ZL)
	print cal_day,symbol,lastday_equity,lastday_equity_ZL
	real_account_result.append([cal_day,symbol,lastday_equity,lastday_equity_ZL])


def cal_ac_day_equity_huibao(account, symbolid, symbol,acanme):
	#step 1
	postionpd = get_delta_info_from_database(account,symbol,symbolid)
	#postionpd = get_delta_info(symbol, symbolid,account)

	newtotalpo = cal_equity_huibao(symbol, postionpd)
	write_position_csv(type='huibao', symbol=symbol, endtime=equity_day, df1=newtotalpo)
	day_equity = equity_resharp_huibao(newtotalpo)
	tempdf=day_equity
	tempdf['day']=day_equity.index
	write_position_csv(type='huibao_dayli_equity', symbol=symbol, endtime=equity_day, df1=tempdf)
	write_to_database_symbol_equity_huibao(account, acanme, tempdf)
	lastday_equity = day_equity['equity'][-1]
	cal_day = day_equity.index[-1]
	real_total.append(lastday_equity)
	print cal_day, symbol,symbolid, lastday_equity
	real_huibao_result.append([cal_day, symbol,symbolid, lastday_equity])


def main_get_lilun(step_acname,totalratio):
	sql="select * from (select distinct f_ac from p_follow where ac='%s') a order by f_ac" % (step_acname)
	myres=ms.dict_sql(sql)
	for myitem in myres:
		#print myitem
		cal_ac_day_equity(step_acname,myitem['f_ac'],totalratio)

	print '####lilun_total',sum(lilun_total)
	totalresult_df1=pd.DataFrame(lilun_result)




def main_get_account_position(account,step_acname):
	sql = "select SUBSTRING(f_ac,0, CHARINDEX('StepMu',f_ac)) as symbol ,f_ac,Stock from p_follow where ac='%s' order by f_ac" % (step_acname)
	myres2=ms.dict_sql(sql)
	for myitem in myres2:
		#print 'begin:',myitem['Stock'],myitem['symbol']
		cal_ac_day_equity_real(account,myitem['Stock'],myitem['symbol'],myitem['f_ac'])
	print '#####real_total',sum(real_total)
	print '#####real_total_ZL',sum(real_total_ZL)
	totalresult_df2=pd.DataFrame(real_account_result)

def main_get_huibao_position(account,step_acname):
	sql = "select SUBSTRING(f_ac,0, CHARINDEX('StepMu',f_ac)) as symbol ,f_ac,Stock from p_follow where ac='%s' order by f_ac" % (step_acname)
	myres2=ms.dict_sql(sql)
	for myitem in myres2:
		#print 'begin:',myitem['Stock'],myitem['symbol']
		cal_ac_day_equity_huibao(account,myitem['Stock'],myitem['symbol'],myitem['f_ac'])
	print '#####real_total',sum(real_total)
	totalresult_df3=pd.DataFrame(real_huibao_result)



# cal_ac_day_equity('StepMultiI300w_up','srStepMultiI_up',2.2)
# cal_ac_day_equity_real(account,3,'sr')
# cal_ac_day_equity_huibao(account,7,'yy')
# cal_ac_day_equity_huibao(account,52,'zc')
# cal_ac_day_equity_huibao(account,8,'zn')
# cal_ac_day_equity_huibao(account,53,'bu')
#

#mytype= 'lilun' 'position' 'huibao'
mytype="lilun"
if mytype=='lilun':
	# 计算理论当天权益
	main_get_lilun(step_acname,totalratio)
if mytype=='position':	# #
	# # 计算期货账户仓位 当天权益
	main_get_account_position(account,step_acname)
if mytype=='huibao':
	#计算成交回报 当天权益
	main_get_huibao_position(account,step_acname)


# 写整个EXCEL

# totaldf=pd.concat([totalresult_df1,totalresult_df2,totalresult_df3],axis=1)
# write_position_csv('result','',endtime='2017-11-12',df1=1)
# print 1