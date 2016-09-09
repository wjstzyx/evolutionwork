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


url = 'http://apis.baidu.com/xiaogg/holiday/holiday?d=20160902'


req = urllib2.Request(url)

req.add_header("apikey", "6677fe3debefda50dd040fbf98d0d38b")

resp = urllib2.urlopen(req)
content = resp.read()
if(content):
    print(content)
