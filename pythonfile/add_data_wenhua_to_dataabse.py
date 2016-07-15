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
#ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

##ftp下载数据
def ftp_down(dfrom,localf,filename = "histWhcj.txt"):
    try:
        ftp=FTP() 
        ftp.set_debuglevel(2) 
        ftp.connect('120.26.89.143','8021') 
       # pdb.set_trace() 
      #  print '11111'
        ftp.login('el','104104') 
        #print ftp.getwelcome()#显示ftp服务器欢迎信息
        lf = str(localf)
        ml = lf[-4:]
        ftp.cwd(ml+'_1m/') #选择操作目录
        # ftp.cwd(ml+'_1m(all_40cid)/') #选择操作目录 
        #0324_1m(all_40cid)
        bufsize = 1024 
        localname = lf+".csv"
        localname = open(os.path.join(dfrom,localname),'wb')
        file_handler =localname.write #以写模式在本地打开文件 
        ftp.retrbinary('RETR %s' % os.path.basename(filename),file_handler,bufsize)#接收服务器上文件并写入本地文件 
        ftp.set_debuglevel(0) 
        localname.close() 
        ftp.quit() 
        print "ftp down OK"
        return 1
    except Exception,e:
        print str(e)
        return 0






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
def read_date_write_to_database(targetfile,date,mysymbol=''):
    ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
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
            if linelist[7]==date and (mysymbol=='' or mysymbol.lower()==linelist[0].lower()):
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








_dfrom =r'Y:\data_wenhua'

if os.path.exists(_dfrom):
    pass
else:
    _dfrom =r'/home/yuyang/myfile/data_wenhua'
date = sys.argv[1] 
#date=20160513
if len(sys.argv)>2:
    mysymbol=sys.argv[2]
else:
    mysymbol=''
timestart ='0900'
timeend = 1600
print date,mysymbol


targetfile=_dfrom+'\\'+str(date)+'.csv'
if not os.path.isfile(targetfile):
    print "can not find file,and I will create it",targetfile
    newtargetfile=open(targetfile, 'w')
    newtargetfile.close()


downresult=ftp_down(_dfrom,date)# down from ftp
#downresult=1
if downresult==1:
    targetfilename=add_data_wenhua(_dfrom,date, timestart, timeend,mysymbol )  #  extrct  data from timestart to timeend
    read_date_write_to_database(targetfilename,date,mysymbol) # targetfile=r'Y:\data_wenhua\20160427_0_2359.csv'


