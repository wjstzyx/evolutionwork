import csv
import datetime
from dbconn import MSSQL
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")

def import_date():
	path=r'C:\Users\YuYang\Desktop\getADTMfisher1.csv'
	f=open(path,'r')
	aaa=f.readlines()
	for item in aaa[1:]:
		item=item.split(',')
		timea=item[1]
		timea=datetime.datetime.strptime(timea,'%Y/%m/%d %H:%M:%S')
		symbol=item[0]
		profit_diff=item[-2]
		gross_profit=item[-3]
		sql="insert into [LogRecord].[dbo].[test_profit](symbol,[atime],[profit_diff],[totalprofit]) values('%s','%s','%s','%s')"% (symbol,timea,profit_diff,gross_profit)
		try:
			ms.insert_sql(sql)
		except:
			print item


def plt_pic(valueres,ac):
	avalue=[]
	yvalue=[]
	i=0
	myindex=[]
	for item in valueres:
		avalue.append(item[0])
		yvalue.append(item[1])
		myindex.append(i)
		i=i+1
	plt.figure(figsize=(16,8))
	lenx=len(avalue)
	pl.plot(myindex, yvalue, 'r') 
	 
	pl.subplots_adjust(bottom=0.3) 	 
	ax = pl.gca() 
	ax.fmt_xdata = pl.DateFormatter('%Y-%m-%d') 
	pl.xticks(rotation=75)
	aa=int(lenx/30)
	numx=[]
	labvalue=[]
	for i in range(0,lenx-aa,aa):
		numx.append(i)
		labvalue.append(avalue[i].strftime("%Y-%m-%d"))
	numx.append(myindex[-1])
	labvalue.append(avalue[myindex[-1]].strftime("%Y-%m-%d"))
	pl.xticks(numx, labvalue) 
	pl.grid()
	plt.title('')
	plt.ylabel(u'aaa',fontproperties='SimHei')
	pl.savefig('..\\myimage\\%s' % (ac))
	# if isshow==1:
	# 	pl.show(


def sum_profit():
	sql="select distinct symbol from [LogRecord].[dbo].[test_profit] order by symbol"
	symboldict=ms.dict_sql(sql)
	totalquanyi=[]
	i=1
	for item in symboldict:
		sql="SELECT [atime]    ,[totalprofit] FROM [LogRecord].[dbo].[test_profit] where Symbol='%s' order by atime" % (item['symbol'])
		res=ms.find_sql(sql)
		plt_pic(res,item['symbol'])
		# totalquanyi=add_time_series(totalquanyi,res)
		# print i
		# i=i+1
	# print 'totalquanyi',totalquanyi[0:10]
	# for item in totalquanyi:
	# 	print item[1]




# datalist1=[(date,value)]


def add_time_series(totalquanyi,res1):
	totalquanyitime=[k[0] for k in totalquanyi]
	res1time=[k[0] for k in res1]
	totalquanyidict={}
	for item in totalquanyi:
		totalquanyidict[item[0]]=item[1]
	res1dict={}
	for item in res1:
		res1dict[item[0]]=item[1]
	daylist=list(set(totalquanyitime).union(set(res1time)))
	daylist=sorted(daylist)
	totalquanyilastvalue=0
	res1lastvalues=0
	result={}
	for item in daylist:
		tempvalue=0
		if item in totalquanyitime:
			totalquanyilastvalue=totalquanyidict[item]
		if item in res1time:
			res1lastvalues=res1dict[item]
		tempvalue=float(totalquanyilastvalue)+float(res1lastvalues)
		result[item]=tempvalue
	result=sorted(result.iteritems(), key=lambda d:d[1], reverse = False)
	return result
# sum_profit()


def plt_pic(valueres,ac):
	avalue=[]
	yvalue=[]
	for item in valueres:
		avalue.append(item[0])
		yvalue.append(item[1])
	plt.figure(figsize=(16,8))
	lenx=len(avalue)
	pl.plot(myindex, yvalue, 'r') 
	 
	pl.subplots_adjust(bottom=0.3) 	 
	ax = pl.gca() 
	ax.fmt_xdata = pl.DateFormatter('%Y-%m-%d') 
	pl.xticks(rotation=75)
	aa=int(lenx/30)
	numx=[]
	labvalue=[]
	for i in range(0,lenx-aa,aa):
		numx.append(i)
		labvalue.append(avalue[i].strftime("%Y-%m-%d"))
	numx.append(myindex[-1])
	labvalue.append(avalue[myindex[-1]].strftime("%Y-%m-%d"))
	pl.xticks(numx, labvalue) 
	pl.grid()
	plt.title('')
	plt.ylabel(u'aaa',fontproperties='SimHei')
	pl.savefig('..\\myimage\\%s' % (ac))
	# if isshow==1:
	# 	pl.show()

def shou_account_position():
	sql="select distinct userid from [LogRecord].[dbo].[account_position] order by userid"
	res=ms.dict_sql(sql)
	totalsql=""
	for item in res:
		userid=item['userid']
		tempsql="select '%s' as [userID],STOCK as [stockID],Expr1 as position,GETDATE() as nowtime from future.dbo.view_%s" % (userid,userid)
		totalsql=totalsql+" union all "+tempsql
	totalsql=totalsql.strip(" union all ")
	print totalsql

shou_account_position()