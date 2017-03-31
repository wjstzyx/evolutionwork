#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import pandas as pd
import datetime
import numpy as np
from Mylog import MyLog
import platform
name=platform.platform()
if 'Windows' in name:
	log_path='E:\\test\\'
if 'Linux' in name:
	log_path='/home/yuyang/myfile/logfile/'

log_name='_Account_distinct'
pre_fix=datetime.datetime.now().strftime('%Y%m%d')
log_name=pre_fix+log_name
logger = MyLog(log_name)
logger.set_path(log_path)
log = logger.log


# 获取收件人名单
def get_messagelist():
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
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


def get_all_monitor_list():
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	sql="SELECT [account] ,[isdoCommodity]   ,[isdoIFICIH]   ,[realposition_source] FROM [LogRecord].[dbo].[monitor_accountlist] where (isdoCommodity+isdoIFICIH)>0"
	res=ms.dict_sql(sql)
	return res
# 获取实际账户 和理论仓位
def get_real_lilun_position(accountdict={}):
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	#accountdict={u'account': u'05810058', u'isdoIFICIH': 1, u'realposition_source': u'account_position_2', u'isdoCommodity': 1}
	today=datetime.datetime.now().strftime('%Y%m%d')
	if accountdict['realposition_source']=='account_position_2':
		sql="select case when upper(dbo.m_getstr(instrumentid)) IN ('IC','IF','IH','T','TF') THEN upper(dbo.m_getstr(instrumentid)) else upper(instrumentid) end as conid,longhave,longsend,shorthave,shortsend,inserttime from LogRecord.dbo.account_position_2 where userid='%s' and DATE='%s' and time in (select MAX(time) as maxtime from  LogRecord.dbo.account_position_2 where userid='%s'  and date='%s')" % (accountdict['account'],today,accountdict['account'],today)
		res_real=ms.dict_sql(sql)
		sql="select upper(instrumentid) as conid,num,GETDATE() as nowtime from view_%s" % (accountdict['account'])
		res_lilun=ms.dict_sql(sql)
	elif accountdict['realposition_source']=='account_position':
		sql="select upper(aa.Symbol+'_'+cast(a.stockID as nvarchar)) as conid,a.longhave,a.longsend,a.shorthave,a.shortsend,a.inserttime from  (select * from LogRecord.dbo.account_position where userid='%s' and DATE='%s' and time in (select MAX(time) as maxtime from  LogRecord.dbo.account_position where userid='%s'  and date='%s') ) a inner join symbol_id aa on a.stockID=aa.S_ID and len(aa.Symbol)<3" % (accountdict['account'],today,accountdict['account'],today)
		res_real = ms.dict_sql(sql)
		sql = "select upper(aa.Symbol+'_'+CAST(a.STOCK as nvarchar)) as conid,Expr1 as num,GETDATE() as nowtime from view_%s a inner join symbol_id aa on a.STOCK=aa.S_ID and len(aa.Symbol)<3" % (accountdict['account'])
		res_lilun = ms.dict_sql(sql)
	else:
		print '##### source is error'
		return 0

	# add stock position lilun
	ms1 = MSSQL(host="139.196.104.105", user="future", pwd="K@ra0Key", db="Future")
	sql="SELECT upper(a.symbol) as conid,sum(a.ratio*b.position ) as num ,GETDATE() as nowtime  FROM [future].[dbo].[account_position_stock_yingshe] a left join [future].[dbo].[RealPosition] b on a.acanme=b.Name group by a.account,a.symbol having a.account ='%s'" % (accountdict['account'])
	res1=ms1.dict_sql(sql)
	##### 替换 IC IF 等标记
	refer_info={'IC':11,'IF':4,'IH':12,'T':13,'TF':38}
	for item in res1:
		if refer_info.has_key(item['conid']):
			item['conid']=item['conid']+'_'+str(refer_info[item['conid']])
	#####

	res_lilun.extend(res1)


	return accountdict['account'],res_lilun,res_real


