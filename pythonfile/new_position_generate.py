#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import pandas as pd
import numpy as np
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

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
            print [item[0], round(item[1],6), round(temptotal,6)]
        posotion_pd=pd.DataFrame(positionlist,columns=['stockdate','deltaposition','totalposition'])
        return posotion_pd
    else:
        print 'no position'
        return  []
        # fisrttime = positionlist[0][0]
        # #添加 每天的结束时间
        # sql="select min(StockDate) as stockdate from TSymbol_quotes_backup where Symbol='%s' and  T>='20:00' and stockdate >='%s' group by D order by D" % (symbol,fisrttime)
        # daylist=ms.dict_sql(sql)
        # daylist_pd=pd.DataFrame(daylist)
        # posotion_pd=posotion_pd.append(daylist_pd,ignore_index=True)
        # posotion_pd['myindex']=posotion_pd.index
        # posotion_pd=posotion_pd.sort_values(['stockdate','myindex'],ascending=['True','False'])
        # posotion_pd=posotion_pd.fillna(method='ffill')
        #
        # print 1

# 作用于品种，添加每天收盘的价格
def generate_new_position(position,symbol):
    pass

position=get_position(acname='rbn4other',symbol='rbnight')

print 1

