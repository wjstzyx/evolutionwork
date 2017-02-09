#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime
import time 
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

global lilun_total
global real_total
step_acname='StepMultigaosheng1'
account='1636737'
equity_day='2017-02-09'

def change_scatter_tocontinue(datalist,delta=60):
	newdatalist=[]
	newdatalist.append(datalist[0][:])
	lastdate=datalist[0][:]
	for item in datalist[1:]:
		while (item[0]-lastdate[0])>60:
			lastdate[0]=lastdate[0]+60
			newdatalist.append([lastdate[0],lastdate[1]])
		newdatalist.append(item)
		lastdate=item[:]
	return newdatalist


begintime='2017-02-05'
endtime='2017-02-09 16:00:00'

lilun_total=[]
real_total=[]
	# for totalitem in totalres:
	# 	p_followac=totalitem['F_ac']
	# 	ratio=totalitem['ratio']/100.0	

def cal_ac_day_equity(p_followac,acname,ratio=1):
	sql="select q.ClosePrice,q.stockdate,round(q.totalposition*mr.ratio*%s,0) as totalposition ,q.symbol,sid.S_ID from p_follow p inner join quanyi_log_groupby_v2 q on p.F_ac=q.AC and p.AC='%s' inner join LogRecord.dbo.test_margin mr on q.symbol=mr.symbol inner join symbol_id sid on q.symbol=sid.Symbol where q.AC='%s' and stockdate>='%s' and stockdate<='%s' order by stockdate" % (ratio,p_followac,acname,begintime,endtime)
	res1=ms.dict_sql(sql)
	#compute commvalue  pointvalue
	symbolto=res1[0]['symbol']
	commvalue=1
	pointvalue=1
	sql="SELECT [symbol]  ,[multi] as [pointvalue]  ,[comm] as [commision] FROM [Future].[dbo].[Symbol_ID] where Symbol='%s'" % (symbolto)
	res=ms.dict_sql(sql)
	if res:
		pointvalue=res[0]['pointvalue']
		commvalue=res[0]['commision']
	#print pointvalue,commvalue
	##############################

	#compute every stockdate delta_equity
	lastposition=res1[0]['totalposition']
	lastclose=res1[0]['ClosePrice']
	totalequity={}
	for item in res1:
		#print item['stockdate'],item['ClosePrice'],item['totalposition']
		deltatime=abs(item['totalposition']-lastposition)
		deltaquanyi=(lastposition*(item['ClosePrice']-lastclose)*float(pointvalue)-deltatime*commvalue)
		lastposition=item['totalposition']
		lastclose=item['ClosePrice']
		totalequity[item['stockdate']]=deltaquanyi
	dictlist=sorted(totalequity.iteritems(),key=lambda d:d[0],reverse=False)
	cal_day=dictlist[-1][0].strftime('%Y%m%d')
	lastdaytime=datetime.datetime.strptime(cal_day+" 08:00:00",'%Y%m%d %H:%M:%S')

	lastday_equity=0
	for item in dictlist:
		if item[0]>lastdaytime:
			lastday_equity=lastday_equity+item[1]
	lilun_total.append(lastday_equity)
	print cal_day,acname,lastday_equity






