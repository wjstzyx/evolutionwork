#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from real_st_report")
# print resList
def myround(num):
	if num>=0:
		return round(num)
	if num<=0:
		return round(num+0.000000001)




def daylycaculate(symbolfrom,symbolto,ac):
	print "start daily"
	todaytime=int(datetime.datetime.now().strftime("%Y%m%d"))-20000000
	#todaytime=160628
	sql="delete from real_dailyquanyi where ac='%s' and symbol='%s' and D=%s" % (ac,symbolto,todaytime)
	ms.insert_sql(sql)
	#--end指将这个日期计算的收益（当天21:00信号后才逐渐由收益，21:00之前都是0）
	#获取Pointvalue
	sql="SELECT [symbol]  ,[pointvalue]  ,[commision] FROM [LogRecord].[dbo].[symbolpointvalue] where Symbol='%s'" % (symbolto)
	res=ms.dict_sql(sql)
	if res:
		pointvalue=res[0]['pointvalue']
		commvalue=res[0]['commision']
	#--end

	tablename="#tempinfo_%s" % (ac)
	tablename=tablename.replace('-','_')
	# tablename='tempquanyiinfo'
	try:		
		sql="drop table %s" % (tablename)
		ms.insert_sql(sql)
	except:
		pass
	sql="select deltaposition,0 as position,C,0 as deltaquanyi,0 as comm, D,stockdate into %s from (select ISNULL(b.position,0) AS deltaposition ,a.StockDate,a.C,a.D from TSymbol a left outer join [real_quanyi_log_groupby] b on a.Symbol='%s'  and b.symbol='%s' and b.type=0  and b.ac='%s' and a.StockDate=b.stockdate where a.Symbol='%s' ) temp " % (tablename,symbolto,symbolfrom,ac,symbolto)
	# print sql
	ms.insert_sql(sql)
	sql="select * from %s order by stockdate" % (tablename)
	# print sql 
	res=ms.dict_sql(sql)
	#开始计算，初始化变量
	lastposition=0
	lastClose=res[0]['C']

	# lastdaypostiion=0
	lastdayquanyi=0
	# lastdaycomm=0
	# times=0
	deltaquanyilist={}
	deltacommlist={}
	deltaroundplist={}

	sql="select max(D) from real_dailyquanyi where ac='%s' and symbol='%s'" % (ac,symbolto)
	lastrecordday=ms.find_sql(sql)[0][0]
	#lastrecordday记录的是这天21:00之后的收益
	if lastrecordday is None:
		lastrecordday=151001
	lastdaytime=int(lastrecordday)+20000000
	lastdaytime=datetime.datetime.strptime(str(lastdaytime),'%Y%m%d')
	lastdaytime=lastdaytime+datetime.timedelta(hours=10)


	sql="select distinct CONVERT(varchar(10), stockdate, 120 ) as datename from %s where stockdate>='%s' order by datename" % (tablename,lastdaytime)
	datelist=ms.dict_sql(sql)
	dayquanyilist={}
	for item in datelist:
		mytime=item['datename'].replace('-','')
		mytime=str(int(mytime)-20000000)
		#dayquanyilist=[quanyi,comm,times,ref(-1)position]
		dayquanyilist[mytime]=[0,0,0,0]
	daylists=[k for k in sorted(dayquanyilist.keys())]
	# print daylists

	for item in res:
		stockdate=item['stockdate']
		C=item['C']
		deltaposition=item['deltaposition']
		# if stockdate>=datetime.datetime.strptime('2016-06-15','%Y-%m-%d') and stockdate<=datetime.datetime.strptime('2016-06-16','%Y-%m-%d'):
		# 	print stockdate, myround(lastposition),float((C-lastClose)),C,lastClose
		deltaquanyi=myround(lastposition)*float((C-lastClose))*float(pointvalue)
		deltatime=abs(myround(lastposition+deltaposition)-myround(lastposition))
		deltacomm=deltatime*commvalue
		# deltaquanyilist[stockdate]=deltaquanyi
		# deltacommlist[stockdate]=deltacomm
		# deltaroundplist[stockdate]=deltatime

		###########插入日期分类
		if stockdate>=lastdaytime:
			dayindex=range_quanyi_byyepan(stockdate,daylists)			
			#dayindex=range_quanyi_bydaily(stockdate,daylists)
			dayquanyilist[dayindex][0]=dayquanyilist[dayindex][0]+deltaquanyi
			dayquanyilist[dayindex][1]=dayquanyilist[dayindex][1]+deltacomm
			dayquanyilist[dayindex][2]=dayquanyilist[dayindex][2]+deltatime
			dayquanyilist[dayindex][3]=myround(lastposition)
		###########
		lastposition=lastposition+deltaposition
		lastClose=C
	#--end数据dict计算完毕

	####写入数据库
	newlist=[(k,dayquanyilist[k]) for k in sorted(dayquanyilist.keys())]
	for item in newlist:
		position=item[1][3]
		lastdayquanyi=item[1][0]
		lastdaycomm=item[1][1]
		changeD=item[0]
		times=item[1][2]
		sql="SELECT round(sum(p_size*ratio/100),0) FROM p_log where type=1 and st<>123456 and ac='%s' and symbol='%s' and d=%s" % (ac,symbolfrom,changeD)
		d_max=ms.find_sql(sql)[0][0]
		if d_max is None or d_max==0:
			d_max=0.0001
		if changeD>lastrecordday:
			sql="insert into real_dailyquanyi(ac,symbol,position,quanyi,comm,D,d_max,times) values('%s','%s',%s,%s,%s,%s,%s,%s)" % (ac,symbolto,myround(position),lastdayquanyi,lastdaycomm,changeD,d_max,times)
			ms.insert_sql(sql)


	try:		
		sql="drop table %s" % (tablename)
		ms.insert_sql(sql)
	except:
		pass



