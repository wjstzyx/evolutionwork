#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
import time
import sys, urllib, urllib2, json
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def get_messagelist():
	sql="select email from [LogRecord].[dbo].[mailtolist] where istomail=1"
	reslist=ms.find_sql(sql)
	mailtolist=''
	sendmessage=''
	for item in reslist:
		if "@" in item[0]:
			mailtolist=mailtolist+','+item[0]
		else:
			sendmessage=sendmessage+','+item[0]
	mailtolist=mailtolist.strip(',')
	sendmessage=sendmessage.strip(',')
	return mailtolist,sendmessage


def minusmin(time1,time2):
	#time1=160523
	hour1=round(time1/10000)
	min1=round((time1%10000)/100)
	sec1=time1-hour1*10000-min1*100
	hour2=round(time2/10000)
	min2=round((time2%10000)/100)
	sec2=time2-hour2*10000-min2*100
	return (hour2-hour1)*3600+(min2-min1)*60+(sec2-sec1)

def update_target_table(getrecordlist,type):
	sql="SELECT [id]   ,[type]    ,[item]    ,[msg]     ,[issolved]    ,[isactive]    ,[inserttime] ,[updatetime]     ,[classcode]    FROM [LogRecord].[dbo].[all_monitor_info] where type='%s' and issolved=0 and isactive=1 order by id " % (type)
	res2=ms.dict_sql(sql)
	res2item=[[aa['item'],aa['id']] for aa in res2]
	res1item=[aa['item'] for aa in getrecordlist]
	#1 set some to issovlved
	for item in res2item:
		if item[0] not in res1item:
			sql="update [LogRecord].[dbo].[all_monitor_info] set issolved=1 where type='%s' and id=%s" % (type,item[1])
			ms.insert_sql(sql)
	#2 update or insert to all_monitor_info
	for item in getrecordlist:
		sql = "select 1 from [LogRecord].[dbo].[all_monitor_info] where type='%s' and item='%s' and issolved=0" % (
		type, item['item'])
		res = ms.dict_sql(sql)
		if res:
			sql = "update [LogRecord].[dbo].[all_monitor_info] set updatetime=getdate()  where type='%s' and item='%s'" % (
			type, item['item'])
			# print sql
			ms.insert_sql(sql)
		else:
			sql = " insert into [LogRecord].[dbo].[all_monitor_info](type,item,msg,[issolved],[isactive],[inserttime],[updatetime],[classcode]) values('%s','%s','%s','%s','%s',getdate(),getdate(),'%s')" % (
			type, item['item'], item['msg'], 0, 1, 'fa-bolt')
			# print sql
			ms.insert_sql(sql)


# quotes monitor
def quotes_monitor():
	sql="select DATEDIFF(MINUTE,stockdate,GETDATE()) as mydatediff ,stockdate, Symbol,nowtime from (  select MAX(stockdate) as stockdate,Symbol,GETDATE() as nowtime from TSymbol group by Symbol) a  where DATEDIFF(MINUTE,stockdate,GETDATE())>=2 order by DATEDIFF(MINUTE,stockdate,GETDATE()) desc"
	res=ms.dict_sql(sql)
	nowtime=res[0]['nowtime'].strftime('%H%M')
	print nowtime
	lostinfo=[]

	if (nowtime>='0901' and nowtime<='1014') or (nowtime>='1031' and nowtime<='1130') or (nowtime>='1331' and nowtime<='1500'):
		sql="SELECT [symbol]  FROM [LogRecord].[dbo].[catch_quotes] where isday in (1,12) and symbol not in ('RMZL')"
		tempres=ms.dict_sql(sql)
		selectsymbol=[]
		for item in tempres:
			selectsymbol.append(item['symbol'])
		selectres=[]
		for item in res:
			if item['Symbol'] in selectsymbol:
				if item['Symbol'] in ('T','IC','IF','TF','IH'):
					if nowtime>='0931':
						selectres.append(item)
				else:
					selectres.append(item)
		day_lost_quotes=selectres
		print 'day_lost_quotes',day_lost_quotes
		lostinfo=day_lost_quotes


	if (nowtime>='2101' and nowtime<='2300'):
		sql = "SELECT [symbol] FROM [LogRecord].[dbo].[catch_quotes] where isday =0 and symbol not in ('RMZL')"
		tempres = ms.dict_sql(sql)

		selectsymbol = []
		for item in tempres:
			selectsymbol.append(item['symbol'])
		selectres = []
		for item in res:
			if item['Symbol'] in selectsymbol:
				selectres.append(item)
		night_lost_quotes = selectres
		lostinfo=night_lost_quotes
		print 'night_lost_quotes',night_lost_quotes
	# if exist quotes loss [{u'Symbol': u'HCnight', u'nowtime': datetime.datetime(2017, 3, 2, 10, 32, 43, 727000), u'mydatediff': 693, u'stockdate': datetime.datetime(2017, 3, 1, 22, 59)}]
	getrecordlist=[]
	for myitem in lostinfo:
		item=myitem['Symbol']
		msg = myitem['Symbol'] + '    ' + '缺少 ' + str(myitem['mydatediff']) + '分钟 最新更新时间: ' + myitem[
			'stockdate'].strftime("%Y-%m-%d %H:%M")
		getrecordlist.append({'item':item,'msg':msg})
	update_target_table(getrecordlist,'quotes')


