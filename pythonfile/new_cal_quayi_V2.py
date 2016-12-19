#coding=utf-8 
#!/usr/bin/env python
import sys

from collections import Counter
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# 返回行情list 或者0

def myround(num):
	if num>=0:
		return round(num)
	if num<=0:
		return round(num+0.000000001)

def input_groupbyquanyi(ac,symbol,quanyisymbol=''):
	if quanyisymbol=='':
		quanyisymbol=symbol
	# 清除临时表
	try:
		sql="drop table #temp_quanyi_new"
		ms.insert_sql(sql)
		sql="drop table #temp_p_log"
		ms.insert_sql(sql)
	except:
		pass
	# 产生临时p_log
	#sql="select * into #temp_p_log from (SELECT   aa.*, sid.Symbol, (YEAR(GETDATE()) - 2000) * 10000 + MONTH(GETDATE()) * 100 + DAY(GETDATE()) AS D from (select  p.AC, p.STOCK, p.type, p.ST, p.P_size, a.ratio from P_BASIC p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.type=a.type and p.AC='%s') as aa inner join Symbol_ID AS sid ON sid.S_ID = aa.STOCK where Symbol='%s') temp" % (ac,symbol)
	sql ="select * into #temp_p_log from (select '%s' as ac,temp1.STOCK,temp1.type,temp1.ST,temp1.P_size as P_size,temp1.ratio,temp1.Symbol,temp1.num from (select p.*,a.ratio,sid.Symbol,isnull(n.num,1)as num from P_BASIC p inner join AC_RATIO a on p.AC=a.AC and p.AC='%s' inner join Symbol_ID  AS sid ON p.STOCK=sid.S_ID left join [LogRecord].[dbo].[Ninone_config] n on n.st=p.st) temp1 where Symbol='%s' )aaa"% (ac,ac,symbol)
	#print sql 
	ms.insert_sql(sql)
	sql="select SUM(p_size*ratio/100*num) as totalsum from #temp_p_log"
	res=ms.dict_sql(sql)
	totalsum=res[0]['totalsum']

	#产生临时整个虚拟组st_report
	sql="select * into  #temp_quanyi_new from ( select p.ac,p.symbol,st_report.type,st_report.id,st_report.p,st_report.pp,p.p_size,p.ratio ,st_report.st,st_report.stockdate from st_report  inner join #temp_p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s')temp " % (ac,symbol)
	#print sql 
	ms.insert_sql(sql)
	#print 1,datetime.datetime.now()
	sql="select count(1) from #temp_quanyi_new"
	res=ms.find_sql(sql)[0][0]
	if res>0:
		#如果有记录才进行
		#初始化每个时刻的仓位为0
		deltepositionlist={}
		sql="SELECT distinct stockdate from #temp_quanyi_new"
		res1=ms.dict_sql(sql)
		for item in res1:
			deltepositionlist[item['stockdate']]=0
		#初始化每个策略的初始位置为0
		laststlistposition={}
		sql="select distinct st from #temp_quanyi_new"
		res1=ms.dict_sql(sql)
		for item in res1:
			laststlistposition[item['st']]=0
		#开始计算每个时刻的仓位
		sql="select (p*p_size*ratio/100) as p,st,stockdate from #temp_quanyi_new  order by stockdate"
		res1=ms.dict_sql(sql)
		for item in res1:
			#赋值laststlistposition
			deltepositionlist[item['stockdate']]=deltepositionlist[item['stockdate']]+(item['p']-laststlistposition[item['st']])
			laststlistposition[item['st']]=item['p']
		#print 2,datetime.datetime.now()
		newlist=[(k,deltepositionlist[k]) for k in sorted(deltepositionlist.keys())]
		#print 3,datetime.datetime.now()
		positionlist=[]
		lastp=0
		for item in newlist:
			temptotal=item[1]+lastp
			lastp=temptotal
			positionlist.append([item[0],item[1],temptotal])
			# [datetime.datetime(2016, 7, 19, 14, 59), -4.0, 0.0]
		#总仓位有部分与现有的不符合，但大多数一致，可以再找个虚拟组测试下
		##print positionlist
		###以上已经准备好虚拟组的仓位信息
		fisrttime=positionlist[0][0]
		#[datetime.datetime(2015, 10, 21, 9, 0), 6.0, 6.0]
		sql="select	C,StockDate from TSymbol_quotes_backup where Symbol='%s' and  stockdate >='%s' order by StockDate " % (quanyisymbol,fisrttime)
		res=ms.dict_sql(sql)
		# print res[:10]
		#对行情日期遍历

		lastquote=res[0]
		mymewquote=[]
		temppositionlist=positionlist[:]
		lastappend=[]
		lastpostiion=temppositionlist[0]
		lastresvalue=res[-1]
		res.append(lastresvalue)
		for item in res:
			StockDate=lastquote['StockDate']
			C=lastquote['C']
			if StockDate.strftime("%Y%m%d")!=item['StockDate'].strftime("%Y%m%d"):
				# print 'StockDate is the last day'
				
				iskeep=1
			else:
				iskeep=0
			lastquote=item
			#--end
			templastposition=[]
			for item1 in temppositionlist:
				if StockDate<=item1[0]:
					#如果行情日期和仓位日期一直，直接插入
					if StockDate==item1[0]:
						temp=[StockDate,C,item1[2]]
						mymewquote.append(temp)
						if StockDate==datetime.datetime(2016, 8, 01, 14, 59):
							print "1--item1",item1,lastpostiion
						lastappend=temp
						lastpostiion=item1


					#如果行情日期小于仓位日期，取前一个仓位的日期
					else:
						temp=[StockDate,C,templastposition[2]]
						if iskeep==1:
							mymewquote.append(temp)
							lastappend=temp
							if StockDate==datetime.datetime(2016, 8, 01, 14, 59):
								print "2--iskeep",iskeep,StockDate
						else:
							if lastappend==[] or lastappend[2]!=temp[2]:
								mymewquote.append(temp)
								if StockDate==datetime.datetime(2016, 8, 01, 14, 59):
									print "3--lastappend",lastappend,templastposition,temp
								lastappend=temp	
						lastpostiion=item1
					break
				templastposition=item1
			if iskeep==1 and StockDate>temppositionlist[-1][0]:
				temp=[StockDate,C,temppositionlist[-1][2]]
				mymewquote.append(temp)
				# lastappend=temp
		#插入当天行情的最后一根bar
		lastClose=res[-1]['C']
		lastdatetime=res[-1]['StockDate']
		lastquoteposition=mymewquote[-1][2]
		if lastdatetime!=mymewquote[-1][0]:
			mymewquote.append([lastdatetime,lastClose,lastquoteposition])
		# for item in positionlist:
		# 	print item[0],item[2]
		# for item in mymewquote:
		# 	print item[0],item[1],item[2] 
		# #分商品和IC  IF 两类	(这个是delta仓位，其实不能去除)
		if 	symbol in ('IC','IF'):
			#去除9:00-9:29分钟的信号
			for item in mymewquote:
				timestr=item[0].strftime("%H%M")
				timestr=int(timestr)
				if timestr>=900 and  timestr<=929:
					mymewquote.remove(item)
			#--end
		##插入数据库
		lastrecordtime=datetime.datetime(2015,01,01,01,00)
		sql="select max(stockdate) as stockdate  from [Future].[dbo].[quanyi_log_groupby_v2] where ac='%s' and symbol='%s'" % (ac,symbol)
		timeinfo=ms.dict_sql(sql)[0]
		if timeinfo['stockdate'] is None:
			lastrecordtime=datetime.datetime(2015,01,01,01,00)
		else:
			lastrecordtime=timeinfo['stockdate']

		insertvalue=""
		numofinsert=0
		for item in mymewquote:
			if item[0]>lastrecordtime:
				insertvalue=insertvalue+","+"('%s','%s',0,%s,'%s',%s,%s)" % (ac,symbol,item[1],item[0],item[2],totalsum)
				numofinsert=numofinsert+1
			if numofinsert>700:
				insertvalue=insertvalue.strip(',')
				sql="insert into [Future].[dbo].[quanyi_log_groupby_v2](ac,symbol,type,ClosePrice,stockdate,totalposition,totalNum) values%s" % insertvalue
				ms.insert_sql(sql)
				numofinsert=0
				insertvalue=""


		if insertvalue !="":
			insertvalue=insertvalue.strip(',')
			sql="insert into [Future].[dbo].[quanyi_log_groupby_v2](ac,symbol,type,ClosePrice,stockdate,totalposition,totalNum) values%s" % insertvalue
			ms.insert_sql(sql)
			# print sql
		##--end
		return mymewquote,totalsum
		
	else:
		return 0,0.0001
		








