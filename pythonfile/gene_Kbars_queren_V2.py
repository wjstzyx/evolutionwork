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
    sql="select a.*,b.O,c.C,c.OPI from  (select Symbol,MIN(StockDate) as openstockdate,MAX(StockDate) as closestockdate,MAX(H) as H,MIN(L) as L,SUM(V) as V from TSymbol where StockDate>='%s'  AND DATEDIFF(MINUTE,'%s',StockDate)<%s  group by Symbol ) a inner join  TSymbol b on a.Symbol=b.Symbol and a.openstockdate=b.StockDate inner join TSymbol c on a.Symbol=c.Symbol and a.closestockdate=c.StockDate " % (stockdate,stockdate,period)
    # print sql 
    res=ms.dict_sql(sql)
    #put in table
    tempstr=""
    for item in res:
        symbol=item['Symbol']
        sql="Insert_Kbars '%s','%s',%s,%s,%s,%s,%s,%s,%s" % (symbol,stockdate,item['O'],item['C'],item['H'],item['L'],item['V'],item['OPI'],period)
        #print sql
        ms.insert_sql(sql)




def get_Kbarinfo_history(ms,period,stockdate):
    sql="select a.*,b.O,c.C,c.OPI from  (select Symbol,MIN(StockDate) as openstockdate,MAX(StockDate) as closestockdate,MAX(H) as H,MIN(L) as L,SUM(V) as V from TSymbol_quotes_backup where StockDate>='%s'  AND DATEDIFF(MINUTE,'%s',StockDate)<%s  group by Symbol ) a inner join  TSymbol_quotes_backup b on a.Symbol=b.Symbol and a.openstockdate=b.StockDate inner join TSymbol_quotes_backup c on a.Symbol=c.Symbol and a.closestockdate=c.StockDate " % (stockdate,stockdate,period)
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








def write_heart(type,name):
    ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    sql="update [LogRecord].[dbo].[quotes_python_heart] set [updatetime]=getdate() where type='%s' and name='%s' and [isactive]=1" % (type,name)
    ms.insert_sql(sql)






def gene_history_Kbars(ms,period,fromtime='2015-01-01'):
    resultlist=[]
    total_day_generate(fromdate=fromtime,interval=period,resultlist=resultlist)
    aaa=resultlist

    sql="select distinct symbol from Tsymbol"
    symbollist=ms.dict_sql(sql)
    totalKbars={}
    for symboldict in symbollist:
        symbol=symboldict['symbol']
        print symbol
        tempaaa=aaa[:]
        sql="select * from TSymbol_quotes_backup where symbol='%s' and stockdate>='%s'  order by stockdate" % (symbol,fromtime)
        quotes=ms.dict_sql(sql)
        tempindex=0
        cpmparetime=tempaaa[0]
        newquotes={}
        for item in quotes:
            stockdate=item['StockDate']
            #print "#",stockdate,cpmparetime,tempaaa[0]
            if (stockdate - cpmparetime).total_seconds()>=period*60 and len(tempaaa)>0:
                # next tempaaa
                tt=1
                while (tt):
                    #print stockdate,cpmparetime,(stockdate - cpmparetime).total_seconds()
                    if (stockdate - cpmparetime).total_seconds()<0:
                        #stockdate 后移动
                        tt=0
                        tempindex=0
                    else:
                        if (stockdate - cpmparetime).total_seconds()<period*60 and (stockdate - cpmparetime).total_seconds()>=0:
                            tt=0
                            tempindex=0
                        else:
                            if len(tempaaa)>0:
                                cpmparetime=tempaaa.pop(0)
                            else:
                                print tempaaa
                                print stockdate,cpmparetime
                                print '3333',cpmparetime
                                break

            if (stockdate - cpmparetime).total_seconds()<period*60 and (stockdate - cpmparetime).total_seconds()>=0:
                # print cpmparetime

                # 1min bar is between the period,group by
                if tempindex==0:
                    #tempquote=[o,c,h,l,v,opi]
                    tempquote=[item['O'],item['C'],item['H'],item['L'],item['V'],item['OPI']]
                    # tempquote.append(stockdate)
                    # tempquote.append(cpmparetime)
                else:
                    tempquote[1]=item['C']
                    tempquote[2]=max(tempquote[2],item['H'])
                    tempquote[3]=min(tempquote[3],item['L'])
                    tempquote[4]=tempquote[4]+item['V']
                    tempquote[5]=item['OPI']
                    # tempquote.append(stockdate)
                tempindex=tempindex+1
                newquotes[cpmparetime]=tempquote
        items=newquotes.items()
        items.sort()
        listnewquotes=[[key,value] for key,value in items]
        totalKbars[symbol]=listnewquotes
    return totalKbars








