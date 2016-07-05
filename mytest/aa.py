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
a='160828'
stockdate='2016-06-28 00:00:00'
stockdate=datetime.datetime.strptime(stockdate,'%Y-%m-%d %H:%M:%S')
def count_words(s, n):
    """Return the n most frequently occuring words in s."""
    
    # TODO: Count the number of occurences of each word in s
    slist=s.split(" ")
    mylist={}
    sset=set(slist)
    for item in sset:
        mylist[item]=0
    for item in slist:
        mylist[item]=mylist[item]+1
    mylist=[(k,mylist[k]) for k in mylist.keys()]
    return mylist
L = [('d',2),('dd',4),('b',4),('c',2)]
print L.sort(key=lambda x:(x[1],x[0]))
print L

def mycmp(a,b):
	if a[0]>=b[0] and a[1]<=b[1]:
		return 1
	else:
		return -1

L.sort(cmp=mycmp)
print L

