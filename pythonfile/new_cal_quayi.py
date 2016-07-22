#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# 返回行情list 或者0

def myround(num):
	if num>=0:
		return round(num)
	if num<=0:
		return round(num+0.000000001)

def input_groupbyquanyi(ac,symbol):
	# 清除临时表
	try:
		sql="drop table #temp_quanyi_new"
		ms.insert_sql(sql)
		sql="drop table #temp_p_log"
		ms.insert_sql(sql)
	except:
		pass
	# 产生临时p_log
	sql="select * into #temp_p_log from (SELECT   aa.*, sid.Symbol, (YEAR(GETDATE()) - 2000) * 10000 + MONTH(GETDATE()) * 100 + DAY(GETDATE()) AS D from (select  p.AC, p.STOCK, p.type, p.ST, p.P_size, a.ratio from P_BASIC p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.type=a.type and p.AC='%s') as aa inner join Symbol_ID AS sid ON sid.S_ID = aa.STOCK where Symbol='%s') temp" % (ac,symbol)
	#print sql
	ms.insert_sql(sql)
	sql="select SUM(p_size*ratio/100) as totalsum from #temp_p_log"
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
		sql="select	C,StockDate from TSymbol where Symbol='%s' and  stockdate >='%s' order by StockDate " % (symbol,fisrttime)
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


def cal_quanyi(ac,myquotes,totalsum,symbolto):
	if totalsum<=0:
		totalsum=1000000
	#totalsum=10
	commvalue=1
	pointvalue=1
	sql="SELECT [symbol]  ,[pointvalue]  ,[commision] FROM [LogRecord].[dbo].[symbolpointvalue] where Symbol='%s'" % (symbolto)
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
	i=0
	for item in tempquotes:
		datetime=item[0]
		deltatime=abs(myround(item[2])-myround(lastposition))
		totalquanyi=(myround(lastposition)*(item[1]-lastC)*float(pointvalue)-deltatime*commvalue)/totalsum+totalquanyi
		lastposition=item[2]
		lastC=item[1]
		myindex.append(i)
		i=i+1
		avalue.append(datetime)
		yvalue.append(totalquanyi)
	# for i in range(10):
	# 	print avalue[i],yvalue[i]
	plt.figure(figsize=(16,8))
	# plt.plot(avalue, yvalue, 'r')
	# plt.show()
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
	#ax.xaxis.set_major_formatter(pl.DateFormatter('%Y-%m-%d')) 
	pl.grid()
	plt.title('%s---%s' % (ac,symbolto))
	plt.ylabel(u'平均每手净收益',fontproperties='SimHei')
	pl.savefig('%s' % (ac))
	pl.show() 







(myquotes,totalsum)=input_groupbyquanyi('Rbyztp','RB')
#仓位信息OK
# print totalsum
cal_quanyi('Rbyztp',myquotes,totalsum,'RB')