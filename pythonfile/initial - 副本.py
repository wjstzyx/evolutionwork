#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

import socket
outIP = socket.gethostbyname(socket.gethostname())#这个得到本地ip
ipList = socket.gethostbyname_ex(socket.gethostname())
computername=ipList[0]
iplist=ipList[2]
localIP=""
for item in iplist:
	if item !=outIP:
		localIP=item
print computername
print localIP
print outIP

