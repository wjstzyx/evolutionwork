# -*- coding: utf-8 -*-
#按照每天9:00开始，产生N分钟的BAR
import os
import re
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import datetime
fromtime=datetime.datetime.strptime('09:00:00','%H:%M:%S')
def format_bar(day,minites):
    day=day
    fromtime1=day+" "+'09:00:00'
    endtime1=day+" "+'18:00:00'
    fromtime2=day+" "+'21:00:00'
    endtime2=day+" "+'04:00:00'
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
            result1.append(fromtime1)
        else:
            break
        fromtime1= fromtime1+datetime.timedelta(minutes=minites)
    for i in range(200):
        if fromtime2<=endtime2:
            result1.append(fromtime2)
        else:
            break
        fromtime2= fromtime2+datetime.timedelta(minutes=minites)
    for item in result1:
        for i in range(minites):
            temp=[item,item+datetime.timedelta(minutes=i)]
            second_result1.append(temp)
    tempstr=""
    for item in second_result1:
        temp="('%s','%s',%s)" % (item[0],item[1],minites)
        tempstr=tempstr+","+temp
    tempstr=tempstr.strip(",")
    tempstr="insert into [Future].[dbo].[Kbars_merge]([stockdate],[intervaldate],[period]) values %s" %(tempstr)
    ms.insert_sql(tempstr)
    
# format_bar('2016-11-04',15)



def format_bar_interval(day,minites):
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
            result1.append(fromtime1)
        else:
            break
        fromtime1= fromtime1+datetime.timedelta(minutes=minites)
    for i in range(200):
        if fromtime2<=endtime2:
            result1.append(fromtime2)
        else:
            break
        fromtime2= fromtime2+datetime.timedelta(minutes=minites)
    # print result1[:10]

    tempstr=""
    for item in result1:
        temp="('%s',%s)" % (item,minites)
        tempstr=tempstr+","+temp
    tempstr=tempstr.strip(",")
    tempstr="insert into [Future].[dbo].[Kbars_merge]([intervaldate],[period]) values %s" %(tempstr)
    ms.insert_sql(tempstr)
   
# format_bar_interval('2016-12-05',15)
def total_day_generate(interval):
    fromdate='2014-01-01'
    fromdate=datetime.datetime.strptime(fromdate,'%Y-%m-%d')
    for i in range(2000):
        fromtime1= fromdate+datetime.timedelta(days=i)
        fromtime1=fromtime1.strftime("%Y-%m-%d")
        print fromtime1
        format_bar_interval(fromtime1,interval)




# total_day_generate(15)



def get_Kbarinfo(period,stockdate):
    # stockdate='2016-12-05 11:15:00'
    # period=15
    # sql='select top(15) * from TSymbol where StockDate>='2016-12-05 11:15:00' AND Symbol='rb' AND DATEDIFF(MINUTE,'2016-12-05 11:15:00',StockDate)<=15 order by StockDate'
    # sql="select Symbol,MIN(StockDate) as openstockdate,MAX(StockDate) as closestockdate,MAX(H) as H,MIN(L) as L,SUM(V) as V,SUM(OPI) as OPI from TSymbol where StockDate>='%s'  AND DATEDIFF(MINUTE,'%s',StockDate)<=%s group by Symbol ORDER BY SYMBOL" % (stockdate,stockdate,period)
    sql="select a.*,b.O,c.C from  (select Symbol,MIN(StockDate) as openstockdate,MAX(StockDate) as closestockdate,MAX(H) as H,MIN(L) as L,SUM(V) as V,SUM(OPI) as OPI from TSymbol_quotes_backup where StockDate>='%s'  AND DATEDIFF(MINUTE,'%s',StockDate)<%s  group by Symbol ) a inner join  TSymbol_quotes_backup b on a.Symbol=b.Symbol and a.openstockdate=b.StockDate inner join TSymbol_quotes_backup c on a.Symbol=c.Symbol and a.closestockdate=c.StockDate " % (stockdate,stockdate,period)
    # print sql 
    res=ms.dict_sql(sql)
    #put in table
    tempstr=""
    for item in res:
        symbol=item['Symbol']
        sql="Insert_Kbars '%s','%s',%s,%s,%s,%s,%s,%s" % (symbol,stockdate,item['O'],item['C'],item['H'],item['L'],item['V'],item['OPI'])
        ms.insert_sql(sql)
        
    #     temp="('%s','%s',%s,%s,%s,%s,%s,%s)" % (symbol,stockdate,item['O'],item['C'],item['H'],item['L'],item['V'],item['OPI']) 
    #     tempstr=tempstr+","+temp
    # tempstr=tempstr.strip(",")
    # if tempstr!="":
    #     tempstr="insert into [Future].[dbo].[TSymbol_15min]([Symbol],[StockDate],[O]  ,[C]   ,[H]   ,[L]  ,[V] ,[OPI]) values %s" %(tempstr)
    #     ms.insert_sql(tempstr)





# get_Kbarinfo(15,'2016-12-05 11:0:00')






def general_Kbars(intervaltime):
    sql="select * from [Future].[dbo].[Kbars_merge]  where period=%s and intervaldate>='2015-01-02 12:30:00'  and  intervaldate<='2016-12-07' order by [intervaldate] " % (intervaltime)
    #'2016-03-19 12:30:00'
    res=ms.dict_sql(sql)
    for item in res:
        print item 
        get_Kbarinfo(intervaltime,item['intervaldate'])

general_Kbars(15)




def generate_p_basic():
    rootpath=r'C:\Users\YuYang\Desktop\TEMP'
    filelist=os.listdir(rootpath)
    for item in filelist:
        if os.path.isdir(rootpath+"\\"+item):
            sfile=os.listdir(rootpath+"\\"+item)
            for item1 in sfile:
                f=open(rootpath+"\\"+item+"\\"+item1,'r')
                aa=f.read()
                # pattern=r'StrategyName = "60min_30_25_getDAYBREAKER";'
                pattern=r'StrategyName = "30min_30_20_getADTMfisher1";'
                ismatch=re.search(pattern,aa)
                if ismatch:
                    pattern1=r'StrategyID = "(.*)";'
                    ismatch1=re.search(pattern1,aa)
                    st=ismatch1.group(1)
                    s_id=st[3:5]
                    s_id=int(s_id)
                    print item,",",s_id,",",ismatch1.group(1),",",1,",",1

# generate_p_basic()
