#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import matplotlib.pyplot as plt
import sys
reload(sys)
import csv
import pandas as pd
import numpy as np
import os
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

lilundir=r'C:\YYfiles\evolutionwork\all_future_position\Lilun_dayli_equity'
accoutdir=r'C:\YYfiles\evolutionwork\all_future_position\Account_dayli_equity'
huibaodir=r'C:\YYfiles\evolutionwork\all_future_position\huibao_dayli_equity'
global date
# date='2017-02-15'
# acname='sssss'
# mytype='lilun'
date=sys.argv[1]
acname=sys.argv[2]
mytype=sys.argv[3]

def merge_fromhuibao(lilundir):
    totalpd=pd.DataFrame()
    filelists=os.listdir(lilundir+"\\"+date)
    symbillist=[]
    symbol_zl_list=[]

    for item in filelists:
        symbol=item.split('.csv')[0].split('_')[-1]
        df1=pd.read_csv(lilundir+"\\"+str(date)+"\\"+item)
        df1[symbol]=df1['equity']
        df1[symbol+'_zl'] = df1['equity_ZL']
        df1=df1[[symbol,symbol+'_zl','day']]
        symbillist.append(symbol)
        symbol_zl_list.append(symbol+'_zl')
        if len(totalpd)==0:
            totalpd=df1
        else:
            totalpd=pd.merge(totalpd,df1,'outer',left_on='day',right_on='day')
        totalpd= totalpd.set_index(totalpd['day'])

    # delete first day data
    totalpd=totalpd.iloc[2:]
    totalpd['Col_sum'] = totalpd[symbillist].apply(lambda x: x.sum(), axis=1)
    totalpd['Col_sum_zl'] = totalpd[symbol_zl_list].apply(lambda x: x.sum(), axis=1)

    tempa=totalpd[symbillist].apply(lambda x: x.sum())
    tempa=tempa.reset_index()

    tempb=totalpd[symbol_zl_list].apply(lambda x: x.sum())
    tempb=tempb.reset_index()
    tempb['index'] =tempb['index'].apply(lambda x: x[:-3])

    aaa=pd.merge(tempa,tempb,'outer',on='index',suffixes=('_zhishu','_ZL'))
    aaa['dist']=aaa['0_ZL']-aaa['0_zhishu']

    return totalpd[['Col_sum','Col_sum_zl']],aaa



def merge_fromhuibao_huibao(lilundir):
    totalpd=pd.DataFrame()
    filelists=os.listdir(lilundir+"\\"+date)
    symbillist=[]
    for item in filelists:
        symbol=item.split('.csv')[0].split('_')[-1]
        df1=pd.read_csv(lilundir+"\\"+str(date)+"\\"+item)
        df1[symbol]=df1['equity']
        df1=df1[[symbol,'day']]
        symbillist.append(symbol)
        if len(totalpd)==0:
            totalpd=df1
        else:
            totalpd=pd.merge(totalpd,df1,'outer',left_on='day',right_on='day')
        totalpd= totalpd.set_index(totalpd['day'])



    totalpd['Col_sum'] = totalpd[symbillist].apply(lambda x: x.sum(), axis=1)
    totalpd=totalpd.sort_values(['day'])
    return totalpd[['Col_sum']]




def merge__by_date_by_symbol(lilundir):
    totalpd=pd.DataFrame()
    filelists=os.listdir(lilundir+"\\"+date)
    symbillist=[]
    symbol_zl_list=[]

    for item in filelists:
        symbol=item.split('.csv')[0].split('_')[-1]
        df1=pd.read_csv(lilundir+"\\"+str(date)+"\\"+item)
        df1[symbol]=df1['equity']
        df1[symbol+'_zl'] = df1['equity_ZL']
        df1=df1[[symbol,symbol+'_zl','day']]
        symbillist.append(symbol)
        symbol_zl_list.append(symbol+'_zl')
        if len(totalpd)==0:
            totalpd=df1
        else:
            totalpd=pd.merge(totalpd,df1,'outer',left_on='day',right_on='day')
        totalpd= totalpd.set_index(totalpd['day'])


    totalpd['Col_sum'] = totalpd[symbillist].apply(lambda x: x.sum(), axis=1)
    totalpd['Col_sum_zl'] = totalpd[symbol_zl_list].apply(lambda x: x.sum(), axis=1)

    tempa=totalpd[symbillist].apply(lambda x: x.sum())
    tempa=tempa.reset_index()

    tempb=totalpd[symbol_zl_list].apply(lambda x: x.sum())
    tempb=tempb.reset_index()
    tempb['index'] =tempb['index'].apply(lambda x: x[:-3])

    aaa=pd.merge(tempa,tempb,'outer',on='index',suffixes=('_zhishu','_ZL'))
    aaa['dist']=aaa['0_ZL']-aaa['0_zhishu']



    return totalpd[['Col_sum','Col_sum_zl']],aaa




# aaa=merge__by_date_by_symbol(lilundir)
# print aaa
# exit()

if mytype=='lilun':
    aa,by_symbol=merge_fromhuibao(lilundir)
    aa.sort_index(inplace=True)
    path=r'C:\YYfiles\evolutionwork\all_future_position\results'
    aa.to_csv(path+"\\"+acname+"_"+mytype+".csv")
    by_symbol.to_csv(path + "\\" + acname + "_by_symbol_" + mytype + ".csv")
if mytype=='position':
    aa=merge_fromhuibao(accoutdir)
    path=r'C:\YYfiles\evolutionwork\all_future_position\results'
    aa.to_csv(path+"\\"+acname+"_"+mytype+".csv")
if mytype=='huibao':
    aa=merge_fromhuibao(huibaodir)
    path=r'C:\YYfiles\evolutionwork\all_future_position\results'
    aa.to_csv(path+"\\"+acname+"_"+mytype+".csv")