def cal_ac_day_equity_real(account,symbolid,symbol):
	realstokid=symbolid
	realaccount=account
	#sql="select t.Symbol,t.C as ClosePrice,t.StockDate as stockdate,a.totalposition from TSymbol_allfuture t inner join  symbol_id sid on t.Symbol=sid.Symbol and len(sid.symbol)<3 inner join (SELECT convert(nvarchar(16),[inserttime],120)+':00' as stockdate ,[longhave]-[shorthave] as totalposition FROM [LogRecord].[dbo].[account_position] where userid='%s'   and inserttime<='%s' and inserttime>='%s' and stockid=%s )a on t.StockDate=a.stockdate and sid.S_ID=%s order by a.stockdate" % (realaccount,endtime,begintime,realstokid,realstokid)

	sql="select t.StockDate as stockdate,0 as delta,a.totalposition from TSymbol_allfuture t inner join  symbol_id sid on t.Symbol=sid.Symbol and len(sid.symbol)<3 inner join (SELECT convert(nvarchar(16),[inserttime],120)+':00' as stockdate ,[longhave]-[shorthave] as totalposition FROM [LogRecord].[dbo].[account_position] where userid='%s'   and inserttime<='%s' and inserttime>='%s' and stockid=%s )a on t.StockDate=a.stockdate and sid.S_ID=%s order by a.stockdate" % (realaccount,endtime,begintime,realstokid,realstokid)	
	res2=ms.find_sql(sql)
	if res2:
		# merge with Tsymbol_allfuture stockdate
		positionlist=res2
		fisrttime=positionlist[0][0]
		#[datetime.datetime(2015, 10, 21, 9, 0), 6.0, 6.0]
		sql="select	C,StockDate from TSymbol_allfuture where Symbol='%s' and  stockdate >='%s' and stockdate<='%s' order by StockDate " % (symbol,begintime,endtime)
		res=ms.dict_sql(sql)
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
			templastposition=[0,0,0]
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
		# for item in mymewquote:
		# 	print item 

	########################################
		#compute commvalue  pointvalue
		symbolto=symbol
		commvalue=1
		pointvalue=1
		sql="SELECT [symbol]  ,[multi] as [pointvalue]  ,[comm] as [commision] FROM [Future].[dbo].[Symbol_ID] where Symbol='%s'" % (symbolto)
		res=ms.dict_sql(sql)
		if res:
			pointvalue=res[0]['pointvalue']
			commvalue=res[0]['commision']
		##############################

		#compute every stockdate delta_equity
		lastposition=mymewquote[0][2]
		lastclose=mymewquote[0][1]
		totalequity={}
		for item in mymewquote:
			#print item[0],item[1],item[2]
			deltatime=abs(item[2]-lastposition)
			deltaquanyi=(lastposition*(item[1]-lastclose)*float(pointvalue)-deltatime*commvalue)
			lastposition=item[2]
			lastclose=item[1]
			totalequity[item[0]]=deltaquanyi
		dictlist=sorted(totalequity.iteritems(),key=lambda d:d[0],reverse=False)
		cal_day=dictlist[-1][0].strftime('%Y%m%d')
		lastdayendtime=datetime.datetime.strptime(cal_day+" 15:00:00",'%Y%m%d %H:%M:%S')
		lastdaybegintime=lastdayendtime-datetime.timedelta(hours=18)
		#lastdaytime=datetime.datetime.strptime(cal_day+" 08:00:00",'%Y%m%d %H:%M:%S')

		lastday_equity=0
		for item in dictlist:
			if item[0]>=lastdaybegintime:
				lastday_equity=lastday_equity+item[1]
		print cal_day,symbolto,lastday_equity
	else:
		lastday_equity=0
		print 'notexit',symbol,lastday_equity
	real_total.append(lastday_equity)

