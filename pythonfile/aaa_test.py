#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

aaalist=[
[datetime.datetime(2016, 1, 1, 0, 0), ['pStepMultituji1_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultituji1_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultituji1_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultituji1_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultituji1_P.csv']]
,[datetime.datetime(2016, 3, 1, 0, 0), ['pStepMultituji1_P.csv']]
,[datetime.datetime(2016, 4, 30, 0, 0), ['pStepMultituji2_P.csv', 'pStepMultituji2_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultituji2_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultituji2_P.csv', 'pStepMultituji2_P.csv', 'pStepMultidnhiprofit_P.csv']]
,[datetime.datetime(2016, 6, 29, 0, 0), ['pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultituji1_P.csv']]
,[datetime.datetime(2016, 8, 28, 0, 0), ['pStepMultiI_up_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultituji1_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultiI_up_P.csv']]
,[datetime.datetime(2016, 10, 27, 0, 0), ['pStepMultidnhiprofit_P.csv', 'pStepMultituji1_P.csv', 'espp_P.csv', 'Pmid_P.csv', 'pStepMultituji1_P.csv', 'pStepMultituji1_P.csv', 'pStepMultituji1_P.csv', 'pStepMultidnhiprofit_P.csv', 'espp_P.csv']]
,[datetime.datetime(2016, 12, 26, 0, 0), ['pStepMultidnhiprofit_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv']]
]


def main_fun(atime,alist):
	totallist=[]
	for csvfile in alist:
		print csvfile
		acname=csvfile.split('.csv')[0]
		df1=pd.read_csv(dir+"\\"+csvfile,names=['a','b','c','d'])
		df1['d']=pd.to_datetime(df1['d'],format='%Y/%m/%d')
		df1['delta_equity']=df1['c']-df1['c'].shift()
		df1=df1.fillna(0)
		df1=df1.set_index(df1['d'])
		df1=df1['delta_equity']
		totallist.append(df1)
	aa=pd.concat(totallist,axis=1)
	aa=aa.fillna(0)
	aa['mymean']=aa.apply(lambda x: x.mean(),axis=1)
	return aa[['mymean']]




atime=aaalist[0][0]
alist=aaalist[0][1]
print atime,alist
dir=r'C:\Users\YuYang\Desktop\yuyang\yuyang_origin-data'
last_equity=pd.DataFrame()
for aaa in aaalist:
	atime=aaa[0]
	alist=aaa[1]
	period_equity=main_fun(atime, alist)
	period_equity=period_equity[period_equity.index>=atime]
	if len(last_equity)==0:
		last_equity=period_equity
	else:
		last_equity=last_equity[last_equity.index<atime]
		last_equity=pd.concat([last_equity,period_equity],axis=0)


last_equity['total']=last_equity['mymean'].cumsum()
last_equity['total'].plot()
plt.show()




# total = pd.DataFrame()
# aa=main_fun(atime,alist)
# print 1
