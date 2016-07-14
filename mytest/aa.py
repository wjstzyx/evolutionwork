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

nowD=160805
newesttime=str(nowD+20000000)+" 08:00:00"
newesttime=datetime.datetime.strptime(str(newesttime),"%Y%m%d %H:%M:%S")
print newesttime