def cal_quanyi(ac,myquotes,totalsum,symbolto):
	print "start daily"
	import datetime
	atime=datetime.datetime.now()
	todaytime=int(datetime.datetime.now().strftime("%Y%m%d"))-20000000
	#todaytime=160628
	sql="delete from dailyquanyi_V2 where ac='%s' and symbol='%s' and D=%s" % (ac,symbolto,todaytime)
	ms.insert_sql(sql)
	if totalsum<=0:
		totalsum=1000000
	#totalsum=10
	commvalue=1
	pointvalue=1
	sql="SELECT [symbol]  ,[multi] as [pointvalue]  ,[comm] as [commision] FROM [Future].[dbo].[Symbol_ID] where Symbol='%s'" % (symbolto)
	res=ms.dict_sql(sql)
	if res:
		pointvalue=res[0]['pointvalue']
		commvalue=res[0]['commision']

	#直接计算并画图
	tempquotes=myquotes[:]
	avalue=[]
	yvalue=[]
	myindex=[]
	lastC=tempquotes[0][1]
	lastposition=tempquotes[0][2]
	lastdate=tempquotes[0][0]
	totalquanyi=0
	#得到总的需要计算日期的天数
	#dayquanyilist=[quanyi,times,ref(-1)position]
	dayquanyilist={}
	sql="select distinct CONVERT(varchar(10), stockdate, 120 ) as datename from [Future].[dbo].[quanyi_log_groupby_v2] order by datename"
	datelist=ms.dict_sql(sql)
	for item in datelist:
		mytime=item['datename'].replace('-','')
		mytime=str(int(mytime)-20000000)
		dayquanyilist[mytime]=[0,0,0]
	daylists=[k for k in sorted(dayquanyilist.keys())]


	#将总权益分成每天的权益，最后再合成
	for item in tempquotes:
		datetime=item[0]
		D=datetime.strftime('%Y%m%d')
		thisday=str(int(D)-20000000)
		deltatime=abs(myround(item[2])-myround(lastposition))
		totalquanyi=(myround(lastposition)*(item[1]-lastC)*float(pointvalue)-deltatime*commvalue)/round(totalsum,3)+totalquanyi
		deltaquanyi=(myround(lastposition)*(item[1]-lastC)*float(pointvalue)-deltatime*commvalue)/round(totalsum,3)
		lastposition=item[2]
		lastC=item[1]
		dayquanyilist[thisday][0]=dayquanyilist[thisday][0]+deltaquanyi
		dayquanyilist[thisday][1]=dayquanyilist[thisday][1]+deltatime
		dayquanyilist[thisday][2]=myround(lastposition)

	####写入数据库
	newlist=[[k,dayquanyilist[k]] for k in sorted(dayquanyilist.keys())]

	tempmyquanyi=0
	for item  in newlist:
		tempmyquanyi=tempmyquanyi+item[1][0]
		item[1][0]=tempmyquanyi
	# for item in newlist:
	# 	print item 



	sql="select MAX(D)  as D from [Future].[dbo].[dailyquanyi_V2] where ac='%s' and Symbol='%s'" % (ac,symbolto)
	datelist=ms.dict_sql(sql)[0]
	if datelist['D'] is None:
		lastrecordday=150101
	else:
		lastrecordday=datelist['D']
	for item in newlist:
		position=item[1][2]
		lastdayquanyi=item[1][0]
		changeD=item[0]
		times=item[1][1]
		if changeD>lastrecordday:
			sql="insert into dailyquanyi_V2(ac,symbol,position,quanyi,D,totalnum,times) values('%s','%s',%s,%s,%s,%s,%s)" % (ac,symbolto,myround(position),lastdayquanyi,changeD,totalsum,times)
			ms.insert_sql(sql)

	##--end



	








