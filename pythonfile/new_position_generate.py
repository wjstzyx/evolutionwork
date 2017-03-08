#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import pandas as pd
import datetime
from pandas.tseries import offsets
import numpy as np
import multiprocessing
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")




# 获取原始的仓位
def get_position(acname,symbol):
	sql="select p.AC,p.P_size*a.ratio/100.0*s.P as p,s.ST as st,s.stockdate from P_BASIC p inner join AC_RATIO a on p.AC=a.AC and p.AC='%s' inner join st_report s on p.ST=s.ST order by stockdate asc,s.id asc" % (acname)
	res=ms.dict_sql(sql)
	deltepositionlist={}
	laststlistposition={}
	if len(res)>0:
		for item in res:
			if not deltepositionlist.has_key(item['stockdate']):
				deltepositionlist[item['stockdate']]=0
			if not laststlistposition.has_key(item['st']):
				laststlistposition[item['st']]=0
			deltepositionlist[item['stockdate']] = deltepositionlist[item['stockdate']] + (item['p'] - laststlistposition[item['st']])
			laststlistposition[item['st']] = item['p']
		newlist = [(k, deltepositionlist[k]) for k in sorted(deltepositionlist.keys())]
		# print 3,datetime.datetime.now()
		positionlist = []
		lastp = 0
		for item in newlist:
			temptotal = item[1] + lastp
			lastp = temptotal
			positionlist.append([item[0], round(item[1],6), round(temptotal,6)])
			#print [item[0], round(item[1],6), round(temptotal,6)]
		posotion_pd=pd.DataFrame(positionlist,columns=['stockdate','deltaposition','totalposition'])
		return posotion_pd
	else:
		print 'no position'
		return  []


# 从c++处获取信号，并且存入表，再从表中取出来
def get_position_cplus(acname,symbol):
	sql="select p.AC,p.P_size*a.ratio/100.0*s.P as p,s.ST as st,s.stockdate from P_BASIC_cplus p inner join AC_RATIO a on p.AC=a.AC and p.AC='%s' inner join real_st_report s on p.ST=s.ST order by stockdate asc,s.id asc" % (acname)
	res=ms.dict_sql(sql)
	deltepositionlist={}
	laststlistposition={}
	if len(res)>0:
		for item in res:
			if not deltepositionlist.has_key(item['stockdate']):
				deltepositionlist[item['stockdate']]=0
			if not laststlistposition.has_key(item['st']):
				laststlistposition[item['st']]=0
			deltepositionlist[item['stockdate']] = deltepositionlist[item['stockdate']] + (item['p'] - laststlistposition[item['st']])
			laststlistposition[item['st']] = item['p']
		newlist = [(k, deltepositionlist[k]) for k in sorted(deltepositionlist.keys())]
		# print 3,datetime.datetime.now()
		positionlist = []
		lastp = 0
		for item in newlist:
			temptotal = item[1] + lastp
			lastp = temptotal
			positionlist.append([item[0], round(item[1],6), round(temptotal,6)])
			print [item[0], round(item[1],6), round(temptotal,6)]
		posotion_pd=pd.DataFrame(positionlist,columns=['stockdate','deltaposition','totalposition'])
		return posotion_pd
	else:
		print 'no position'
		return  []


# 作用于品种，添加每天收盘的价格
def generate_new_position(posotion_pd,symbol):
	fisrttime=posotion_pd.iloc[[0]]['stockdate'][0]
	#添加 每天的结束时间
	sql="select max(StockDate) as stockdate from TSymbol_allfuture where Symbol='%s' and  T<='16:00' and stockdate >='%s' group by D order by D" % (symbol,fisrttime)
	daylist=ms.dict_sql(sql)
	daylist_pd=pd.DataFrame(daylist)
	posotion_pd=posotion_pd.append(daylist_pd,ignore_index=True)
	posotion_pd['myindex']=posotion_pd.index
	posotion_pd=posotion_pd.sort_values(['stockdate','myindex'],ascending=['True','True'])
	posotion_pd=posotion_pd.fillna(method='ffill')
	sql="select C,stockdate from TSymbol_allfuture where symbol='%s' and stockdate>='%s' order by stockdate" % (symbol,fisrttime)
	quotes=ms.dict_sql(sql)
	quotes_pd=pd.DataFrame(quotes)
	newposition =pd.merge(quotes_pd,posotion_pd,'outer',left_on='stockdate',right_on='stockdate')
	newposition = newposition.sort_values(['stockdate','myindex'])
	newposition['C']=newposition['C'].fillna(method='ffill')
	newposition =newposition[pd.notnull(newposition['totalposition'])]
	return newposition[['stockdate','C','totalposition']]

