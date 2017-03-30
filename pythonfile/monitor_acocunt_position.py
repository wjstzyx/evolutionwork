#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import pandas as pd
import numpy as np
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")


# 获取收件人名单
def get_messagelist():
	sql="select email from [LogRecord].[dbo].[mailtolist] where istomail=1"
	reslist=ms.find_sql(sql)
	mailtolist=''
	sendmessage=''
	for item in reslist:
		if "@" in item[0]:
			mailtolist=mailtolist+','+item[0]
		else:
			sendmessage=sendmessage+','+item[0]
	mailtolist=mailtolist.strip(',')
	sendmessage=sendmessage.strip(',')
	return mailtolist,sendmessage

import logging
import platform


class MyLog:

    def __init__(self, name):
        self.name = name
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(console_formatter)
        self.log.addHandler(console)

    def set_path(self, path):
        file_name = path + self.name + '.log'
        handler_file = logging.FileHandler(file_name)
        file_formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        handler_file.setFormatter(file_formatter)
        self.log.addHandler(handler_file)

name='test'
log_path='E:\\test\\'
logger = MyLog(name)
logger.set_path(log_path)
log = logger.log
log.info(platform.platform())
log.info('ddd322')
log.info('ddd322')