def cal_quanyi_foraccount(ac,myquotes,totalsum,symbolto,ratio):
	if totalsum<=0:
		totalsum=1000000
	#totalsum=10
	commvalue=1
	pointvalue=1
	sql="SELECT [symbol]  ,[multi] as [pointvalue]  ,[comm] as [commision] FROM [Future].[dbo].[Symbol_ID] where Symbol='%s'" % (symbolto)
	res=ms.dict_sql(sql)
	if res:
		pointvalue=res[0]['pointvalue']
		commvalue=res[0]['commision']

	#直接计算
	tempquotes=myquotes[:]
	avalue=[]
	yvalue=[]
	myindex=[]
	lastC=tempquotes[0][1]
	lastposition=tempquotes[0][2]
	lastdate=tempquotes[0][0]
	totalquanyi=0
	i=0
	totalchangetime=0
	oneacquanyidict={}

	for item in tempquotes:
		datetime=item[0]
		deltatime=abs(myround(item[2])-myround(lastposition))
		totalchangetime=totalchangetime+deltatime
		totalquanyi=(myround(lastposition)*(item[1]-lastC)*float(pointvalue)-deltatime*commvalue)/totalsum*ratio +totalquanyi
		lastposition=item[2]
		lastC=item[1]
		myindex.append(i)
		i=i+1
		avalue.append(datetime)
		yvalue.append(totalquanyi)
		oneacquanyidict[datetime]=totalquanyi
	return oneacquanyidict

