# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os, sys
from os.path import join, getsize, splitext, split
from ftplib import FTP
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
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







_dfrom =r'Y:\data_wenhua'

if os.path.exists(_dfrom):
    pass
else:
    _dfrom =r'/home/yuyang/myfile/data_wenhua'
#每天23点运行
sql="select replace(convert(nvarchar(10),getdate(),120),'-','') as mydate"
res=ms.dict_sql(sql)
date = res[0]['mydate']
#date=20160918
if len(sys.argv)>1:
    date=sys.argv[1]

if len(sys.argv)>2:
    mysymbol=sys.argv[2]
else:
    mysymbol=''
timestart ='0000'
timeend = 2359
print date,mysymbol


targetfile=_dfrom+'\\'+str(date)+'.csv'
if not os.path.isfile(targetfile):
    print "can not find file,and I will create it",targetfile
    newtargetfile=open(targetfile, 'w')
    newtargetfile.close()



downresult=ftp_down(_dfrom,date)# down from ftp

sql="insert into [LogRecord].[dbo].[get_quotes_date](date,result) values('%s',%s)" % (date,downresult)
ms.insert_sql(sql)
#如果成功自动调用补全数据功能，补全所有数据
if downresult==1:
    cmd="python C:\\YYfiles\\evolutionwork\\pythonfile\\fix_quotes_to_dataabse.py %s" % (date)
    os.system(cmd)


