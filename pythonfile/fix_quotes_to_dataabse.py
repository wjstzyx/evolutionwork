# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, sys
from os.path import join, getsize, splitext, split
# import pandas as pd
# import numpy as np
# import pdb
from ftplib import FTP
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList




##将下载的数据按照数据库格式生成
def  add_data_wenhua(rawroot,date, timestart, timeend,mysymbol=''):
    timestart=int(timestart)
    timeend=int(timeend)
    fin = open(join(rawroot, str(date)+'.csv'))
    targetfilename=join(rawroot, str(date)+'_'+str(timestart)+'_'+str(timeend)+'.csv')
    fout = open(join(rawroot, str(date)+'_'+str(timestart)+'_'+str(timeend)+'.csv'), 'w') 
    for line in fin:        
        p = line.split()
        if len(p)<5:
            continue        
        date=p[5][0:-4]
        time = p[5][-4:]
        if int(time)<timestart or int(time)>timeend:
            continue            
        odate = date[:4] + '/' + date[4:6] + '/' + date[6:]
        otime = time[0:2]+':'+time[2:4]     
        datetime =date[:4] + '-' + date[4:6] + '-' + date[6:]+' '+ otime+':00.000'        
        symbol = p[2]
        oopen = p[6]
        ohigh = p[7]
        olow = p[8]
        oclose = p[9]
        ovol= p[12]
        oopi = p[-3]
        orefc = p[-1]
        if mysymbol=='' or mysymbol.lower()== symbol.lower():
            resarr=[symbol,oopen,oclose,ohigh,olow,ovol,oopi,odate,otime,datetime,orefc]        
            newline = ','.join(resarr).strip() + '\n'
            fout.write(newline)
        
    fin.close()
    fout.close()
    print  "produce File OK"  
    return targetfilename
        


##读取数据写入数据库
def read_date_write_to_database_day(ms,targetfile,date,mysymbol=''):
    #ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    #date=20160428
    date=str(date)
    date=date[0:4]+'/'+date[4:6]+'/'+date[6:8]
    print "Starting..."
    file = open(targetfile)
    successnum=0
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            line=line.strip('\n')
            linelist=line.split(',')
            timeint=int(linelist[8][0:2])*100+int(linelist[8][3:])
            if linelist[7]==date and (timeint>=900 and timeint<=1530) and (mysymbol=='' or mysymbol.lower()==linelist[0].lower()) and  linelist[0] not in ('CMXGLD','SG@A50','BRENTOIL','CMXSLV','UK@CU'):
                sql="insert into Tsymbol ([Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc])values('%s',%s,%s,%s,%s,%s,%s,'%s','%s','%s',%s)" % (linelist[0],linelist[1],linelist[2],linelist[3],linelist[4],linelist[5],linelist[6],linelist[7],linelist[8],linelist[9],linelist[10])
                try:
                    ms.insert_sql(sql)
                    successnum=successnum+1
                    print successnum
                except Exception,e:
                    if "Cannot insert duplicate key row" in str(e):
                        pass                
                    else:
                        break
    file.close()
    print "Finish"
    print "Success Insert Num :",successnum

def read_date_write_to_database_night(ms,targetfile,date,mysymbol=''):
    #ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    #date=20160428
    date=str(date)
    date=date[0:4]+'/'+date[4:6]+'/'+date[6:8]
    print "Starting..."
    file = open(targetfile)
    successnum=0
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            line=line.strip('\n')
            linelist=line.split(',')
            isnight=0
            timeint=int(linelist[8][0:2])*100+int(linelist[8][3:])
            # print timeint

            if ((timeint>=2100 and timeint<=2359) or (timeint>=0000 and timeint<=400)) and  (mysymbol=='' or mysymbol.lower()==linelist[0].lower()) and  linelist[0] not in ('CMXGLD','SG@A50','BRENTOIL','CMXSLV','UK@CU'):
                
                if linelist[0]=='RB':
                    linelist[0]='RBnight'
                    isnight=1
                if linelist[0]=='P':
                    linelist[0]='Rnight'
                    isnight=1
                if linelist[0]=='RU':
                    linelist[0]='RUnight'
                    isnight=1
                if linelist[0]=='TA':
                    linelist[0]='TAnight'
                    isnight=1
                if linelist[0]=='NI':
                    linelist[0]='NInight'
                    isnight=1
                if linelist[0]=='L':
                    linelist[0]='Lnight'
                    isnight=1
                if linelist[0]=='J':
                    linelist[0]='Jnight'
                    isnight=1
                if linelist[0]=='I':
                    linelist[0]='Inight'
                    isnight=1
                if linelist[0]=='HC':
                    linelist[0]='HCnight'
                    isnight=1
                if linelist[0]=='CS':
                    linelist[0]='CSnight'
                    isnight=1
                if linelist[0]=='BU':
                    linelist[0]='BUnight'
                    isnight=1
                if linelist[0]=='AL':
                    linelist[0]='ALnight'
                    isnight=1
                if isnight==1:
                    sql="insert into Tsymbol ([Symbol],[O],[C],[H],[L],[V],[OPI],[D],[T],[StockDate],[refc])values('%s',%s,%s,%s,%s,%s,%s,'%s','%s','%s',%s)" % (linelist[0],linelist[1],linelist[2],linelist[3],linelist[4],linelist[5],linelist[6],linelist[7],linelist[8],linelist[9],linelist[10])
                    #print sql 
                    try:
                        ms.insert_sql(sql)
                        successnum=successnum+1
                        print successnum
                    except Exception,e:
                        if "Cannot insert duplicate key row" in str(e):
                            pass                
                        else:
                            break
    file.close()
    print "Finish"
    print "Success Insert Num :",successnum