def add_acquanyi(acquanyi1,acquanyi2):
	newquanyi=dict(Counter(acquanyi1)+Counter(acquanyi2))
	alltime=[ k for k in sorted(newquanyi.keys())]
	allquanyi=[]
	acquanyi1keys=acquanyi1.keys()
	acquanyi2keys=acquanyi2.keys()
	acquanyi1value=0
	acquanyi2value=0
	for item in alltime:
		if item in acquanyi1keys:
			acquanyi1value=acquanyi1[item]
			lastvalue=acquanyi2value+acquanyi1value
			allquanyi.append(lastvalue)
		else:
			if item in acquanyi2keys:
				acquanyi2value=acquanyi2[item]
				lastvalue=acquanyi2value+acquanyi1value
				allquanyi.append(lastvalue)
			else:
				allquanyi.append(lastvalue)
	#print dict(zip(alltime,allquanyi))
	return dict(zip(alltime,allquanyi))



def show_account(accountname):
	sql="select ac,ratio,symbol from [Future].[dbo].[backtest_account_ac] where [accountname]='%s'" % (accountname)
	res=ms.dict_sql(sql)
	myqanyi=[]
	mydatetime=[]
	totalquanyidict={}
	sql="select sum(ratio) as ratio from [Future].[dbo].[backtest_account_ac] where [accountname]='%s'" % (accountname)
	i=ms.dict_sql(sql)[0]['ratio']
	for item in res:
		ratio=item['ratio']
		ac=item['ac']
		symbol=item['symbol']
		(myquotes,totalsum)=input_groupbyquanyi(ac,symbol)
		oneacquanyidict=cal_quanyi_foraccount(ac,myquotes,totalsum,symbol,ratio)
		#totalquanyidict=dict(Counter(totalquanyidict)+Counter(oneacquanyidict))
		totalquanyidict=add_acquanyi(totalquanyidict,oneacquanyidict)
	#totalquanyidict对此排序
	temptotalquanyidict=[(k,totalquanyidict[k]) for k in sorted(totalquanyidict.keys())]
	avalue=[]
	yvalue=[]
	myindex=[]
	indexnum=0
	#最大回撤相关
	lasthighquanyi=0
	lasthighhuiche=0
	nowhuiche=0
	if i==0:
		i=1
	for item in temptotalquanyidict:
		itemquanyi=item[1]/i
		avalue.append(item[0])
		yvalue.append(itemquanyi)
		myindex.append(indexnum)
		indexnum=indexnum+1
		#计算回撤相关
		nowhuiche=lasthighquanyi-itemquanyi
		if itemquanyi>lasthighquanyi:
			lasthighquanyi=itemquanyi
		if nowhuiche>lasthighhuiche:
			lasthighhuiche=nowhuiche
		##--end
	if lasthighhuiche<0:
		lasthighhuiche=0
	#开始画图
	# print myindex
	# print yvalue
	plt.figure(figsize=(16,8))
	lenx=len(avalue)
	pl.plot(myindex, yvalue, 'r') 	 
	pl.subplots_adjust(bottom=0.3) 	 
	ax = pl.gca() 
	ax.fmt_xdata = pl.DateFormatter('%Y-%m-%d') 
	pl.xticks(rotation=75) 	 
	#生成x轴的间隔
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
	plt.title('%s--MaxDrawDown:%s' % (accountname,int(lasthighhuiche)))
	#plt.ylabel(u'平均每手净收益',fontproperties='SimHei')
	plt.ylabel(u'Profit Per Hand')
	pl.savefig('..\\myimage\\%s' % (accountname))
	pl.show() 


