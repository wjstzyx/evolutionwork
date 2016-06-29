#coding=utf-8 
#!/usr/bin/env python
import sys
import time
import datetime
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
D=160628
myDbegin=str(D+20000000)
myDbegin=datetime.datetime.strptime(myDbegin,'%Y%m%d')
myDbegin=myDbegin+datetime.timedelta(minutes=1260)
myDend=myDbegin+datetime.timedelta(hours=6)
print myDbegin,myDend
todaytime=datetime.datetime.now().strftime("%Y-%m-%d")
todaytime=datetime.datetime.strptime(todaytime,"%Y-%m-%d")
deltime=todaytime+datetime.timedelta(hours=8)
print todaytime
print deltime