# 计算权益
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
	totalpo['profit']=(totalpo['totalposition']).shift()*(totalpo['C']-totalpo['C'].shift())*pointvalue
	#totalpo['profit_ZL']=(totalpo['totalposition'].round()).shift()*(totalpo['CZL']-totalpo['CZL'].shift())*pointvalue
	totalpo['comm']=abs((totalpo['totalposition'])-(totalpo['totalposition'].shift()))*commvalue
	totalpo['equity']=totalpo['profit']-totalpo['comm']
	#totalpo['equity_ZL']=totalpo['profit_ZL']-totalpo['comm']
	return  totalpo

# 偏移到 从21点开始计算新的一天收益
def equity_resharp(newtotalpo):
	deltatime=offsets.DateOffset(hours=6)
	newtotalpo['stockdate']=newtotalpo['stockdate']+deltatime
	newtotalpo['day']=newtotalpo['stockdate'].apply(lambda x: x.strftime('%Y%m%d'))
	mydailposition=newtotalpo[newtotalpo['stockdate'].apply(lambda x: x.strftime('%H%M%S'))=='205900'][['stockdate','totalposition']]
	mydailposition['day']=mydailposition['stockdate'].apply(lambda x: x.strftime('%Y%m%d'))
	mydailposition['lastdayposition']=mydailposition['totalposition']
	mydailposition=mydailposition[['day','lastdayposition']]
	newtotalpo['deltaposition']=abs(newtotalpo['totalposition']-newtotalpo['totalposition'].shift())
	day_equity=pd.groupby(newtotalpo,'day').sum()
	day_equity['day']=day_equity.index
	day_equity=pd.merge(day_equity,mydailposition,how='left',on='day')
	day_equity['lastdayposition']=day_equity['lastdayposition'].fillna(method='ffill')


	return day_equity[['profit','comm','equity','deltaposition','lastdayposition','day']]


#仓位入数据库 quanyi_log_symbol_V3
def write_to_database_position(df1,symbol,acname):
	df1=df1.fillna(0)
	nowday=datetime.datetime.now().strftime("%Y-%m-%d")
	nowday='2017-02-20'
	sql="delete from quanyi_log_groupby_v2 where ac='%s' and symbol='%s' and stockdate>='%s'" % (acname,symbol,nowday)
	ms.insert_sql(sql)
	sql="select max(stockdate) as stockdate from quanyi_log_groupby_v2 where ac='%s' and symbol='%s'" % (acname,symbol)
	res=ms.dict_sql(sql)[0]['stockdate']
	if res is None:
		pass
		#insert all
	else:
		firsttime=res
		df1=df1[df1['stockdate']>firsttime]
	df2=df1.as_matrix()
	totalsql=""
	for aaa in df2:
		sql="insert into [Future].[dbo].[quanyi_log_groupby_v2](ac,symbol,type,closeprice,stockdate,totalposition) values('%s','%s','%s','%s','%s','%s')" % (acname,symbol,0,aaa[1],aaa[0],aaa[2])
		totalsql=totalsql+';'+sql
	ms.insert_sql(totalsql)
	totalsql=""

	#get position from quanyilog_v2
	sql="select symbol from symbol_id where s_id in (select s_id from symbol_id where symbol='%s')  and LEN(symbol)<3" % (symbol)
	quanyi_symbol_v2=ms.dict_sql(sql)[0]['symbol']
	sql = "select q.stockdate,t.C,q.totalposition from quanyi_log_groupby_v2 q   inner join TSymbol_allfuture t   on q.stockdate=t.StockDate and t.Symbol='%s' where q.ac='%s' and q.symbol='%s'   order by q.stockdate" % (quanyi_symbol_v2, acname, symbol)
	print sql
	res = ms.dict_sql(sql)
	mydf=pd.DataFrame(res)
	mydf=mydf[['stockdate','C','totalposition']]
	return mydf

