#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
import csv
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList


def cache_into_trading_logtrade():
	sql="select p,stock,st,systemtime from [Trading_logSymbol] where systemtime>='2016-06-12'"
	res=ms.dict_sql(sql)
	for item in res:
		sql="SELECT top 1 id,p,st  FROM [LogRecord].[dbo].[Trading_logTrade] WHERE ST = %s  order by systemtime desc " % (item['st'])
		res1=ms.dict_sql(sql)
		if res1:
			if item['p'] != res1[0]['p']:
				sql="insert into [LogRecord].[dbo].[trading_logtrade] (p,stock,st,systemtime) values(%s,'%s',%s,'%s')" % (item['p'],item['stock'],item['st'],item['systemtime'])
				ms.insert_sql(sql)
		else:
			sql="insert into [LogRecord].[dbo].[trading_logtrade] (p,stock,st,systemtime) values(%s,'%s',%s,'%s')" % (item['p'],item['stock'],item['st'],item['systemtime'])
			ms.insert_sql(sql)


filepath="C:\YYfiles\cachesigfiles"
timestamp=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
def cache_sig_tocsv():
	sql="select p,stock,st,systemtime from [Trading_logSymbol] where systemtime>='2016-06-12'"
	res=ms.find_sql(sql)
	timestamp=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	filename=filepath+'\st_'+timestamp+'.csv'
	csvfile = file(filename, 'wb')
	writer = csv.writer(csvfile)
	writer.writerows(res)
	csvfile.close()
	sql="insert into [LogRecord].[dbo].[readcsvlist](path,filename,type,isdone,inserttime) values('%s','%s','%s',%s,getdate())" % (filepath,'st_'+timestamp+'.csv','strategy',0)
	ms.insert_sql(sql)



def read_csv_into_database():
	sql="select * from [LogRecord].[dbo].[readcsvlist] where isdone=0 order by id"
	res=ms.dict_sql(sql)
	for item in res:
		filename=item['path']+'\\'+item['filename']
		csvfile = file(filename,'rb')
		reader = csv.reader(csvfile)
		for line in reader:
			print line
			p=line[0]
			st=line[2]
			stockdate=line[3]
			D=stockdate[2:4]+stockdate[5:7]+stockdate[8:10]
			T=stockdate[11:13]+stockdate[14:16]+stockdate[17:19]
			try:
				sql="insert into [myst_report](p,st,D,T,stockdate) values(%s,%s,%s,%s,'%s')" % (p,st,D,T,stockdate)
				ms.insert_sql(sql)
			except:
				pass

		csvfile.close()
		sql="update [LogRecord].[dbo].[readcsvlist] set isdone=1 where id=%s" % (item['id'])
		ms.insert_sql(sql)





# cache_sig_tocsv()
read_csv_into_database()

# cache_into_trading_logtrade()

# while(1):
# 	cache_into_trading_logtrade()