def cal_ac_day_equity_real_new(account,symbolid,symbol):
	realstokid=symbolid
	realaccount=account
	sql="SELECT convert(datetime,convert(nvarchar(16),[inserttime],120)+':00',120) as stockdate ,[longhave]-[shorthave] as totalposition FROM [LogRecord].[dbo].[account_position] where userid='666061010'   and inserttime<='2017-02-08 16:00:00' and inserttime>='2017-02-05' and stockid=20 order by stockdate "
	res2=ms.find_sql(sql)
	# add every day last bar
	#ger every day last bar
	sql="select distinct  CONVERT(nvarchar(10),stockdate,120) as day from TSymbol_allfuture where symbol='CF' and stockdate<='2017-02-08 16:00:00' and stockdate>='2017-02-05'  order by day"
	daylist=ms.find_sql(sql)
	maxstockdatelist=[]
	for item in daylist:
		sql="select max(stockdate) as stockdate from TSymbol_allfuture where symbol='CF' and stockdate<='%s 15:31:00'" % (item)
		temp1=ms.find_sql(sql)
		maxstockdatelist.append(temp1[0][0])
	print  maxstockdatelist





	sql="select t.Symbol,t.C as ClosePrice,t.StockDate as stockdate,a.totalposition from TSymbol_allfuture t inner join  symbol_id sid on t.Symbol=sid.Symbol and len(sid.symbol)<3 inner join (SELECT convert(nvarchar(16),[inserttime],120)+':00' as stockdate ,[longhave]-[shorthave] as totalposition FROM [LogRecord].[dbo].[account_position] where userid='%s'   and inserttime<='%s' and inserttime>='%s' and stockid=%s )a on t.StockDate=a.stockdate and sid.S_ID=%s order by a.stockdate" % (realaccount,endtime,begintime,realstokid,realstokid)
	sql="select t.StockDate as stockdate,0 as delta,a.totalposition from TSymbol_allfuture t inner join  symbol_id sid on t.Symbol=sid.Symbol and len(sid.symbol)<3 inner join (SELECT convert(nvarchar(16),[inserttime],120)+':00' as stockdate ,[longhave]-[shorthave] as totalposition FROM [LogRecord].[dbo].[account_position] where userid='%s'   and inserttime<='%s' and inserttime>='%s' and stockid=%s )a on t.StockDate=a.stockdate and sid.S_ID=%s order by a.stockdate" % (realaccount,endtime,begintime,realstokid,realstokid)
	res2=ms.find_sql(sql)
	print sql 
	# merge with Tsymbol_allfuture stockdate
	positionlist=res2
	fisrttime=positionlist[0][0]
	#[datetime.datetime(2015, 10, 21, 9, 0), 6.0, 6.0]
	sql="select	C,StockDate from TSymbol_allfuture where Symbol='%s' and  stockdate >='%s' and stockdate<='%s' order by StockDate " % (symbol,begintime,endtime)
	res=ms.dict_sql(sql)
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
		templastposition=[0,0,0]
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
	# for item in mymewquote:
	# 	print item 

	########################################
	if res2:
		#compute commvalue  pointvalue
		symbolto=symbol
		commvalue=1
		pointvalue=1
		sql="SELECT [symbol]  ,[multi] as [pointvalue]  ,[comm] as [commision] FROM [Future].[dbo].[Symbol_ID] where Symbol='%s'" % (symbolto)
		res=ms.dict_sql(sql)
		if res:
			pointvalue=res[0]['pointvalue']
			commvalue=res[0]['commision']
		##############################

		#compute every stockdate delta_equity
		lastposition=mymewquote[0][2]
		lastclose=mymewquote[0][1]
		totalequity={}
		for item in mymewquote:
			print item[0],item[1],item[2]
			deltatime=abs(item[2]-lastposition)
			deltaquanyi=(lastposition*(item[1]-lastclose)*float(pointvalue)-deltatime*commvalue)
			lastposition=item[2]
			lastclose=item[1]
			totalequity[item[0]]=deltaquanyi
		dictlist=sorted(totalequity.iteritems(),key=lambda d:d[0],reverse=False)
		cal_day=dictlist[-1][0].strftime('%Y%m%d')
		lastdayendtime=datetime.datetime.strptime(cal_day+" 15:00:00",'%Y%m%d %H:%M:%S')
		lastdaybegintime=lastdayendtime-datetime.timedelta(hours=18)
		#lastdaytime=datetime.datetime.strptime(cal_day+" 08:00:00",'%Y%m%d %H:%M:%S')

		lastday_equity=0
		for item in dictlist:
			if item[0]>=lastdaybegintime:
				lastday_equity=lastday_equity+item[1]
		print cal_day,symbolto,lastday_equity
	else:
		lastday_equity=0
		#print 'not exit',symbol,lastday_equity
	real_total.append(lastday_equity)



sql="select * from (select distinct f_ac from p_follow where ac='StepMultigaosheng1') a order by replace(f_ac,'StepMultigaosheng1','')"
myres=ms.dict_sql(sql)
for myitem in myres:
	#print myitem
	cal_ac_day_equity('StepMultigaosheng1',myitem['f_ac'],1)
print 'lilun_total',sum(lilun_total)

# sql="select replace(f_ac,'StepMultigaosheng1','') as symbol ,Stock from p_follow where ac='StepMultigaosheng1' order by replace(f_ac,'StepMultigaosheng1','')"
# myres2=ms.dict_sql(sql)
# for myitem in myres2:
# 	#print 'begin:',myitem['symbol'],myitem['Stock']
# 	cal_ac_day_equity_real('1636737',myitem['Stock'],myitem['symbol'])
# print 'real_total',sum(real_total)
# exit()
# cal_ac_day_equity_real('1636737',1,'ru')
# cal_ac_day_equity('StepMultigaosheng1','csStepMultigaosheng1',1)