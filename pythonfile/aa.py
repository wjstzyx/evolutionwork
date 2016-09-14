# -*- coding: utf-8 -*- 
import string, os
import csv
import time
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime

def order_get_ac_ratio_two(account):
	#获取总账户配置的虚拟组的ratio
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	#sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  [LogRecord].[dbo].[order_p_follow] WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100 FROM   Emp         INNER JOIN [LogRecord].[dbo].[order_p_follow] d ON d.ac = Emp.F_ac)SELECT AC,f_AC,ratio FROM  Emp" % (account)
	#sql="select AC,f_AC,ratio from [LogRecord].[dbo].[order_p_follow] where ac='%s'" % (account)
	#检测是否自循环
	sql="select * from [LogRecord].[dbo].[order_p_follow]  where ac=F_ac and ac='%s'" % (account)
	res=ms.dict_sql(sql)
	if res:
		return []

	sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  [LogRecord].[dbo].[order_p_follow] WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100 FROM   Emp         INNER JOIN [LogRecord].[dbo].[order_p_follow] d ON d.ac = Emp.F_ac)     select '%s' as AC,f_AC,SUM(ratio) as ratio from Emp where  f_ac not in (select ac from Emp) group by F_ac" % (account,account)
	res=ms.dict_sql(sql)
	accountlist=[]
	aclist=[]
	for item in res:
		accountlist.append(item['AC'])
		aclist.append(item['f_AC'])
	accountlist=list(set(accountlist))
	aclist=list(set(aclist))
	# print accountlist
	# print aclist
	ac_ratio={}
	for item in aclist:
		ac_ratio[item]=0
	for item in res:
		ac_ratio[item['f_AC']]=ac_ratio[item['f_AC']]+item['ratio']
	# print ac_ratio
	for key in accountlist:
		if ac_ratio.has_key(key):
			del ac_ratio[key]
	# print ac_ratio
	return ac_ratio


aclistresult= order_get_ac_ratio_two('9785')
newaclistresult={}
for key in aclistresult:
	newaclistresult[key.lower()]=aclistresult[key]
aclistresult=newaclistresult
keylist=""
for key in aclistresult:
	keylist=keylist+",'"+key+"'"
keylist=keylist.strip(",")

sql="select kk.acname,quanyisymbol,case when issumps=0 then pp.position when issumps=1 then 10 end as position from LogRecord.dbo.quanyicaculatelist kk inner join (select round(SUM(p.P_size*a.ratio/100.0),0) as position,p.ac,p.STOCK from p_basic p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.AC in (%s) where p.ac in (%s) group by p.ac,p.STOCK) pp on kk.acname=pp.AC" % (keylist,keylist)
tmpres11=ms.dict_sql(sql)
resultlist={}
for item in tmpres11:
	resultlist[item['quanyisymbol']]=0
for item in tmpres11:
	resultlist[item['quanyisymbol']]=resultlist[item['quanyisymbol']]+item['position']*aclistresult[str(item['acname']).lower()]/100.0
	del aclistresult[item['acname'].lower()]
for key in aclistresult:
	resultlist[key]="此虚拟组没有找到对应手数"
resultlist=[(key,resultlist[key]) for key in resultlist]
resultlist.sort(key=lambda x:x[0]) 
print resultlist