# 对比仓位差异，入库
def compare_position(account,lilun,real,log):
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	total_distinct_content=[]
	#转换lilun 数据形式
	new_lilun=dict()
	new_real=dict()
	for item in lilun:
		new_lilun[item['conid']]=item
	for item in real:
		new_real[item['conid']]=item

	# 逐条对比 real
	for item in real:
		conid=item['conid']
		if new_lilun.has_key(conid):
			lilun_position=new_lilun[conid]['num']
			lilun_time=new_lilun[conid]['nowtime']
		else:
			lilun_position=0
			lilun_time=datetime.datetime.now()
		temp = [account, conid, str(item['longhave']), str(item['shorthave']), str(item['longsend']),str(item['shortsend']), str(int(lilun_position))]
		if int((item['longhave']-item['shorthave']))<>int(lilun_position):
			total_distinct_content.append(temp)
			log.info(",".join(temp)+'---liluntime:'+lilun_time.strftime('%Y-%m-%d %H:%M:%S')+'---realtime:'+item['inserttime'].strftime('%Y-%m-%d %H:%M:%S'))
	# 检查 lilun 存在 real 不存在的
	for item in lilun:
		conid = item['conid']
		lilun_position=item['num']
		lilun_time=item['nowtime']
		if not new_real.has_key(conid) and lilun_position<>0:
			temp = [account, conid, '0', '0', '0','0', str(int(lilun_position))]
			total_distinct_content.append(temp)
			log.info(",".join(temp) + '---liluntime:' + lilun_time.strftime('%Y-%m-%d %H:%M:%S') + '---realtime:No')

	# 查询已经有的记录
	sql="SELECT id, [userID] ,[conid]  ,[longhave]  ,[longsend]  ,[shorthave]  ,[shortsend]  ,[lilun_position]  ,[inserttime] FROM [LogRecord].[dbo].[account_position_temp_compare_v2] where [userID] ='%s'" % (account)
	res=ms.dict_sql(sql)
	new_res={}
	todo_sql=""
	for item in res:
		new_res[item['conid']]=item
	for item in total_distinct_content:
		if new_res.has_key(item[1]):
			content=new_res[item[1]]
			#print item[2:6],item[1]
			#print [str(content['longhave']),str(content['shorthave']),str(content['longsend']),str(content['shortsend'])]
			if item[2:6]<>[str(content['longhave']),str(content['shorthave']),str(content['longsend']),str(content['shortsend'])]:
				#update time
				sql="update [LogRecord].[dbo].[account_position_temp_compare_v2] set inserttime=getdate(),longhave=%s,shorthave=%s,longsend=%s,shortsend=%s,lilun_position=%s where userID='%s' and conid='%s';" % (item[2], item[3], item[4], item[5], item[6],account,item[1])
				todo_sql=todo_sql+sql
		else:
			# insert record
			sql = "insert into [LogRecord].[dbo].[account_position_temp_compare_v2]([userID]  ,[conid]  ,[longhave]  ,[shorthave] ,[longsend]    ,[shortsend]  ,[lilun_position]   ,[inserttime]) values('%s','%s',%s,%s,%s,%s,%s,getdate());" % (item[0], item[1], item[2], item[3], item[4], item[5], item[6])
			todo_sql = todo_sql + sql
	# delete
	new_total_distinct_content=[]
	new_total_distinct_content=[item[1] for item in total_distinct_content]
	if new_total_distinct_content==[]:
		sql="delete from [LogRecord].[dbo].[account_position_temp_compare_v2] where userid='%s';" % (account)
		todo_sql=todo_sql+sql
	else:
		for item in res:
			if item['conid'] not in new_total_distinct_content:
				sql="delete from [LogRecord].[dbo].[account_position_temp_compare_v2] where userid='%s' and conid='%s';" % (account,item['conid'])
				todo_sql = todo_sql + sql
	#print todo_sql
	ms.insert_sql(todo_sql)





# update getrecordlist=[{'item':myitem['name'],'msg':msg},{},{}]
def update_target_table(getrecordlist,type):
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
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



# 精确报警逻辑
def select_alert(account):
	# 可以添加
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	sql="SELECT DATEDIFF(MINUTE, inserttime,getdate()) as timediff,inserttime, getdate() as nowtime,[longhave]   ,[longsend]  ,[shorthave]   ,[shortsend] ,[lilun_position],conid FROM [LogRecord].[dbo].[account_position_temp_compare_v2]  where userid='%s'" % (account)
	res=ms.dict_sql(sql)
	nowhour=datetime.datetime.now().strftime('%H%M')
	nowhour=int(nowhour)
	getrecordlist=[]
	for item in res:
		atime = item['timediff']
		uniquekey=item['conid']
		#define condition 1 send=0
		isalert=0
		dealtap=item['longhave']-item['shorthave']+item['longsend']-item['shortsend']
		if dealtap<>item['lilun_position']:
			isalert=1

		if isalert and atime>4 and ((nowhour>=901 and nowhour<=1130) or (nowhour>=1331 and nowhour<=1959)):

			if uniquekey in ('IC','IF','IH','T','TF') and nowhour>933:
				getrecordlist.append({'item':uniquekey,'msg':u'Real:%s  database:%s' % (dealtap,item['lilun_position'])})
			if uniquekey not in ('IC','IF','IH','T','TF'):
				getrecordlist.append({'item':uniquekey,'msg':u'Real:%s  database:%s' % (dealtap,item['lilun_position'])})
	dayofweek=datetime.datetime.now().weekday()
	if dayofweek in (5,6):
		getrecordlist=[]
	return getrecordlist


# 10s 运行完 40个账户
res_lists=get_all_monitor_list()
result= get_real_lilun_position(res_lists[0])
compare_position(result[0],result[1],result[2],log)
getrecordlist=select_alert(result[0])
update_target_table(getrecordlist,'Account2')


