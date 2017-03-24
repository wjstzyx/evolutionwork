#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pymssql
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
conn=pymssql.connect(host="192.168.0.5",user="future",password="K@ra0Key",database='future',charset="utf8")


def get_df_acname_type(acname,type):
	if type=='zhuli':
		sql="SELECT      [date]        ,round(sum([lilun_zhuli]),0) as %s   FROM [LogRecord].[dbo].[account_lilun_distinct_acname] a  inner join p_follow p on a.acname=p.F_ac and a.account=p.AC  where account='%s' group by [account],date   order by account,date" % (type,acname)
		if acname in ('newtuji300'):
			sql="select date,round(sum(lilun_zhuli/mr.ratio*p.ratio/100.0),0) as %s  from LogRecord.dbo.account_lilun_distinct_acname a inner join p_follow p on a.acname=p.F_ac and p.AC='%s' inner join symbol_id s_id on p.stock=s_id.S_ID and len(s_id.Symbol)<3  inner join  LogRecord.dbo.test_margin mr on mr.symbol=s_id.Symbol  group by date order by date" % (type,acname)
	elif type=='zhishu':
		sql = "SELECT      [date]        ,round(sum([lilun_zhishu]),0) as %s   FROM [LogRecord].[dbo].[account_lilun_distinct_acname] a  inner join p_follow p on a.acname=p.F_ac and a.account=p.AC  where account='%s' group by [account],date   order by account,date" % (type, acname)
	if acname in ('newtuji300'):
		sql = "select date,round(sum(lilun_zhishu/mr.ratio*p.ratio/100.0),0) as %s from LogRecord.dbo.account_lilun_distinct_acname a inner join p_follow p on a.acname=p.F_ac and p.AC='%s' inner join symbol_id s_id on p.stock=s_id.S_ID and len(s_id.Symbol)<3  inner join  LogRecord.dbo.test_margin mr on mr.symbol=s_id.Symbol  group by date order by date" % (type, acname)
	print sql
	df1=pd.read_sql(sql,conn)
	df1=df1.fillna(0)
	df1[acname]=df1[type].cumsum()
	df1.index=df1['date']
	df1=df1[[acname]]
	return df1


def get_tradeday_list():
	sql="select distinct replace(CONVERT(nvarchar,stockdate,102),'.','') as date from TSymbol_allfuture where symbol='RB' and stockdate>='2016-12-01' and T<='21:00' and T>='09:00' order by  replace(CONVERT(nvarchar,stockdate,102),'.','') "
	daylist=pd.read_sql(sql,conn)
	daylist.index=daylist['date']
	return daylist








stepmultilist=['StepMultigaosheng1','StepMultiI300w_up','StepMultituji1','StepMultituji2','StepMultituji3','StepMultidnhiboth','StepMultidnhiprofit','StepMultidnhisharp','StepMultidnshort','newtuji300']
type='zhuli'
totalpd=[]
#totalpd.append(get_tradeday_list())
for item in stepmultilist:
	a=get_df_acname_type(item, type)
	totalpd.append(a)

aa=pd.concat(totalpd,axis=1)
aa=aa.fillna(method='ffill')
aa.to_csv(r'E:\test\%s.csv' % (type))




