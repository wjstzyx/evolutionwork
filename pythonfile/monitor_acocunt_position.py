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
log_path='E:\\test\\'
log_name='Account_distinct'
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
	sql="SELECT [account] ,[isdoCommodity]   ,[isdoIFICIH]   ,[realposition_source] FROM [LogRecord].[dbo].[monitor_accountlist]"
	res=ms.dict_sql(sql)
	return res
# 获取实际账户 和理论仓位
def get_real_lilun_position(accountdict={}):
	ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
	accountdict={u'account': u'05810058', u'isdoIFICIH': 1, u'realposition_source': u'account_position_2', u'isdoCommodity': 1}
	if accountdict['realposition_source']=='account_position_2':
		sql="select upper(a.instrumentid) as conid,a.longhave,a.longsend,a.shorthave,a.shortsend,a.inserttime from (select * from LogRecord.dbo.account_position_2 where userid='05810058' ) a inner join (select MAX(inserttime) as inserttime,instrumentid from LogRecord.dbo.account_position_2 where userid='05810058'  group by instrumentid )b on a.instrumentid=b.instrumentid  and a.inserttime=b.inserttime"
		res_real=ms.dict_sql(sql)
		sql="select upper(instrumentid) as conid,num,GETDATE() as nowtime from view_05810058"
		res_lilun=ms.dict_sql(sql)
	elif accountdict['realposition_source']=='account_position':
		sql="select upper(aa.Symbol+'_'+cast(a.stockID as nvarchar)) as conid,a.longhave,a.longsend,a.shorthave,a.shortsend,a.inserttime from (select * from LogRecord.dbo.account_position where userid='05810058' ) a inner join (select MAX(inserttime) as inserttime,stockid from LogRecord.dbo.account_position where userid='05810058'  group by stockid )b on a.stockid=b.stockid  and a.inserttime=b.inserttime inner join symbol_id aa on a.stockID=aa.S_ID and LEN(aa.Symbol)<3"
		res_real = ms.dict_sql(sql)
		sql = "select upper(aa.Symbol+'_'+CAST(a.STOCK as nvarchar)) as conid,Expr1 as num,GETDATE() as nowtime from view_8005004702 a inner join symbol_id aa on a.STOCK=aa.S_ID and len(aa.Symbol)<3"
		res_lilun = ms.dict_sql(sql)
	else:
		print '##### source is error'
		return 0
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
		if not new_real.has_key(conid):
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
			if item[2:6]<>[str(content['longhave']),str(content['longsend']),str(content['shorthave']),str(content['shortsend'])]:
				#update time
				sql="update [LogRecord].[dbo].[account_position_temp_compare_v2] set inserttime=getdate(),longhave=%s,longsend=%s,shorthave=%s,shortsend=%s,lilun_position=%s where userID='%s' and conid='%s';" % (item[2], item[3], item[4], item[5], item[6],account,item[1])
				todo_sql=todo_sql+sql
		else:
			# insert record
			sql = "insert into [LogRecord].[dbo].[account_position_temp_compare_v2]([userID]  ,[conid]  ,[longhave]  ,[longsend]   ,[shorthave]  ,[shortsend]  ,[lilun_position]   ,[inserttime]) values('%s','%s',%s,%s,%s,%s,%s,getdate());" % (item[0], item[1], item[2], item[3], item[4], item[5], item[6])
			todo_sql = todo_sql + sql
	# delete

	print todo_sql
	#ms.insert_sql(todo_sql)







#get_all_monitor_list()
result= get_real_lilun_position()
compare_position(result[0],result[1],result[2],log)
