#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import shutil
import time
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

root=r'E:\test'
source=r'E:\test\aaa\ccc'
target=r'E:/test/bbb'

shutil.rmtree(target)
time.sleep(0.5)

shutil.copytree(source, target)