def range_quanyi_byyepan(stockdate,daylists):
	D=stockdate.strftime('%Y%m%d')
	thisday=str(int(D)-20000000)
	thisdayindex=daylists.index(thisday)
	beforeday=daylists[thisdayindex-1]
	D=datetime.datetime.strptime(D,'%Y%m%d')
	Dcenter=D+datetime.timedelta(hours=24)
	timedelta1 = Dcenter - stockdate
	timedelta1=abs(timedelta1.total_seconds())
	if timedelta1<3600*5:
		return thisday
	else:
		return beforeday

def range_quanyi_bydaily(stockdate,daylists):
	D=stockdate.strftime('%Y%m%d')
	thisday=str(int(D)-20000000)
	return thisday



def input_groupbyquanyi(ac,symbol,type,D):
	#删除当日8点之后已经存在的记录
	todaytime=datetime.datetime.now().strftime("%Y-%m-%d")
	todaytime=datetime.datetime.strptime(todaytime,"%Y-%m-%d")
	deltime=todaytime+datetime.timedelta(hours=8)
	sql="delete from real_quanyi_log_groupby where ac='%s' and symbol='%s' and type=%s and stockdate>'%s'" % (ac,symbol,type,deltime)
	ms.insert_sql(sql)
	#--end
	try:
		sql="drop table #temp_quanyi_new"
		ms.insert_sql(sql)
	except:
		pass
	sql="select * into  #temp_quanyi_new from (select '%s' as ac,'%s' as symbol,'%s' as type,temp.id,p,PP,p_size,ratio,st,o.stockdate from tsymbol o inner join (select real_st_report.id,real_st_report.p,real_st_report.pp,p.symbol,real_st_report.stockdate,real_st_report.st,p.p_size,p.ac,p.ratio,real_st_report.type from real_st_report  inner join p_log p on p.st=real_st_report.st and p.ac='%s' and p.symbol='%s' and p.d=%s and real_st_report.type=%s ) temp on temp.stockdate=o.stockdate and o.symbol=temp.symbol where o.symbol='%s' ) temp " % (ac,symbol,type,ac,symbol,D,type,symbol)
	ms.insert_sql(sql)
	print 2,datetime.datetime.now()
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
		print 4,datetime.datetime.now()
		sql="select (p*p_size*ratio/100) as p,st,stockdate from #temp_quanyi_new  order by stockdate"
		res1=ms.dict_sql(sql)
		for item in res1:
			#赋值laststlistposition
			deltepositionlist[item['stockdate']]=deltepositionlist[item['stockdate']]+(item['p']-laststlistposition[item['st']])
			laststlistposition[item['st']]=item['p']
		print 5,datetime.datetime.now()
		newlist=[(k,deltepositionlist[k]) for k in sorted(deltepositionlist.keys())]

		#选出数据库中最新的记录
		#D=160628指计算28日21点之后的仓位
		myDbegin=str(D+20000000)
		myDbegin=datetime.datetime.strptime(myDbegin,'%Y%m%d')
		myDbegin=myDbegin+datetime.timedelta(minutes=1260)
		myDend=myDbegin+datetime.timedelta(hours=6)
		#myDbegin='2016-06-28 21:00:00'
		sql="select top 1 totalposition,stockdate from [real_quanyi_log_groupby] where ac='%s' and symbol='%s' and TYPE=%s order by stockdate desc " % (ac,symbol,type)
		res=ms.dict_sql(sql)
		if res:
			#lastdayP=res[0]['totalposition']
			laststockdate=res[0]['stockdate']
		else:
			#lastdayP=0
			laststockdate=datetime.datetime.strptime('2010-01-01','%Y-%m-%d')
		#计算昨天的总仓位
		sql="select top 1 totalposition,stockdate from [real_quanyi_log_groupby] where ac='%s' and symbol='%s' and TYPE=%s and stockdate<'%s' order by stockdate desc " % (ac,symbol,type,myDbegin)
		res=ms.dict_sql(sql)
		if res:
			lastdayP=res[0]['totalposition']
		else:
			lastdayP=0
		#写入交易日第一根BAR
		sql="select  top 1 stockdate  from Tsymbol where symbol='%s' and stockdate >='%s' and stockdate<='%s' order by stockdate " % (symbol,myDbegin,myDend)
		firststockdate=ms.dict_sql(sql)
		if firststockdate:
			#如果存在第一根BAR则继续
			firststockdate=firststockdate[0]['stockdate']
			# #分商品和IC  IF 两类	
			# if 	symbol in ('IC','IF'):
			# 	firststockdate=firststockdate.strftime("%Y-%m-%d 09:30:00")
			# 	firststockdate=datetime.datetime.strptime(firststockdate,"%Y-%m-%d %H:%M:%S")
			# 	#去除9:00-9:29分钟的信号
			# 	for item in newlist:
			# 		timestr=item[0].strftime("%H%M")
			# 		timestr=int(timestr)
			# 		if timestr>=900 and  timestr<=929:
			# 			newlist.remove(item)
			# 	#--end
			#开始计算当天仓位
			sql="select SUM(a.p*a.p_size*a.ratio/100) as P from #temp_quanyi_new a inner join(  select MAX(StockDate) as stockdate,st from #temp_quanyi_new where StockDate<='%s'  group by st  ) temp  on a.ST=temp.ST and a.StockDate=temp.stockdate" % (firststockdate)
			lastP=ms.find_sql(sql)[0][0]
			if lastP is None:
				lastP=0
			deltaposition=lastP-lastdayP
			#插入数据库
			valueslist="('%s','%s','%s','%s','%s','%s')" % (ac,symbol,type,deltaposition,firststockdate,lastP)
			for item in newlist:
				#只插入D这天的数据，从>firststockdate这个时间戳开始
				if (int(item[0].strftime("%Y%m%d"))-20000000)==D and item[0]>firststockdate:
					lastP=lastP+item[1]
					if item[0]>laststockdate:
						valueslist=valueslist+","+"('%s','%s','%s','%s','%s','%s')" % (ac,symbol,type,item[1],item[0],lastP)
			valueslist=valueslist.strip(',')
			if firststockdate>laststockdate:
				sql="insert into [Future].[dbo].[real_quanyi_log_groupby](ac,symbol,[type],[position],[stockdate],[totalposition]) values "+valueslist
				ms.insert_sql(sql)
				print 7,datetime.datetime.now()

	sql="drop table #temp_quanyi_new"
	ms.insert_sql(sql)
	print "OK"


