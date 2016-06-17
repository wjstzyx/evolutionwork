#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def testquanyi():
	sql="select distinct ac,symbol from [Future].[dbo].[real_quanyi_log_groupby]"
	res=ms.dict_sql(sql)
	isss=0
	for iitem in res:
		ac=iitem['ac']
		symbol=iitem['symbol']
		sql="select * from [Future].[dbo].[real_quanyi_log_groupby] where ac='%s' and symbol='%s' order by stockdate" %(ac,symbol)
		print sql
		res1=ms.dict_sql(sql)
		lastposition=res1[0]['totalposition']
		for item in res1[1:]:
			position=item['position']
			totalposition=item['totalposition']
			if abs(totalposition-position-lastposition)>0.00001:
				print item['stockdate']
				print (position+lastposition)
				print totalposition
				isss=1
			lastposition=totalposition
		if isss==1:
			break

testquanyi()