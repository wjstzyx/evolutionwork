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
date='2017-02-13'
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
        print 1

    totalpd['Col_sum'] = totalpd[symbillist].apply(lambda x: x.sum(), axis=1)
    totalpd['Col_sum_zl'] = totalpd[symbol_zl_list].apply(lambda x: x.sum(), axis=1)
    return totalpd[['Col_sum','Col_sum_zl']]



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
        print 1
    print 1

    totalpd['Col_sum'] = totalpd[symbillist].apply(lambda x: x.sum(), axis=1)
    totalpd=totalpd.sort_values(['day'])
    print 1
    return totalpd[['Col_sum']]



aa=merge_fromhuibao(lilundir)
print aa


positionhuibao=r'C:\YYfiles\evolutionwork\all_future_position\huibao\2017-02-10'
positionaccount=r'C:\YYfiles\evolutionwork\all_future_position\Account\2017-02-10'
positionlilun=r'C:\YYfiles\evolutionwork\all_future_position\Lilun\2017-02-10'
def plot_position(symbol):
    liilun=positionlilun+"\\Lilun_"+symbol.lower()+".csv"
    if os.path.isfile(liilun):
        pass
    else:
        liilun = positionlilun + "\\Lilun_" + symbol.upper() + ".csv"
    df1=pd.read_csv(liilun)
    df1=df1[['stockdate','totalposition']]
    account=positionaccount+"\\Account_"+symbol.lower()+".csv"
    if os.path.isfile(account):
        pass
    else:
        account = positionlilun + "\\Account_" + symbol.upper() + ".csv"
    df2=pd.read_csv(account)
    df2=df2[['stockdate','totalposition']]
    huibao=positionhuibao+"\\huibao_"+symbol.lower()+".csv"
    if os.path.isfile(huibao):
        pass
    else:
        huibao = positionlilun + "\\huibao_" + symbol.upper() + ".csv"
    df3=pd.read_csv(huibao)
    df3=df3[['stockdate','totalposition']]
    aaa=pd.merge(df1,df2,'outer','stockdate',suffixes=('_lilun','_account'))
    aaa=pd.merge(aaa,df3,'outer','stockdate')
    aaa=aaa.sort_values(['stockdate'])
    aaa['lilun']=aaa['totalposition_lilun']
    aaa['account'] = aaa['totalposition_account']
    aaa['huibao'] = aaa['totalposition']
    aaa =aaa.set_index('stockdate')
    aaa=aaa.fillna(method='ffill')
    return aaa[['lilun','account','huibao']]




# sql='select distinct symbol from tsymbol_allfuture order by symbol'
# res=ms.dict_sql(sql)
# for item in res:
#     try:
#         print item['symbol']
#         sss=plot_position(item['symbol'])
#         sss['myindex']=sss.index
#         sss=sss[(sss['myindex']>='2017-01-19 00:00:00') & (sss['myindex']<='2017-02-10 00:00:00')]
#         sss[['account','huibao']].plot()
#         plt.show()
#     except:
#         pass