def pre_quanyi_data(ac,symbol,type):
	sql="select max(stockdate) as stockdate FROM [Future].[dbo].[real_quanyi_log_groupby] where ac='%s' and symbol='%s'" % (ac,symbol)
	res=ms.dict_sql(sql)[0]
	if res['stockdate'] == None:
		nowD=151020
		print "NONENONENNOE"
	else:
		nowD=res['stockdate'].strftime("%Y%m%d")[2:]
		nowD=int(nowD)
	# nowD=160601
	sql="select distinct D from real_st_report where D>=%s  order by D" % (nowD)
	res=ms.dict_sql(sql)
	for item1 in res:
		print item1['D']
		input_groupbyquanyi(ac,symbol,type,item1['D'])
		# time.sleep(6)





def main_fun():
	#获取需要处理的列表
	sql="SELECT [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isforbacktest]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where iscaculate=1  and isyepan=1"
	# sql="SELECT [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isforbacktest]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where isforbacktest=0 and positionsymbol='JD'"
	res=ms.dict_sql(sql)
	for item in res:
		print item['acname']
		positionsymbol=item['positionsymbol']
		quanyisymbol=item['quanyisymbol']
		pre_quanyi_data(item['acname'],item['positionsymbol'],0)
		daylycaculate(positionsymbol,quanyisymbol,item['acname'])


main_fun()
# input_groupbyquanyi('RBQGSTREVYP_TG','RBnight',0,160628)
# pre_quanyi_data('RBNtrend2','RBnight',0)
# daylycaculate('RBnight','RBnight','RBNtrend2')