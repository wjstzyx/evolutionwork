# -*- coding: utf-8 -*-
#按照每天9:00开始，产生N分钟的BAR
import os
import re
import sys
import time
import datetime
import sys
from dbconn import MSSQL

def format_bar_interval(day,minites,resultlist):
    day=day
    fromtime1=day+" "+'09:00:00'
    endtime1=day+" "+'18:00:00'
    fromtime2=day+" "+'21:00:00'
    endtime2=day+" "+'03:00:00'
    fromtime1=datetime.datetime.strptime(fromtime1,'%Y-%m-%d %H:%M:%S')
    endtime1=datetime.datetime.strptime(endtime1,'%Y-%m-%d %H:%M:%S')
    endtime2=datetime.datetime.strptime(endtime2,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(days=1)
    fromtime2=datetime.datetime.strptime(fromtime2,'%Y-%m-%d %H:%M:%S')
    minites=minites
    result1=[]
    result2=[]
    second_result1=[]
    for i in range(200):
        if fromtime1<=endtime1:
            resultlist.append(fromtime1)
        else:
            break
        fromtime1= fromtime1+datetime.timedelta(minutes=minites)
    for i in range(200):
        if fromtime2<=endtime2:
            resultlist.append(fromtime2)
        else:
            break
        fromtime2= fromtime2+datetime.timedelta(minutes=minites)
   
# format_bar_interval('2016-12-05',15)
def total_day_generate(resultlist,fromdate='2014-01-01',interval=15):
    #去假设程序1年不关闭
    endtime=datetime.datetime.now()+datetime.timedelta(days=365)
    length=(endtime-datetime.datetime.strptime(fromdate,'%Y-%m-%d')).days
    fromdate=datetime.datetime.strptime(fromdate,'%Y-%m-%d')
    for i in range(length):
        fromtime1= fromdate+datetime.timedelta(days=i)
        fromtime1=fromtime1.strftime("%Y-%m-%d")
        format_bar_interval(fromtime1,interval,resultlist)


# total_day_generate(15)



def get_Kbarinfo(ms,period,stockdate):
    sql="select a.*,b.O,c.C from  (select Symbol,MIN(StockDate) as openstockdate,MAX(StockDate) as closestockdate,MAX(H) as H,MIN(L) as L,SUM(V) as V,SUM(OPI) as OPI from TSymbol where StockDate>='%s'  AND DATEDIFF(MINUTE,'%s',StockDate)<%s  group by Symbol ) a inner join  TSymbol b on a.Symbol=b.Symbol and a.openstockdate=b.StockDate inner join TSymbol c on a.Symbol=c.Symbol and a.closestockdate=c.StockDate " % (stockdate,stockdate,period)
    # print sql 
    res=ms.dict_sql(sql)
    #put in table
    tempstr=""
    for item in res:
        symbol=item['Symbol']
        sql="Insert_Kbars '%s','%s',%s,%s,%s,%s,%s,%s,%s" % (symbol,stockdate,item['O'],item['C'],item['H'],item['L'],item['V'],item['OPI'],period)
        # print sql
        ms.insert_sql(sql)




def get_Kbarinfo_history(ms,period,stockdate):
    sql="select a.*,b.O,c.C from  (select Symbol,MIN(StockDate) as openstockdate,MAX(StockDate) as closestockdate,MAX(H) as H,MIN(L) as L,SUM(V) as V,SUM(OPI) as OPI from TSymbol_quotes_backup where StockDate>='%s'  AND DATEDIFF(MINUTE,'%s',StockDate)<%s  group by Symbol ) a inner join  TSymbol_quotes_backup b on a.Symbol=b.Symbol and a.openstockdate=b.StockDate inner join TSymbol_quotes_backup c on a.Symbol=c.Symbol and a.closestockdate=c.StockDate " % (stockdate,stockdate,period)
    # print sql 
    res=ms.dict_sql(sql)
    #put in table
    tempstr=""
    for item in res:
        symbol=item['Symbol']
        temp="('%s','%s',%s,%s,%s,%s,%s,%s)" % (symbol,stockdate,item['O'],item['C'],item['H'],item['L'],item['V'],item['OPI']) 
        tempstr=tempstr+","+temp
    tempstr=tempstr.strip(",")
    if tempstr!="":
        if period==5:
            tempstr="insert into [Future].[dbo].[TSymbol_5min]([Symbol],[StockDate],[O]  ,[C]   ,[H]   ,[L]  ,[V] ,[OPI]) values %s" %(tempstr)
        if period==15:
            tempstr="insert into [Future].[dbo].[TSymbol_15min]([Symbol],[StockDate],[O]  ,[C]   ,[H]   ,[L]  ,[V] ,[OPI]) values %s" %(tempstr)
        if period==20:
            tempstr="insert into [Future].[dbo].[TSymbol_20min]([Symbol],[StockDate],[O]  ,[C]   ,[H]   ,[L]  ,[V] ,[OPI]) values %s" %(tempstr)
        if period==30:
            tempstr="insert into [Future].[dbo].[TSymbol_30min]([Symbol],[StockDate],[O]  ,[C]   ,[H]   ,[L]  ,[V] ,[OPI]) values %s" %(tempstr)
        if period==60:
            tempstr="insert into [Future].[dbo].[TSymbol_60min]([Symbol],[StockDate],[O]  ,[C]   ,[H]   ,[L]  ,[V] ,[OPI]) values %s" %(tempstr)
        ms.insert_sql(tempstr)



# get_Kbarinfo(15,'2016-12-05 11:0:00')




def write_heart(type,name):
    ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    sql="update [LogRecord].[dbo].[quotes_python_heart] set [updatetime]=getdate() where type='%s' and name='%s' and [isactive]=1" % (type,name)
    ms.insert_sql(sql)



def main_fun():
    ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms03 = MSSQL(host="192.168.0.3\SQLEXPRESS",user="future",pwd="K@ra0Key",db="future")
    # get_Kbarinfo(ms05,15,'2016-12-13 10:00:00')
    # get_Kbarinfo(ms03,15,'2016-12-13 10:00:00')

    resultlist=[]
    total_day_generate(fromdate='2016-09-01',interval=15,resultlist=resultlist)
    sql="  select distinct  top(60)   stockdate from [Future].[dbo].[TSymbol_%smin] order by stockdate desc" % (15)
    res=ms.dict_sql(sql)
    firsttime=res[-1]['stockdate']
    lasttime=res[0]['stockdate']
    aaa=[item for item in resultlist if item >=firsttime ]
    aaa=[item for item in aaa if item <=lasttime ]
    for item in aaa:
        print item 
        get_Kbarinfo(ms05,15,item)
        get_Kbarinfo(ms03,15,item)
    write_heart('Kbars','queren')

main_fun()



