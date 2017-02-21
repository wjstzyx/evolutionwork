#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import  os
import pandas as pd

import numpy as np
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

datarooe=r'C:\Users\YuYang\Documents\Tencent Files\794513386\FileRecv\jieti1_zhuli_zhishu'
def aa_fun(filename):
    fileroot=datarooe+"\\"+filename
    df1=pd.read_csv(fileroot)
    df1=df1[['Date/Time','ProfitDiff_zhuli','ProfitDiff_zhishu','Ticker']]
    df1['stockdate']=pd.to_datetime(df1['Date/Time'],format='%Y/%m/%d %H:%M:%S')

    df1['day']=df1['stockdate'].dt.strftime('%Y%m%d')
    df1['myindex']=df1['day']+'_'+df1['Ticker']
    df2=df1[['myindex','ProfitDiff_zhuli','ProfitDiff_zhishu']].groupby(['myindex'])
    df3=df2.sum()[['ProfitDiff_zhuli']]
    df4 = df2.sum()[['ProfitDiff_zhishu']]

    return df3,df4


filelist=os.listdir(datarooe)
bigdata1=[]
bigdata2=[]
for item in filelist:
    df1,df2=aa_fun(item)
    bigdata1.append(df1)
    bigdata2.append(df2)

print 1
aa=pd.concat(bigdata1,axis=1)
bb=pd.concat(bigdata2,axis=1)
aa['sum']=aa.apply(lambda x: x.sum(), axis=1)
bb['sum']=bb.apply(lambda x: x.sum(), axis=1)
aa=aa[['sum']]
bb=bb[['sum']]
aa.to_csv(r'C:\YYfiles\evolutionwork\all_future_position\afile\ProfitDiff_zhuli.csv')
bb.to_csv(r'C:\YYfiles\evolutionwork\all_future_position\afile\ProfitDiff_zhishu.csv')






