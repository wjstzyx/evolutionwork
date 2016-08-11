# -*- coding: utf-8 -*- 
import string, os
import csv
import time
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
aa=datetime.datetime(2016,8,9,22,24,20)
bb=datetime.datetime(2016,8,9,22,24,16,997000)
print aa
print bb
print aa.hour