def write_to_database_equity(df1,symbol,acname):
	df1=df1.fillna(0)
	df1=df1[['day','total_equity','deltaposition','lastdayposition']]
	nowday=datetime.datetime.now().strftime("%Y-%m-%d")
	sql="delete from dailyquanyi_V2 where ac='%s' and symbol='%s'" % (acname,symbol)
	ms.insert_sql(sql)
	df2 = df1.as_matrix()
	totalsql=""
	for aaa in df2:
		D=aaa[0]
		D=int(aaa[0])-20000000
		sql="insert into [Future].[dbo].[dailyquanyi_V2](ac,symbol,D,quanyi,times,totalnum,position) values('%s','%s','%s','%s','%s','%s','%s')" % (acname,symbol,D,aaa[1],round(aaa[2],1),10,round(aaa[3]))
		totalsql=totalsql+';'+sql
	ms.insert_sql(totalsql)
	totalsql=""







#权益入数据库 daily_equity_V3 记录delta 权益

#这是夜盘的权益计算
#看看 日盘 或者 日夜连做的权益是否一样计算


def sub_main(acname,day_night_symbol,quanyi_symbol):
	sql="select symbol from symbol_id where s_id in (select s_id from symbol_id where symbol='%s')  and LEN(symbol)<3" % (day_night_symbol)
	quotes_symbol=ms.dict_sql(sql)[0]['symbol']
	sql="select symbol from symbol_id where s_id in (select s_id from symbol_id where symbol='%s')  and LEN(symbol)<3" % (quanyi_symbol)
	quanyi_symbol_v2=ms.dict_sql(sql)[0]['symbol']
	position = get_position(acname=acname,symbol=quotes_symbol)
	newposition = generate_new_position(position,symbol=quanyi_symbol_v2)
	#newposition.to_csv(r'C:\Users\YuYang\Desktop\dog\aaa.csv')
	newposition=write_to_database_position(newposition,acname=acname,symbol=quanyi_symbol)
	equity_split=cal_equity(quanyi_symbol_v2,newposition)
	equity_day=equity_resharp(equity_split)
	equity_day['total_equity']=equity_day['equity'].cumsum()/10.0
	equity_day['myday']=equity_day['day']
	write_to_database_equity(equity_day,acname=acname,symbol=quanyi_symbol)



sub_main('RB3rangel','RB','RB')


# if __name__=="__main__":
#     threads_N=7
#     multiprocessing.freeze_support()
#
#     pool = multiprocessing.Pool(processes = threads_N)
#
#     sql = "SELECT id, [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where iscaculate=1 and isyepan in (0,1,12)  AND quanyisymbol not in ('IF','IC','IH') order by id desc "
#     res1 = ms.dict_sql(sql)
#
#     for item in res1:
#         acname=item['acname']
#         day_night_symbol=item['positionsymbol']
#         quanyi_symbol=item['quanyisymbol']
#         print item['id'],acname,day_night_symbol,quanyi_symbol
#         # add process to pool
#         if threads_N > 1:
#             print multiprocessing.current_process().name
#             pool.apply_async(sub_main, (acname,day_night_symbol,quanyi_symbol) )
#         else:
#             sub_main(acname,day_night_symbol,quanyi_symbol)
#
#     print "Process Pool Closed, Waiting for sub Process Finishing..."
#     pool.close()
#     pool.join()
#
#     print 'Finished'






