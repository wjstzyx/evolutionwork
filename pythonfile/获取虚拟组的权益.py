#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-
def write_list_ro_csv(csvfile,contentlist):
	with open(csvfile, 'wb') as f:
	    for item1 in contentlist:
	        line = ','.join(item1) + '\n'
	        f.write(line.encode('utf-8'))	

def add_time_series(totalquanyi,res1):
	totalquanyitime=[k[0] for k in totalquanyi]
	res1time=[k[0] for k in res1]
	totalquanyidict={}
	for item in totalquanyi:
		totalquanyidict[item[0]]=item[1]
	res1dict={}
	for item in res1:
		res1dict[item[0]]=item[1]
	daylist=list(set(totalquanyitime).union(set(res1time)))
	daylist=sorted(daylist)
	totalquanyilastvalue=0
	res1lastvalues=0
	result={}
	for item in daylist:
		tempvalue=0
		if item in totalquanyitime:
			totalquanyilastvalue=totalquanyidict[item]
		if item in res1time:
			res1lastvalues=res1dict[item]
		tempvalue=float(totalquanyilastvalue)+float(res1lastvalues)
		result[item]=tempvalue
	result=sorted(result.iteritems(), key=lambda d:d[1], reverse = False)
	return result



def order_get_ac_ratio_three(account):
	#获取总账户配置的虚拟组的ratio
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	#sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  [LogRecord].[dbo].[order_p_follow] WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100 FROM   Emp         INNER JOIN [LogRecord].[dbo].[order_p_follow] d ON d.ac = Emp.F_ac)SELECT AC,f_AC,ratio FROM  Emp" % (account)
	#sql="select AC,f_AC,ratio from [LogRecord].[dbo].[order_p_follow] where ac='%s'" % (account)
	#检测是否自循环
	sql="select * from [Future].[dbo].[p_follow]  where ac=F_ac and ac='%s'" % (account)
	res=ms.dict_sql(sql)
	if res:
		return []
	sql="WITH Emp AS ( SELECT ac,F_ac,ratio,stock FROM  [Future].[dbo].[p_follow] WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100,D.stock FROM   Emp         INNER JOIN [Future].[dbo].[p_follow] d ON d.ac = Emp.F_ac)     select '%s' as AC,f_AC+'__'+stock as f_AC,SUM(ratio) as ratio from Emp where  f_ac not in (select ac from Emp)  and ratio<>0 group by F_ac,stock order by F_ac" % (account,account)
	#sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  [Future].[dbo].[p_follow] WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100 FROM   Emp         INNER JOIN [Future].[dbo].[p_follow] d ON d.ac = Emp.F_ac)     select '%s' as AC,f_AC,SUM(ratio) as ratio from Emp where  f_ac not in (select ac from Emp)  and ratio<>0 group by F_ac" % (account,account)
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


