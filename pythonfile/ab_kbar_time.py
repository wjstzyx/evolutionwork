# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:27:39 2017

@author: jesse
"""
import datetime 
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")


def main_fun(tf = 43):
    #time frame

    # begin_hour and time
    base_h = 9
    base_m = 0

    timelist=list()

    # one day has 1440min
    # move forward until midnight !! why ???
    for i in range(0,1440,tf):
        currm = base_h * 60 + base_m + i    

        h = currm/60
        m = currm % 60
        if h > 23:
            #h = h % 24
        
            #print "HH:MM",h,m
            break
        else:
            #print "HH:MM",h,m
            timelist.append(h*100+m)

    last_end_start = timelist[-1]
    #print "last_end_start",last_end_start

    #move backward until midnight!! why ???
    for i in range(0,-1440,-tf):
        currm = base_h * 60 + base_m + i     

        h = currm/60
        m = currm % 60
        
        if h< 0:
            
            h = h + 24
            print 100*h+m
            
            
            # if time < last day's lastbar's begin time,break
            if h* 100 + m <= last_end_start :
                
                break
            else:
                timelist.append(h*100+m)
        else:
        
            #h = h % 24
            
            #print "HH:MM",h,m
            timelist.append(h*100+m)



    timelist.remove(base_h * 100 + base_m)
    timelist.sort()
    print timelist
    beginlist=[]
    endlist=[]
    for item in timelist:
        if len(str(item))<=4:
            temp='0'*(4-len(str(item)))+str(item)
        barbegin=datetime.datetime.strptime('2010-01-02 '+temp,'%Y-%m-%d %H%M')
        barend=barbegin-datetime.timedelta(minutes=1)
        beginlist.append(barbegin.strftime('%H:%M:%S'))
        endlist.append(barend.strftime('%H:%M:%S'))

    newendlist=endlist[1:]
    newendlist.append(endlist[0])
    totalsql=""
    for i in range(len(beginlist)):
        sql=" insert into  [LogRecord].[dbo].[AB_BAR_interval] ([period],[begintime],[endtime]) values(%s,'%s','%s');" % (tf,beginlist[i],newendlist[i])
        totalsql=totalsql+sql
    ms.insert_sql(totalsql)
    

for i in range(6,180):

    main_fun(tf = i)