_dfrom =r'Y:\data_wenhua'

if os.path.exists(_dfrom):
    pass
else:
    _dfrom =r'/home/yuyang/myfile/data_wenhua'



sql="select replace(convert(nvarchar(10),getdate(),120),'-','') as mydate"
res=ms.dict_sql(sql)
date = res[0]['mydate']
#date=20160918
if len(sys.argv)>1:
    date=sys.argv[1]
#date=20160513
if len(sys.argv)>2:
    mysymbol=sys.argv[2]
else:
    mysymbol=''
timestart ='0000'
timeend = 2359
print date,mysymbol


targetfilename=add_data_wenhua(_dfrom,date, timestart, timeend,mysymbol )  #  extrct  data from timestart to timeend


#按顺序往不同数据库写入
try:
    print "write into 05"
    ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    read_date_write_to_database_night(ms05,targetfilename,date,mysymbol) # targetfile=r'Y:\data_wenhua\20160427_0_2359.csv'
    read_date_write_to_database_day(ms05,targetfilename,date,mysymbol)
except Exception,e:
    msg="05数据库 "+str(e).replace("'",'#')
    sql="insert into [LogRecord].[dbo].[report_daily_error](type,msg) values('%s','%s')" ('定时补全数据',msg)
    ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms05.insert_sql(sql)
    
try：
    print "write into 03"
    ms03 = MSSQL(host="192.168.0.3",user="future",pwd="K@ra0Key",db="future")
    read_date_write_to_database_night(ms03,targetfilename,date,mysymbol) # targetfile=r'Y:\data_wenhua\20160427_0_2359.csv'
    read_date_write_to_database_day(ms03,targetfilename,date,mysymbol)
except Exception,e:
    msg="03数据库 "+str(e).replace("'",'#')
    sql="insert into [LogRecord].[dbo].[report_daily_error](type,msg) values('%s','%s')" ('定时补全数据',msg)
    ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms05.insert_sql(sql)

try:
    print "write into 07"
    ms07 = MSSQL(host="192.168.0.7",user="future",pwd="K@ra0Key",db="future")
    read_date_write_to_database_night(ms07,targetfilename,date,mysymbol) # targetfile=r'Y:\data_wenhua\20160427_0_2359.csv'
    read_date_write_to_database_day(ms07,targetfilename,date,mysymbol)
except Exception,e:
    msg="07数据库 "+str(e).replace("'",'#')
    sql="insert into [LogRecord].[dbo].[report_daily_error](type,msg) values('%s','%s')" ('定时补全数据',msg)
    ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms05.insert_sql(sql)

try:
    print "write into cloud"
    mscloud = MSSQL(host="139.196.190.246",user="future",pwd="K@ra0Key",db="future")
    read_date_write_to_database_night(mscloud,targetfilename,date,mysymbol) # targetfile=r'Y:\data_wenhua\20160427_0_2359.csv'
    read_date_write_to_database_day(mscloud,targetfilename,date,mysymbol)
except Exception,e:
    msg="cloud数据库 "+str(e).replace("'",'#')
    sql="insert into [LogRecord].[dbo].[report_daily_error](type,msg) values('%s','%s')" ('定时补全数据',msg)
    ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms05.insert_sql(sql)


