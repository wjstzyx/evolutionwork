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
mynewD=str(D+20000000)


todaytime=datetime.datetime.now().strftime("%Y-%m-%d")
todaytime=int(datetime.datetime.now().strftime("%Y%m%d"))-20000000
print todaytime
acname='YEQGOT'
symbol='IF'
sql="select distinct ac,symbol from dailyquanyi where symbol='IF' and D>151020  and ac='YEQGOT' order by ac"
res=ms.dict_sql(sql)
for item in res:
	acname=item['ac']
	symbol=item['symbol']
	sql="select D,(quanyi-comm)/d_max as quanyia from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
	res1=ms.find_sql(sql)
	sql="select D,(quanyi-comm)/d_max as quanyia from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
	res2=ms.find_sql(sql)		
	nesres1=[]
	for item in res1:
		D=int(item[0])+20000000
		D1=str(D)[0:4]
		D2=str(D)[4:6]
		D3=str(D)[6:8]		
		tmp=[int(D1),int(D2),int(D3),item[1]]
		print tmp
		nesres1.append(tmp)



	print nesres1