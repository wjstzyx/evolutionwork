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
###function
account='account11'
sql="select * from [LogRecord].[dbo].[order_p_follow]  where ac=F_ac and ac='%s'" % (account)
res=ms.dict_sql(sql)
print res 