#只针对同一种商品的账户权益
def real_account_groupbyquanyi(ac,symbol):
	# 清除临时表
	try:
		sql="drop table #temp_quanyi_new"
		ms.insert_sql(sql)
		sql="drop table #temp_p_log"
		ms.insert_sql(sql)
	except:
		pass
	# 产生临时p_log
	#sql="select * into #temp_p_log from (SELECT   aa.*, sid.Symbol, (YEAR(GETDATE()) - 2000) * 10000 + MONTH(GETDATE()) * 100 + DAY(GETDATE()) AS D from (select  p.AC, p.STOCK, p.type, p.ST, p.P_size, a.ratio from P_BASIC p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.type=a.type and p.AC='%s') as aa inner join Symbol_ID AS sid ON sid.S_ID = aa.STOCK where Symbol='%s') temp" % (ac,symbol)
	sql ="select * into #temp_p_log from (select '%s' as ac,temp1.STOCK,temp1.type,temp1.ST,temp1.P_size*f.ratio/100 as P_size,temp1.ratio,temp1.Symbol,temp1.num from (select p.*,a.ratio,sid.Symbol,isnull(n.num,1)as num from P_BASIC p inner join AC_RATIO a on p.AC=a.AC inner join Symbol_ID AS sid ON p.STOCK=sid.S_ID left join [LogRecord].[dbo].[Ninone_config] n on n.st=p.st ) temp1 inner join p_follow f on temp1.AC=f.F_ac and f.AC='%s' and f.ratio<>0 where P_size<>0  and Symbol='%s')aaa" % (ac,ac,symbol)

	#print sql
	ms.insert_sql(sql)
	sql="select SUM(p_size*ratio/100*num) as totalsum from #temp_p_log"
	res=ms.dict_sql(sql)
	totalsum=res[0]['totalsum']

	#产生临时整个虚拟组st_report
	sql="select * into  #temp_quanyi_new from ( select p.ac,p.symbol,st_report.type,st_report.id,st_report.p,st_report.pp,p.p_size,p.ratio ,st_report.st,st_report.stockdate from st_report  inner join #temp_p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s')temp " % (ac,symbol)
	#print sql
	ms.insert_sql(sql)
	#print 1,datetime.datetime.now()
	sql="select count(1) from #temp_quanyi_new"
	res=ms.find_sql(sql)[0][0]
	if res>0:
		#如果有记录才进行
		#初始化每个时刻的仓位为0
		deltepositionlist={}
		sql="SELECT distinct stockdate from #temp_quanyi_new"
		res1=ms.dict_sql(sql)
		for item in res1:
			deltepositionlist[item['stockdate']]=0
		#初始化每个策略的初始位置为0
		laststlistposition={}
		sql="select distinct st from #temp_quanyi_new"
		res1=ms.dict_sql(sql)
		for item in res1:
			laststlistposition[item['st']]=0
		#开始计算每个时刻的仓位
		sql="select (p*p_size*ratio/100) as p,st,stockdate from #temp_quanyi_new  order by stockdate"
		res1=ms.dict_sql(sql)
		for item in res1:
			#赋值laststlistposition
			deltepositionlist[item['stockdate']]=deltepositionlist[item['stockdate']]+(item['p']-laststlistposition[item['st']])
			laststlistposition[item['st']]=item['p']
		#print 2,datetime.datetime.now()
		newlist=[(k,deltepositionlist[k]) for k in sorted(deltepositionlist.keys())]
		#print 3,datetime.datetime.now()
		positionlist=[]
		lastp=0
		for item in newlist:
			temptotal=item[1]+lastp
			lastp=temptotal
			positionlist.append([item[0],item[1],temptotal])
			# [datetime.datetime(2016, 7, 19, 14, 59), -4.0, 0.0]
		#总仓位有部分与现有的不符合，但大多数一致，可以再找个虚拟组测试下
		##print positionlist
		###以上已经准备好虚拟组的仓位信息
		fisrttime=positionlist[0][0]
		#[datetime.datetime(2015, 10, 21, 9, 0), 6.0, 6.0]
		sql="select	C,StockDate from TSymbol_quotes_backup where Symbol='%s' and  stockdate >='%s' order by StockDate " % (symbol,fisrttime)
		res=ms.dict_sql(sql)
		# print res[:10]
		#对行情日期遍历

		lastquote=res[0]
		mymewquote=[]
		temppositionlist=positionlist[:]
		lastappend=[]
		lastpostiion=temppositionlist[0]
		lastresvalue=res[-1]
		res.append(lastresvalue)
		for item in res:
			StockDate=lastquote['StockDate']
			C=lastquote['C']
			if StockDate.strftime("%Y%m%d")!=item['StockDate'].strftime("%Y%m%d"):
				# print 'StockDate is the last day'
				# print 'StockDate',StockDate
				iskeep=1
			else:
				iskeep=0
			lastquote=item
			#--end
			templastposition=[]
			for item1 in temppositionlist:
				if StockDate<=item1[0]:
					#如果行情日期和仓位日期一直，直接插入
					if StockDate==item1[0]:
						temp=[StockDate,C,item1[2]]
						mymewquote.append(temp)
						if StockDate==datetime.datetime(2015, 10, 21, 9, 5):
							print "1--item1",item1,lastpostiion
						lastappend=temp
						lastpostiion=item1


					#如果行情日期小于仓位日期，取前一个仓位的日期
					else:
						temp=[StockDate,C,templastposition[2]]
						if iskeep==1:
							mymewquote.append(temp)
							lastappend=temp
							if StockDate==datetime.datetime(2015, 10, 21, 9, 5):
								print "2--iskeep",iskeep,StockDate
						else:
							if lastappend==[] or lastappend[2]!=temp[2]:
								mymewquote.append(temp)
								if StockDate==datetime.datetime(2015, 10, 21, 9, 5):
									print "3--lastappend",lastappend,templastposition,temp
								lastappend=temp	
						lastpostiion=item1
					break

				templastposition=item1

		# for item in positionlist:
		# 	print item[0],item[2]
		# for item in mymewquote:
		# 	print item[0],item[1],item[2] 
		# #分商品和IC  IF 两类	(这个是delta仓位，其实不能去除)
		if 	symbol in ('IC','IF'):
			#去除9:00-9:29分钟的信号
			for item in mymewquote:
				timestr=item[0].strftime("%H%M")
				timestr=int(timestr)
				if timestr>=900 and  timestr<=929:
					mymewquote.remove(item)
			#--end
		return mymewquote,totalsum
	else:
		return 0,0.0001










				










			





	# newesttime=str(nowD+20000000)+" 08:00:00"
	# newesttime=datetime.datetime.strptime(str(newesttime),"%Y%m%d %H:%M:%S")
	# sql="delete from dayp_quanyi_log_groupby where ac='%s' and symbol='%s' and type=%s and stockdate>'%s'" % (ac,symbol,type,newesttime)
	# ms.insert_sql(sql)
	#--end