def order_get_dailyquanyi_margin(account,fromDdy):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	ac_ratio=order_get_ac_ratio_three(account)
	totalquanyi=[]
	#获取对齐时间
	Dlist=[]
	tempresult=""
	configinfo=[]
	Dlist.append(fromDdy)
	if ac_ratio==[]:
		return {"ispass":0,"result":"存在有自己跟随自己的配置，请修正"}
	if ac_ratio=={}:
		return {"ispass":0,"result":"P_follow中不存在相应配置，请确认是否正确"}
	for key in ac_ratio:
		realac=key.split("__")[0]
		quanyisymbols_id=key.split("__")[-1]
		sql="select top(1) [positionsymbol] from [LogRecord].[dbo].[quanyicaculatelist]  where acname='%s'" % (realac)
		res11=ms.dict_sql(sql)
		if res11:
			positionsymbol=res11[0]['positionsymbol']
		else:
			return {"ispass":0,"result":"虚拟组权益没有准备，请联系俞洋--%s" % (realac)}
		sql="select  a.acname,s.S_ID,s.Symbol from LogRecord.dbo.quanyicaculatelist a left join Symbol_ID s on a.quanyisymbol=s.Symbol where a.acname='%s' and  s.S_ID='%s'" % (realac,quanyisymbols_id)
		quanyisymbol=ms.dict_sql(sql)[0]['Symbol']
		sql="SELECT top 1  (convert(int,replace(convert(varchar(10),DATEADD(day,1,stockdate),120),'-',''))-20000000) as D  FROM [Future].[dbo].[quanyi_log_groupby_v2] where ac='%s' and symbol='%s' order by stockdate" % (realac,positionsymbol)
		# or
		sql="select top 1 D from dailyquanyi_V2 where ac='%s' and symbol='%s' and not (position=0 and quanyi=0 and times=0) order by D" % (realac,positionsymbol)
		tempD=ms.dict_sql(sql)
		if tempD:
			Dlist.append(tempD[0]['D'])
			configinfo.append([key,ac_ratio[key],tempD[0]['D']])
		else:
			Dlist.append(200000)
			sql="select ac from [LogRecord].[dbo].[order_p_follow]  where F_ac='%s' and stock='%s'" % (realac,quanyisymbol)
			tempres=ms.dict_sql(sql)
			tempresult=tempresult+" 基本账户 %s 中 %s 没有产生过信号,请补全近两年策略信号</br>" % (tempres[0]['ac'],key)
			configinfo.append([key,ac_ratio[key],200000])
	fromDdy=max(Dlist)
	if 200000 in Dlist:
		return {"ispass":0,"result":tempresult,"configinfo":configinfo}

		
	for key in ac_ratio:

		realac=key.split("__")[0]
		quanyisymbols_id=key.split("__")[-1]
		sql="select  a.acname,s.S_ID,s.Symbol from LogRecord.dbo.quanyicaculatelist a left join Symbol_ID s on a.quanyisymbol=s.Symbol where a.acname='%s' and  s.S_ID='%s'" % (realac,quanyisymbols_id)
		quanyisymbol=ms.dict_sql(sql)[0]['Symbol']


		ratio=ac_ratio[key]
		if ratio<>0:
			sql="SELECT [quanyisymbol]  FROM [LogRecord].[dbo].[quanyicaculatelist] where acname='%s' and quanyisymbol='%s'" % (realac,quanyisymbol)
			res=ms.dict_sql(sql)
			if not res:
				# print {"ispass":0,"result":"%s does not has equity" % (key)}
				return {"ispass":0,"result":"%s 不在配置表 quanyicaculatelist 中，请加上并获得历史信号" % (key),"configinfo":configinfo}
			else:
				symbol=res[0]['quanyisymbol']
				acname=realac
				sql="select top 1 D,quanyi as  quanyia from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,fromDdy)
				tempres=ms.find_sql(sql)
				if tempres==[]:
					initoalquanyi=0
				else:
					initoalquanyi=tempres[0][1]
				initoalquanyi=0
				sql="select D,(quanyi-(%s)) as  quanyia from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (initoalquanyi,acname,symbol,fromDdy)
				res1=ms.find_sql(sql)
				#乘以ratio
				newres1=[]
				for item in res1:
					newres1.append([item[0],item[1]*ratio/10.0])
				totalquanyi=add_time_series(totalquanyi,newres1)
				totalquanyi=sorted(totalquanyi,key=lambda a :a[0])
	totalquanyi=[[item[1],item[0]] for item in totalquanyi]
				# for item in totalquanyi:
				# 	print item 
	return {"ispass":1,"result":totalquanyi,"configinfo":configinfo}