# AB_st_heart
def AB_st_day(mytype=2):
	nowtime=datetime.datetime.now().strftime('%H%M')
	isbegin=0
	if mytype==1:
		if nowtime>='0850' and nowtime<='1540':
			isbegin=1
	if mytype==2:
		if nowtime>='2050' and nowtime<='2330':
			isbegin=1
	print 'isbegin',isbegin
	if isbegin==1:
		sql="select distinct address from (SELECT a.st,a.TradName,b.address,b.stockdate  FROM [Future].[dbo].[Trading_logSymbol] a  inner join(  SELECT [st],address,stockdate   FROM [LogRecord].[dbo].[ST_heart] where DATEDIFF(MINUTE, [stockdate], getdate())>=3 and type in (%s,12)  ) b on a.ST=b.st) a" % (mytype)
		machine=ms.dict_sql(sql)
		getrecordlist=[]
		for item in machine:
			sql="SELECT top 2 a.st,a.TradName,b.address,b.stockdate  FROM [Future].[dbo].[Trading_logSymbol] a  inner join(  SELECT [st],address,stockdate   FROM [LogRecord].[dbo].[ST_heart] where DATEDIFF(MINUTE, [stockdate], getdate())>=3 and type in (2,12)  ) b on a.ST=b.st where address='%s'" % (item['address'])
			res1=ms.dict_sql(sql)
			for item1 in res1:
				myitem=item['address']+' 【'+ str(item1['st'])+'】'
				msg=item1['stockdate'].strftime("%Y-%m-%d %H:%M")+' '+item1['TradName']
				getrecordlist.append({'item':myitem,'msg':msg})
		update_target_table(getrecordlist,'AB')



#Thunder st_heart
def Thunder():
	# 检测最新更新时间与当时的时间差，如果相差80s就报警
	sql = "SELECT [name],time ,getdate() as nowtime,[isific],isnight FROM [future].[dbo].[Program] where isactive=1 order by id  "
	res = ms1.dict_sql(sql)
	getrecordlist=[]
	for myitem in res:
		lasttime = myitem['time']
		nowtime= myitem['nowtime'].strftime('%H%M%S')
		beizhi='lastupdatetime=%s,database_nowtime=%s' % (lasttime,nowtime)
		nowtime=int(nowtime)
		chayi = minusmin(lasttime, nowtime)
		if myitem['isific']==0 and (chayi > 80 or chayi < -80) and  ((nowtime>85400 and nowtime<150400)):
			msg='延迟【%s】秒 %s' % (abs(chayi),beizhi)
			getrecordlist.append({'item':myitem['name'],'msg':msg})
		if myitem['isific']==1 and (chayi > 80 or chayi < -80) and  ((nowtime>92700 and nowtime<151500)):
			msg='延迟【%s】秒 %s' % (abs(chayi),beizhi)
			getrecordlist.append({'item':myitem['name'],'msg':msg})	
		if myitem['isnight']==1 and (chayi > 80 or chayi < -80) and  ((nowtime>205000 and nowtime<233000)):
			msg='延迟【%s】秒 %s' % (abs(chayi),beizhi)
			getrecordlist.append({'item':myitem['name'],'msg':msg})	

	update_target_table(getrecordlist, 'Thunder')

# Account_distinct
def Account_lilun_distinct():
	# sql="SELECT [userID]    ,[stockID]   ,[realposition]   ,[lilunposition]   ,[inserttime] ,b.Symbol FROM [LogRecord].[dbo].[account_position_temp_compare] a left join symbol_id b on a.stockID=b.S_ID where LEN(b.Symbol)<3"
	# res1=ms.dict_sql(sql)
	# getrecordlist=[]
	# for myitem in res1:
	# 	item=myitem['userID']+'_'+myitem['Symbol']
	# 	msg='AB【%s】--Account【%s】'% (myitem['lilunposition'],myitem['realposition'])
	# 	getrecordlist.append({'item':item,'msg':msg})
	# update_target_table(getrecordlist, 'Account')
	pass
	# refer to [cal_position_lilun.py]



for i in range(3):
	try:
		Thunder()
		AB_st_day(1)
		AB_st_day(2)
		quotes_monitor()
	except:
		print 'Find Error'
		subject = '实时总监控脚本出错'
		msg = '实时总监控脚本出错'
		try:
			(mailtolist, sendmessage) = get_messagelist()
		except:
			mailtolist='yuyang@evolutionlabs.com.cn,13764504303@139.com'
			sendmessage='13764504303,13764048827,13661579047'
		sql = "insert into [LogRecord].[dbo].[maillist](subject,mailtolist,msg,type,inserttime,sendmessage) values('%s','%s','%s',%s,getdate(),'%s')" % (subject, mailtolist, msg, 0, sendmessage)
		ms.insert_sql(sql)
	time.sleep(19)