# (myquotes,totalsum)=input_groupbyquanyi('RBQGSTREVYP_TG','RBnight','RBnight')
# for item in myquotes:
# 	print item 
# cal_quanyi('RBQGYP_TG',myquotes,totalsum,'RBnight')

# show_account('myaccount2')


def write_heart(type,name):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	sql="update [LogRecord].[dbo].[quotes_python_heart] set [updatetime]=getdate() where type='%s' and name='%s' and [isactive]=1" % (type,name)
	ms.insert_sql(sql)



def main_fun_sumps():
	#获取需要处理的列表
	sql="SELECT id, [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where iscaculate=1 and issumps=1 and isyepan in (0,1,12) order by id desc "
	#sql="SELECT top 17 id,[acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isforbacktest]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RB') and iscaculate=1 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		print item['acname'],item['id']
		positionsymbol=item['positionsymbol']
		quanyisymbol=item['quanyisymbol']
		(myquotes,totalsum)=input_groupbyquanyi(item['acname'],positionsymbol,quanyisymbol)
		# print 'myquotes',myquotes
		#直接设置数字 10
		cal_quanyi(item['acname'],myquotes,10,quanyisymbol)

def main_fun():
	#获取需要处理的列表
	#sql="SELECT TOP 1000 [id]      ,[acname]      ,[positionsymbol]      ,[quanyisymbol]      ,[iscaculate]      ,[isforhistory]      ,[isstatistic]      ,[isyepan]      ,[iscalcubyvick]      ,[sortnum]      ,[issumps]  FROM [LogRecord].[dbo].[quanyicaculatelist] where [positionsymbol]<>[quanyisymbol]  order by id desc"


	sql="SELECT id, [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where iscaculate=1 and issumps=0 and isyepan in (0,1,12)  AND quanyisymbol not in ('IF','IC','IH') order by id desc "
	#sql="SELECT id, [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where iscaculate=1 and issumps=0 and isyepan in (0,1,12)  and id<=715 order by id desc "
	#sql="SELECT top 17 id,[acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isforbacktest]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RB') and iscaculate=1 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		print item['acname'],item['id']
		positionsymbol=item['positionsymbol']
		quanyisymbol=item['quanyisymbol']
		(myquotes,totalsum)=input_groupbyquanyi(item['acname'],positionsymbol,quanyisymbol)
		# print 'myquotes',myquotes
		#直接设置数字 10
		cal_quanyi(item['acname'],myquotes,totalsum,quanyisymbol)





def test_is_ok():
	sql=""


main_fun()
main_fun_sumps()

write_heart('daily_equity','nosum1')