def order_get_dailyquanyi_forLilun(account,fromDdy):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	ac_ratio=order_get_ac_ratio_three(account)
	totalquanyi=[]
	#获取对齐时间
	Dlist=[]
	tempresult=""
	configinfo=[]
	Dlist.append(fromDdy)
	if ac_ratio==[]:
		return {"ispass":0,"result":"存在有自己跟随自己的配置，请修正"}
	if ac_ratio=={}:
		return {"ispass":0,"result":"P_follow中不存在相应配置，请确认是否正确"}
	for key in ac_ratio:
		realac=key.split("__")[0]
		quanyisymbols_id=key.split("__")[-1]
		sql="select top(1) [positionsymbol] from [LogRecord].[dbo].[quanyicaculatelist]  where acname='%s'" % (realac)
		res11=ms.dict_sql(sql)
		if res11:
			positionsymbol=res11[0]['positionsymbol']
		else:
			return {"ispass":0,"result":"虚拟组权益没有准备，请联系俞洋--%s" % (realac)}
		sql="select  a.acname,s.S_ID,s.Symbol from LogRecord.dbo.quanyicaculatelist a left join Symbol_ID s on a.quanyisymbol=s.Symbol where a.acname='%s' and  s.S_ID='%s'" % (realac,quanyisymbols_id)
		quanyisymbol=ms.dict_sql(sql)[0]['Symbol']
		sql="SELECT top 1  (convert(int,replace(convert(varchar(10),DATEADD(day,1,stockdate),120),'-',''))-20000000) as D  FROM [Future].[dbo].[quanyi_log_groupby_v2] where ac='%s' and symbol='%s' order by stockdate" % (realac,positionsymbol)
		# or
		sql="select top 1 D from dailyquanyi_V2 where ac='%s' and symbol='%s' and not (position=0 and quanyi=0 and times=0) order by D" % (realac,positionsymbol)
		tempD=ms.dict_sql(sql)
		if tempD:
			Dlist.append(tempD[0]['D'])
			configinfo.append([key,ac_ratio[key],tempD[0]['D']])
		else:
			Dlist.append(200000)
			sql="select ac from [LogRecord].[dbo].[order_p_follow]  where F_ac='%s' and stock='%s'" % (realac,quanyisymbol)
			tempres=ms.dict_sql(sql)
			tempresult=tempresult+" 基本账户 %s 中 %s 没有产生过信号,请补全近两年策略信号</br>" % (tempres[0]['ac'],key)
			configinfo.append([key,ac_ratio[key],200000])
	fromDdy=max(Dlist)
	if 200000 in Dlist:
		return {"ispass":0,"result":tempresult,"configinfo":configinfo}

		
	for key in ac_ratio:

		realac=key.split("__")[0]
		quanyisymbols_id=key.split("__")[-1]
		sql="select  a.acname,s.S_ID,s.Symbol from LogRecord.dbo.quanyicaculatelist a left join Symbol_ID s on a.quanyisymbol=s.Symbol where a.acname='%s' and  s.S_ID='%s'" % (realac,quanyisymbols_id)
		quanyisymbol=ms.dict_sql(sql)[0]['Symbol']


		ratio=ac_ratio[key]
		if ratio<>0:
			sql="SELECT [quanyisymbol]  FROM [LogRecord].[dbo].[quanyicaculatelist] where acname='%s' and quanyisymbol='%s'" % (realac,quanyisymbol)
			res=ms.dict_sql(sql)
			if not res:
				# print {"ispass":0,"result":"%s does not has equity" % (key)}
				return {"ispass":0,"result":"%s 不在配置表 quanyicaculatelist 中，请加上并获得历史信号" % (key),"configinfo":configinfo}
			else:
				symbol=res[0]['quanyisymbol']
				acname=realac
				sql="select top 1 D,quanyi as  quanyia from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,fromDdy)
				tempres=ms.find_sql(sql)
				if tempres==[]:
					initoalquanyi=0
				else:
					initoalquanyi=tempres[0][1]
				sql="select D,(quanyi-(%s)) as  quanyia from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (initoalquanyi,acname,symbol,fromDdy)
				res1=ms.find_sql(sql)
				#乘以ratio
				newres1=[]
				for item in res1:
					newres1.append([item[0],item[1]*ratio/10.0])
				totalquanyi=add_time_series(totalquanyi,newres1)
				totalquanyi=sorted(totalquanyi,key=lambda a :a[0])
	totalquanyi=[[item[1],item[0]] for item in totalquanyi]
				# for item in totalquanyi:
				# 	print item 
	return {"ispass":1,"result":totalquanyi,"configinfo":configinfo}


def stepmulti_equity(ac):
	totalquanyiresult=order_get_dailyquanyi_forLilun(ac,150521)
	if totalquanyiresult['ispass']==0:
		message="配置似乎不是很正确，请俞洋检查下配置"
	else:
		result=totalquanyiresult['result']
		selectequates=[item for item in result if  item[1]>'161220']
		fisrtvalue=selectequates[0][0]
		selectequates=[[str(round(item[0]-fisrtvalue,2)),item[1]] for item in selectequates]
		result=selectequates
		csvfile=r'D:\test\tmp\\'+ac+".csv"
		print csvfile
		write_list_ro_csv(csvfile,result)
stepmulti_equity('StepMultidnhiprofit')
stepmulti_equity('StepMultigaosheng1')
stepmulti_equity('StepMultidnhisharp')
stepmulti_equity('StepMultiI300w_up')
stepmulti_equity('StepMultituji3')
stepmulti_equity('StepMultituji2')
stepmulti_equity('StepMultituji1')
def ac_equity():
	sql="select distinct ac,symbol from [Future].[dbo].[dailyquanyi_V2] where D>170101 and symbol='P' "
	res=ms.dict_sql(sql)
	root=r'D:\test\sample'
	for item in res:	
		filename='%s_%s.csv' % (item['ac'],item['symbol'])
		sql="SELECT       [ac]      ,[symbol]      ,str([quanyi])       ,convert(nvarchar,CONVERT(datetime,D,112),111) as D  FROM [Future].[dbo].[dailyquanyi_V2]   where D>=151020 and symbol='%s' and ac ='%s'   order by ac,D" % (item['symbol'],item['ac'])
		res1=ms.find_sql(sql)
		with open(root+"\\"+filename, 'wb') as f:
		    for item1 in res1:
		        line = ','.join(item1) + '\n'
		        f.write(line.encode('utf-8'))

