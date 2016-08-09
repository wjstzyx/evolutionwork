#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
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
	sql="delete from dailyquanyi where ac='%s' and symbol='%s' and D=%s" % (ac,symbolto,todaytime)
	ms.insert_sql(sql)
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
	sql="select deltaposition,0 as position,C,0 as deltaquanyi,0 as comm, D,stockdate into %s from (select ISNULL(b.position,0) AS deltaposition ,a.StockDate,a.C,a.D from TSymbol a left outer join [quanyi_log_groupby_V2] b on a.Symbol='%s'  and b.symbol='%s' and b.type=0  and b.ac='%s' and a.StockDate=b.stockdate where a.Symbol='%s' ) temp " % (tablename,symbolto,symbolfrom,ac,symbolto)
	print sql
	exit()
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

	sql="select max(D) from dailyquanyi where ac='%s' and symbol='%s'" % (ac,symbolto)
	lastrecordday=ms.find_sql(sql)[0][0]
	#lastrecordday记录的是这天21:00之后的收益
	if lastrecordday is None:
		lastrecordday=151001
	lastdaytime=int(lastrecordday)+20000000
	lastdaytime=datetime.datetime.strptime(str(lastdaytime),'%Y%m%d')
	lastdaytime=lastdaytime+datetime.timedelta(hours=10)


	sql="select distinct CONVERT(varchar(10), stockdate, 120 ) as datename from %s where stockdate>='%s' order by datename" % (tablename,lastdaytime)
	#print sql
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
		
		deltaquanyi=myround(lastposition)*float((C-lastClose))*float(pointvalue)
		deltatime=abs(myround(lastposition+deltaposition)-myround(lastposition))
		deltacomm=deltatime*commvalue
		# deltaquanyilist[stockdate]=deltaquanyi
		# deltacommlist[stockdate]=deltacomm
		# deltaroundplist[stockdate]=deltatime

		###########插入日期分类
		if stockdate>=lastdaytime:
			#print stockdate, myround(lastposition),float((C-lastClose)),C,lastClose
			#dayindex=range_quanyi_byyepan(stockdate,daylists)			
			dayindex=range_quanyi_bydaily(stockdate,daylists)

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
	# print newlist
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
			sql="insert into dailyquanyi(ac,symbol,position,quanyi,comm,D,d_max,times) values('%s','%s',%s,%s,%s,%s,%s,%s)" % (ac,symbolto,myround(position),lastdayquanyi,lastdaycomm,changeD,d_max,times)
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








def pre_quanyi_data(ac,symbol,type):
	sql="select max(stockdate) as stockdate FROM [Future].[dbo].[quanyi_log_groupby_V2] where ac='%s' and symbol='%s'" % (ac,symbol)
	res=ms.dict_sql(sql)[0]
	if res['stockdate'] == None:
		nowD=151020
		print "NONENONENNOE"
	else:
		nowD=res['stockdate'].strftime("%Y%m%d")[2:]
		nowD=int(nowD)
	sql="select distinct D from st_report where D>=%s  order by D" % (nowD)
	res=ms.dict_sql(sql)
	for item1 in res:
		print item1['D']
		input_groupbyquanyi(ac,symbol,type,item1['D'])
		# time.sleep(6)




def main_fun():
	#获取需要处理的列表
	sql="SELECT [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isforbacktest]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where iscaculate=1  and isyepan=0"
	# sql="SELECT [acname] ,[positionsymbol] ,[quanyisymbol] ,[iscaculate]  ,[isforbacktest]  ,[isstatistic] FROM [LogRecord].[dbo].[quanyicaculatelist] where isforbacktest=0 and positionsymbol='JD'"
	res=ms.dict_sql(sql)
	for item in res:
		print item['acname']
		positionsymbol=item['positionsymbol']
		quanyisymbol=item['quanyisymbol']
		pre_quanyi_data(item['acname'],item['positionsymbol'],0)
		daylycaculate(positionsymbol,quanyisymbol,item['acname'])


# main_fun()
# input_groupbyquanyi('9AGOLD','AG',0,160628)
# pre_quanyi_data('9AGOLD','AG',0)
# daylycaculate('pythonRun-TF-CH-rev-right','TF','TF')
# input_groupbyquanyi('RB2trendorig','RB',0,160706)
# pre_quanyi_data('JDQGST_TG','JD',0)
# daylycaculate('RB','RB','RB2uprev')