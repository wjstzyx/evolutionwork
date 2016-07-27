# -*- coding: gb18030 -*- 
import string, os
import shutil
from dbconn import MSSQL
from collections import Counter
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


a=[3,4,4,5,6]
b=[4,5,6,7,7,8]
print list(set(a).union(set(b)))
x = {}
y = { 'banana': 10, 'pear': 11 }
x=dict(Counter(x)+Counter(y))
print x
aa=x.keys()
if 'banana' in aa:
	print 222
else:
	print 222222
