#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from itertools import islice
import pandas as pd
import numpy as np
import datetime
import os
import csv
from dbconn import MSSQL
import pymssql
ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms03 = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")
ms07 = MSSQL(host="192.168.0.7",user="future",pwd="K@ra0Key",db="future")
# ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Openinterest', 'Turnover']
def input_all_date_to_tsymbol_test():
	dataroot=r'D:\KT\_ExportData_\60'
	filelist=os.listdir(dataroot)
	for i in filelist:
		if '98' in i:
			symbol=i.replace('98.csv','').upper()
			print symbol
			fh=open(dataroot+'\\'+i)
			csvcontent=csv.reader(fh)
			totalsql=""
			j=0
			for row in islice(csvcontent, 1, None):
				O = row[2]
				H = row[3]
				L = row[4]
				C = row[5]
				V = row[6]
				OPI = row[7]
				D = row[0]
				T = row[1]
				if len(T) < 6:
					T = '0' * (6 - len(T)) + T
				T = T[0:2] + ':' + T[2:4]
				D = D[0:4] + '/' + D[4:6] + '/' + D[6:8]
				StockDate = datetime.datetime.strptime(D + ' ' + T, '%Y/%m/%d %H:%M')
				sql = "insert into TSymbol_test ([Symbol]  ,[O]   ,[C]   ,[H]  ,[L]   ,[V]   ,[OPI]  ,[D]  ,[T]  ,[StockDate]  ,[refc] ) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',0);" % (symbol, O, C, H, L, V, OPI, D, T, StockDate)
				totalsql = totalsql + sql
				j = j + 1
				if j > 1000:
					print j,symbol
					ms.insert_sql(totalsql)
					totalsql = ""
					j = 0


			if len(totalsql) > 10:
				ms.insert_sql(totalsql)


#input_all_date_to_tsymbol_test()

def get_infer_quotes(symbol,begintime='2016-01-01',endtime='2017-01-01',type='day'):
	ms05_quotes = pymssql.connect(host='192.168.0.5', user='future', password="K@ra0Key", database="future")
	if type=='day':
		sql="SELECT *  FROM [Future].[dbo].[TSymbol_test] where symbol='%s'  and StockDate>='%s' and StockDate<='%s' and  T>='09:00' and T<='15:00'  order by stockdate" % (symbol,begintime,endtime)
	if type=='night':
		sql="SELECT *  FROM [Future].[dbo].[TSymbol_test] where symbol='%s'  and StockDate>='%s' and StockDate<='%s' and  (T>='21:00' or T<='05:00')  order by stockdate" % (symbol,begintime,endtime)
	if type=='all':
		sql="SELECT *  FROM [Future].[dbo].[TSymbol_test] where symbol='%s'  and StockDate>='%s' and StockDate<='%s' order by stockdate" % (symbol,begintime,endtime)

	df1=pd.read_sql(sql,ms05_quotes)
	return df1

def fix_data_by_Tsymbol_test(ms,fixtable,symbol,refer_df,begintime,endtime):
	sql="select min(stockdate) as stockdate from %s where symbol='%s' and stockdate>='2014-01-01'" % (fixtable,symbol)
	res=ms.dict_sql(sql)
	begintime_table=res[0]['stockdate']
	refer_df=refer_df[refer_df['StockDate']>=begintime_table]
	sql="select * from %s where symbol='%s' and StockDate>='%s' and StockDate<='%s' order by StockDate" % (fixtable,symbol,begintime,endtime)
	res=ms.dict_sql(sql)
	df2=pd.DataFrame(res)
	temp=pd.merge(refer_df, df2, how='left', on='StockDate',suffixes=('','_y'))
	columns=list(refer_df.columns)
	temp=temp[temp['O_y'].isnull()]
	temp=temp[columns]
	#print temp[:2]
	#print columns
	contentlist=temp.values.tolist()
	totalsql=""
	ii=0;
	for item in contentlist:
		#print item
		sql="insert into %s (Symbol,O,C,H,L,V,OPI,D,T,StockDate) values('%s',%s,%s,%s,%s,%s,%s,'%s','%s','%s');" % (fixtable,symbol,item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10])
		totalsql=totalsql+sql
		print sql
		ii=ii+1
		if ii>1000:
			ms.insert_sql(totalsql)
			totalsql=""
			ii=0
	if len(totalsql)>10:
		ms.insert_sql(totalsql)
		totalsql = ""
		ii=0






daylist=[[u'A',u'A'], [u'AG', u'AG'], [u'AL', u'AL'], [u'AU', u'AU'], [u'bu', u'bu'], [u'c', u'c'], [u'CF', u'CF'], [u'cs', u'cs'], [u'CU', u'CU'], [u'FG', u'FG'], [u'hc', u'hc'], [u'I', u'I'], [u'IC', u'IC'], [u'IF', u'IF'], [u'IH', u'IH'], [u'J', u'J'], [u'jd', u'jd']]
nightlist=[[u'AGN', u'AG'], [u'AUN', u'AU'], [u'CUN', u'CU'], [u'Inight', u'I'],  [u'Pnight', u'P'], [u'RBnight', u'RB']]
#nightlist=[[u'Pnight', u'P']]
#daylist=[[u'RB',u'RB']]
begintime='2017-01-01'
endtime='2020-01-01'
for item in nightlist:
	symbol_refer = item[1]
	symbol = item[0]
	type = 'night'
	df1 = get_infer_quotes(symbol_refer, begintime, endtime, type=type)
	for fixtable in ('TSymbol','TSymbol_quotes_backup'):
		fix_data_by_Tsymbol_test(ms05,fixtable,symbol,df1,begintime,endtime)

for item in daylist:
	symbol_refer = item[1]
	symbol = item[0]
	type = 'day'
	df1 = get_infer_quotes(symbol_refer, begintime, endtime, type=type)
	for fixtable in ('TSymbol','TSymbol_quotes_backup'):
		fix_data_by_Tsymbol_test(ms05,fixtable,symbol,df1,begintime,endtime)

for item in daylist:
	symbol_refer = item[1]
	symbol = item[0]
	type = 'all'
	df1 = get_infer_quotes(symbol_refer, begintime, endtime, type=type)
	for fixtable in ['TSymbol_allfuture']:
		fix_data_by_Tsymbol_test(ms05, fixtable, symbol, df1, begintime, endtime)

# sql="select distinct symbol  from symbol_id where LEN(symbol)>=3 order by symbol"
# res=ms05.dict_sql(sql)
# total=[]
# for item in res:
# 	total.append([item['symbol'],item['symbol']])
# print 	total


delete_info=[['AGN',('330','180','150')],['RBnight',('240','60','180','120')],['AUN',('330','180','150')],['CUN',('240','60','180')],['Inight',('330','150')]]


