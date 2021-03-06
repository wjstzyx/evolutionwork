#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import pandas as pd
import  datetime
import os
from pandas.tseries import offsets
import numpy as np
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
#ms = MSSQL(host="27.115.14.62:3888",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

global begintime
begintime='2015-04-20'

def input_to_database(root,acname):
	filelist=os.listdir(root)
	sql="truncate table st_report_test"
	ms.insert_sql(sql)
	for item in filelist:
		filename=item
		print filename
		df1=pd.read_csv(root+"\\"+filename)
		df1=df1[['Ticker','Date/Time','ps']]
		df1=df1.as_matrix()
		totalsql=""
		i=0
		for aaa in df1:
			i=i+1
			st=filename+"__"+aaa[0]
			sql="insert into st_report_test(st,p,stockdate) values('%s',%s,'%s')" % (st,aaa[2],aaa[1])
			totalsql=totalsql+';'+sql
			if i>5000:
				ms.insert_sql(totalsql)
				totalsql = ""
				i=0

		totalsql=totalsql.strip(';')
		ms.insert_sql(totalsql)
		totalsql=""

# 获取原始的仓位
def del_get_position(acname,symbol):
	sql="select p.AC,p.P_size*a.ratio/100.0*s.P as p,s.ST as st,s.stockdate from P_BASIC p inner join AC_RATIO a on p.AC=a.AC and p.AC='%s' inner join st_report_test s on p.ST=s.ST order by stockdate asc,s.id asc" % (acname)
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



def get_position(acname,symbol,stepname):
	sql="select k_a.F_ac as AC,s.P*k_a.ratio as p,s.ST as st,s.stockdate from ( select substring(st,CHARINDEX('__',st)+2,10) as symbol,* from st_report_test) s inner join (select F_ac,upper(a.Symbol) as symbol,aa.ratio/100.0 as ratio from p_follow p inner join symbol_id a on p.stock=a.S_ID and len(a.Symbol)<3 inner join AC_RATIO aa on p.F_ac=aa.AC where p.ac='%s' and p.F_ac='%s' ) k_a on s.symbol=k_a.symbol order by s.stockdate " % (stepname,acname)
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



# 作用于品种，添加每天收盘的价格
def generate_new_position(posotion_pd,symbol):
	fisrttime=position.iloc[[0]]['stockdate'][0]
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
	day_equity=pd.groupby(newtotalpo,'day').sum()
	return day_equity[['profit','comm','equity']]


#仓位入数据库 quanyi_log_symbol_V3
def write_to_database_position(df1,symbol,acname):
	df1=df1.fillna(0)
	nowday=datetime.datetime.now().strftime("%Y-%m-%d")
	sql="delete from quanyi_log_groupby_v3 where ac='%s' and symbol='%s' and stockdate>='%s'" % (acname,symbol,nowday)
	ms.insert_sql(sql)
	sql="select max(stockdate) as stockdate from quanyi_log_groupby_v3 where ac='%s' and symbol='%s'" % (acname,symbol)
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
		sql="insert into [Future].[dbo].[quanyi_log_groupby_v3](ac,symbol,type,closeprice,stockdate,totalposition) values('%s','%s','%s','%s','%s','%s')" % (acname,symbol,0,aaa[1],aaa[0],aaa[2])
		totalsql=totalsql+';'+sql
	ms.insert_sql(totalsql)
	totalsql=""


# drop replicate st_report_test
def drop_replicate_st_report_test():
	sql="select distinct st from st_report_test order by st"
	res=ms.dict_sql(sql)
	for item in res:
		st=item['st']
		sql="select * from st_report_test where st='%s' order by stockdate" % (st)
		res1=ms.dict_sql(sql)
		lastp=res1[0]['P']
		dellist=[]
		for item1 in res1[1:]:
			myid=item1['id']
			if item1['P']==lastp:
				dellist.append(str(myid))
			lastp=item1['P']
		adelist=','.join(dellist)
		print st
		if adelist<>'':
			sql='delete from st_report_test where id in (%s)' % (adelist)
			ms.insert_sql(sql)
















#权益入数据库 daily_equity_V3 记录delta 权益

#这是夜盘的权益计算
#看看 日盘 或者 日夜连做的权益是否一样计算
root=r'C:\Users\YuYang\Documents\Tencent Files\794513386\FileRecv\jieti1_zhuli_zhishu'
acname='StepMultiI300w_up'
# drop_replicate_st_report_test()
# input_to_database(root,acname)

#sql="truncate table quanyi_log_groupby_v3"
#ms.insert_sql(sql)
sql="select p.F_ac,a.Symbol from p_follow p inner join symbol_id a on p.stock=a.S_ID and LEN(a.symbol)<3 and p.AC='%s' ORDER BY f_ac" % (acname)
forlist=ms.dict_sql(sql)
i=0
for item in forlist:
	i=i+1
	print i, item
	position = get_position(acname=item['F_ac'],symbol=item['Symbol'],stepname=acname)
	newposition = generate_new_position(position,symbol=item['Symbol'])
	write_to_database_position(df1=newposition,symbol=item['Symbol'],acname=item['F_ac'])