def compare_kbars(ms,period,fromtime):
    kbars=gene_history_Kbars(ms,period,fromtime)
    sql="select distinct symbol from Tsymbol "
    symbollist=ms.dict_sql(sql)
    for symboldict in symbollist:
        symbol=symboldict['symbol']        

        # compare with [TSymbol_%smin]
        sql="SELECT [O] ,[C] ,[H]  ,[L] ,[V] ,[OPI],[StockDate]  FROM [Future].[dbo].[TSymbol_%smin] where symbol='%s' and stockdate>='%s'" % (period,symbol,fromtime)
        res=ms.dict_sql(sql)
        refquotes={}
        for item in res:
            refquotes[item['StockDate']]=[item['O'],item['C'],item['H'],item['L'],item['V'],item['OPI']]
        newquotes=kbars[symbol]

        for item in newquotes:
            if refquotes.has_key(item[0]):
                if item[1]!=refquotes[item[0]]:
                    newitem1=[round(item[1][0],2),round(item[1][1],2),round(item[1][2],2),round(item[1][3],2),round(item[1][4],2),round(item[1][5],2)]
                    refquotes1=[round(refquotes[item[0]][0],2),round(refquotes[item[0]][1],2),round(refquotes[item[0]][2],2),round(refquotes[item[0]][3],2),round(refquotes[item[0]][4],2),round(refquotes[item[0]][5],2)]
                    if newitem1!=refquotes1:
                        print symbol,item[0],item[1]
                        print symbol,item[0],refquotes[item[0]]
                        print '@@@@@@@@@@@@@@@'
                        # use other method fix
                        get_Kbarinfo(ms,period,item[0])
                    # wright log
            else:
                print 'TSymbol_%smin short of Kbars  %s %s' % (period,symbol,item[0])
                # use ather method fix the date
                get_Kbarinfo(ms,period,item[0])




def main_fun():
    #ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms03 = MSSQL(host="192.168.0.3\SQLEXPRESS",user="future",pwd="K@ra0Key",db="future")
    fromtime=datetime.datetime.now()-datetime.timedelta(days=20)
    fromtime=fromtime.strftime('%Y-%m-%d')
    print fromtime
    index=0
    try:
        compare_kbars(ms03,15,fromtime)
    except:
        index=index+1
        pass
    try:
        compare_kbars(ms05,15,fromtime)
    except:
        index=index+1
        pass
    try:
        compare_kbars(ms03,5,fromtime)
    except:
        index=index+1
        pass
    try:
        compare_kbars(ms05,5,fromtime)
    except:
        index=index+1
        pass
    try:
        compare_kbars(ms05,30,fromtime)
    except:
        index=index+1
        pass

    if index==0:
        write_heart('Kbars','queren')
#ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# get_Kbarinfo(ms05,5,'2016-12-02 14:00:00')
main_fun()




#########for generate######################
#ms03 = MSSQL(host="192.168.0.3\SQLEXPRESS",user="future",pwd="K@ra0Key",db="future")
#ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
def from_begin_generate_Kbars(myms,period,starttime):    
    print "begin"
    totalKbars=gene_history_Kbars(myms,period,starttime)
    for key in totalKbars:
        if len( totalKbars[key])>0:
            content=""
            i=0
            for item in totalKbars[key]:
                i=i+1
                temp="('%s','%s',%s,%s,%s,%s,%s,%s)" % (key,item[0],item[1][0],item[1][1],item[1][2],item[1][3],item[1][4],item[1][5])
                # print temp
                content=content+","+temp
                if i>998:
                    content=content.strip(',')
                    sql="insert into [Future].[dbo].[TSymbol_%smin](symbol,[StockDate],O,C,H,L,V,OPI) values%s" % (period,content)
                    myms.insert_sql(sql)
                    content=""
                    i=0
            content=content.strip(',')
            if len(content)>10:
                sql="insert into [Future].[dbo].[TSymbol_%smin](symbol,[StockDate],O,C,H,L,V,OPI) values%s" % (period,content)
                myms.insert_sql(sql)
        else:
            print key


# from_begin_generate_Kbars(ms03,30,'2015-01-01')