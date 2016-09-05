#coding:utf-8
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
import time
import math
from django.utils import simplejson
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from dbconn import MSSQL
# ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
# ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")



def st_heart(request):
	data=""
	isres=0
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.POST:
		sttype=request.POST.get("sttype","")
		print sttype
		if sttype=='day':
			sql="SELECT top 15 a.st,a.TradName,b.address,b.stockdate  FROM [Future].[dbo].[Trading_logSymbol] a  inner join(  SELECT [st],address,stockdate   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3 and type in (1,12)  ) b on a.ST=b.st"
		else:
			sql="SELECT top 15 a.st,a.TradName,b.address,b.stockdate  FROM [Future].[dbo].[Trading_logSymbol] a  inner join(  SELECT [st],address,stockdate   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3 and type in (2,12)  ) b on a.ST=b.st"
		res=ms.dict_sql(sql)
		data=res
		if data:
			isres=1
		else:
			isres=2

	return render_to_response('st_heart.html',{
		'data':data,
		'isres':isres
	})	


def st_information(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="SELECT [id],[type],[item],[ismonitor],[starttime],[endtime] FROM [LogRecord].[dbo].[monitorconfig]"
	res=ms.dict_sql(sql)
	data=res
	return render_to_response('st_information.html',{
		'data':data
	})	



def delete_order_p_follow_info(request):
	if request.POST:
		id=request.POST.get('id','')
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		sql="delete from [LogRecord].[dbo].[order_p_follow] where id=%s" % (id)
		ms.insert_sql(sql)
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')



def save_order_p_basic(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 

	if request.POST:
		print request.POST
		data=request.POST.get("data","")
		print data
		data=data.strip('#')
		data=data.split('#')
		isdel=0
		for item in data:
			item=item.strip(',')
			item=item.split(',')
			if len(item)==3:
				if isdel==0:
					sql="delete from [LogRecord].[dbo].[order_p_follow] where ac='%s'" % (item[0])
					ms.insert_sql(sql)
					isdel=1
				sql="insert into [LogRecord].[dbo].[order_p_follow](ac,F_ac,ratio,Pratio) values('%s','%s',%s,%s)" % (item[0],item[1],item[2],item[2])
				ms.insert_sql(sql)
	else:
		print "not post"
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')




def order_account_equity(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="SELECT distinct ac from [LogRecord].[dbo].[order_p_follow] order by ac"
	aclist=ms.dict_sql(sql)
	ICdata=[]
	ispass=0
	tongji={}
	account=""
	res=""
	F_aclist=""
	#开始查询
	if request.POST:
		print request.POST
		whichform=request.POST.get('query','')
		print whichform
		if whichform=='query':
			account=request.POST.get('searchaccount','')
			sql="select ID as myid,row_number()OVER(ORDER BY [AC] DESC) as id,ac,F_ac,ratio from [LogRecord].[dbo].[order_p_follow] where ac='%s' order by F_ac" % (account)
			res=ms.dict_sql(sql)
			sql="select distinct acname as ac from [LogRecord].[dbo].[quanyicaculatelist] order by acname"
			F_aclist=ms.dict_sql(sql)
			return render_to_response('order_account_equity.html',{
				'account':account,
				'res':res,
				'F_aclist':F_aclist,
				'aclist':aclist
			})
		if whichform=='equity':
			account=request.POST.get('account','')
			totalquanyiresult=order_get_dailyquanyi(account,150521)
			if totalquanyiresult['ispass']==0:
				result=totalquanyiresult['result']
				return render_to_response('order_account_equity.html',{
					'aclist':aclist,
					'ispass':ispass,
					'result':result
				})
			else:
				ispass=1
				result=totalquanyiresult['result']	
				(tempday,lilunquanyi,realquanyi)=range_series(result,[])
				tempdict={'acname':account,'symbol':"",'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
				ICdata.append(tempdict)
				tongji=kpi_tongji(lilunquanyi)


	return render_to_response('order_account_equity.html',{
		'ispass':ispass,
		'aclist':aclist,
		'ICdata':ICdata,
		'tongji':tongji,
		'account':account,
		'res':res,
		'F_aclist':F_aclist
	})	





	# ICdata=[]
	# sql="select distinct ac,symbol from dailyquanyi where symbol='IC' and D>151020"
	# res=ms.dict_sql(sql)
	# for item in res:
	# 	acname=item['ac']
	# 	symbol=item['symbol']
	# 	sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
	# 	res1=ms.find_sql(sql)
	# 	sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
	# 	res2=ms.find_sql(sql)		
	# 	(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
	# 	tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
	# 	ICdata.append(tempdict)





def account_equity(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="SELECT [id],[type],[item],[ismonitor],[starttime],[endtime] FROM [LogRecord].[dbo].[monitorconfig]"
	sql="select distinct ac from p_follow order by ac"
	res=ms.dict_sql(sql)
	aclist=res
	ICdata=[]
	ispass=0
	tongji={}
	#开始查询
	if request.POST:
		account=request.POST.get('acname','')
		print account
		totalquanyiresult=get_dailyquanyi(account,150521)
		if totalquanyiresult['ispass']==0:
			result=totalquanyiresult['result']
			return render_to_response('account_equity.html',{
				'aclist':aclist,
				'ispass':ispass,
				'result':result
			})
		else:
			ispass=1
			result=totalquanyiresult['result']

			
			(tempday,lilunquanyi,realquanyi)=range_series(result,[])
			tempdict={'acname':account,'symbol':"",'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
			ICdata.append(tempdict)
			tongji=kpi_tongji(lilunquanyi)

	return render_to_response('account_equity.html',{
		'ispass':ispass,
		'aclist':aclist,
		'ICdata':ICdata,
		'tongji':tongji
	})	





	# ICdata=[]
	# sql="select distinct ac,symbol from dailyquanyi where symbol='IC' and D>151020"
	# res=ms.dict_sql(sql)
	# for item in res:
	# 	acname=item['ac']
	# 	symbol=item['symbol']
	# 	sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
	# 	res1=ms.find_sql(sql)
	# 	sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
	# 	res2=ms.find_sql(sql)		
	# 	(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
	# 	tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
	# 	ICdata.append(tempdict)




def index(request):
	now = datetime.datetime.now()
	t = get_template('myindex.html')
	html = t.render(Context({'current_date': now}))
	return HttpResponse(html)

def adddata(request):
	data=""
	defualtdate=datetime.datetime.now().strftime("%Y%m%d")[2:]
	if request.POST:
		print request.POST
		newD=request.POST.get('datevalue','')
		if len(newD)!=6:
			newD=defualtdate
		defualtdate=newD
		ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
		sql="select a.ac,Convert(decimal(18,1),abs(a.quanyi-a.comm-b.quanyi+b.comm)/(c.pointvalue+0.000001)) as dianshu,a.D,(a.quanyi-a.comm) as backequity,(b.quanyi-b.comm) as realequity from dailyquanyi a left join real_dailyquanyi b on a.ac=b.ac and a.symbol=b.symbol and a.D=b.D and a.D='%s'  inner join [LogRecord].[dbo].[symbolpointvalue] c on a.symbol=c.symbol where a.D='%s' order by dianshu desc" % (newD,newD)
		res=ms.dict_sql(sql)
		data=res
	return render_to_response('realcompare.html',{
		'data':data,
		'defualtdate':defualtdate,
	})	




def acwantedequlitybacktest(request):
	if request.POST:
		id=request.POST.get('id','')
	newD=160621
	RBlist=[]
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 

	RBdata=[]
	sql="select distinct acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where isyepan=0 and iscaculate=1 and isforbacktest=1 order by quanyisymbol"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		RBdata.append(tempdict)



	return render_to_response('acwantedequlitybacktest.html',{
		'RBdata':RBdata,
	})	




def acwantedequlitystock(request):
	if request.POST:
		id=request.POST.get('id','')
	newD=160621
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	IFdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='IF' and D>151020  order by ac"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		IFdata.append(tempdict)

	ICdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='IC' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		ICdata.append(tempdict)

	return render_to_response('acwantedequlitystock.html',{
		'ICdata':ICdata,
		'IFdata':IFdata,
	})	



def acwantedequlity(request):
	if request.POST:
		id=request.POST.get('id','')
	newD=160621
	RBlist=[]

	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	rbdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RB','RBnight') and iscaculate=1 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		rbdata.append(tempdict)

	AGdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='AG' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		AGdata.append(tempdict)

	CUdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='CU' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		CUdata.append(tempdict)

	RUdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='RU' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		RUdata.append(tempdict)

	TAdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='TA' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		TAdata.append(tempdict)

	JDdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='JD' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		if res2==[]:
			tmp=[0,res1[-1][1]]
			res2.append(tmp)

		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		JDdata.append(tempdict)

	BUdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='BU' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		BUdata.append(tempdict)

	CSdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='CS' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		CSdata.append(tempdict)

	HCdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='HC' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		HCdata.append(tempdict)

	Pdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol in ('P','Pnight') and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		Pdata.append(tempdict)

	PPdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='PP' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		PPdata.append(tempdict)

	NIdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol='NI' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		NIdata.append(tempdict)
	
	Idata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol in ('I','Inight') and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		Idata.append(tempdict)

	Mdata=[]
	sql="select distinct ac,symbol from dailyquanyi where symbol in ('M','Mnight') and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		Mdata.append(tempdict)

	return render_to_response('acwantedequlity.html',{
		'rbdata':rbdata,
		'AGdata':AGdata,
		'CUdata':CUdata,
		'RUdata':RUdata,
		'TAdata':TAdata,
		'JDdata':JDdata,
		'BUdata':BUdata,
		'CSdata':CSdata,
		'HCdata':HCdata,
		'Pdata':Pdata,
		'PPdata':PPdata,
		'NIdata':NIdata,
		'Idata':Idata,
		'Mdata':Mdata,
	})	


def acwantedequlitynew(request):
	if request.POST:
		id=request.POST.get('id','')
	newD=160621
	RBlist=[]

	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	rbdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RB','RBnight') and iscaculate in (1,2) order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (tempquanyi,acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		rbdata.append(tempdict)

	AGdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='AG' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		AGdata.append(tempdict)

	CUdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='CU' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		CUdata.append(tempdict)

	RUdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='RU' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		RUdata.append(tempdict)

	TAdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='TA' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		TAdata.append(tempdict)

	JDdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='JD' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		if res2==[]:
			tmp=[0,res1[-1][1]]
			res2.append(tmp)

		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		JDdata.append(tempdict)

	BUdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='BU' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		BUdata.append(tempdict)

	CSdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='CS' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		CSdata.append(tempdict)

	HCdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='HC' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		HCdata.append(tempdict)

	Pdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol in ('P','Pnight') and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		Pdata.append(tempdict)

	PPdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='PP' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		PPdata.append(tempdict)

	NIdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol='NI' and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		NIdata.append(tempdict)
	
	Idata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol in ('I','Inight') and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		Idata.append(tempdict)

	Mdata=[]
	sql="select distinct ac,symbol from dailyquanyi_V2 where symbol in ('M','Mnight') and D>151020"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		Mdata.append(tempdict)

	return render_to_response('acwantedequlity.html',{
		'rbdata':rbdata,
		'AGdata':AGdata,
		'CUdata':CUdata,
		'RUdata':RUdata,
		'TAdata':TAdata,
		'JDdata':JDdata,
		'BUdata':BUdata,
		'CSdata':CSdata,
		'HCdata':HCdata,
		'Pdata':Pdata,
		'PPdata':PPdata,
		'NIdata':NIdata,
		'Idata':Idata,
		'Mdata':Mdata,
	})	






def acwantedequlityforqiu(request):
	if request.POST:
		id=request.POST.get('id','')
	newD=160621
	RBlist=[]

	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	rbdata=[]
	sql="select distinct ac,symbol from dailyquanyi where ac in ('mtr','pzh','cfzh') and D>151020 order by symbol"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		sql="select (quanyi-comm)/d_max as quanyia,D from dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res1=ms.find_sql(sql)
		sql="select (quanyi-comm)/d_max as quanyia,D from real_dailyquanyi where ac='%s' and symbol='%s' and D>=151020 order by D" % (acname,symbol)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		rbdata.append(tempdict)




	return render_to_response('acwantedequlityforqiu.html',{
		'rbdata':rbdata,
	})	




def realcompare(request):
	data=""
	defualtdate=datetime.datetime.now().strftime("%Y%m%d")[2:]
	if request.POST:
		print request.POST
		newD=request.POST.get('datevalue','')
		if len(newD)!=6:
			newD=defualtdate
		defualtdate=newD
		ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
		sql="select a.ac,Convert(decimal(18,1),abs(a.quanyi-a.comm-b.quanyi+b.comm)/(c.pointvalue+0.000001)) as dianshu,a.D,(a.quanyi-a.comm) as backequity,(b.quanyi-b.comm) as realequity from dailyquanyi a left join real_dailyquanyi b on a.ac=b.ac and a.symbol=b.symbol and a.D=b.D and a.D='%s'  inner join [LogRecord].[dbo].[symbolpointvalue] c on a.symbol=c.symbol where a.D='%s' order by dianshu desc" % (newD,newD)
		res=ms.dict_sql(sql)
		data=res
	return render_to_response('realcompare.html',{
		'data':data,
		'defualtdate':defualtdate,
	})	



def showaccompare(requst):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	if requst.GET:
		print "bb"
		print requst.GET
		acname=requst.GET.get('acname','')
	else:
		print "aaaaa"
		acname='Rb_QGpLud'
	#acname='9KDHPM'
	##获取5日前日期
	nowtime=(datetime.datetime.now()-datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
	sql="SELECT top 2000 stockdate,totalposition  FROM [Future].[dbo].[quanyi_log_groupby] where ac='%s' and stockdate>='%s' order by stockdate " % (acname,nowtime)
	print sql
	res1=ms.dict_sql(sql)
	data1=[]
	if res1:
		for item  in res1:
			stockdate=(item['stockdate']+ datetime.timedelta(hours = 8)).strftime("%Y-%m-%d %H:%M:%S")
			timeArray = time.strptime(stockdate, "%Y-%m-%d %H:%M:%S")
			timeStamp = int(time.mktime(timeArray))
			totalposition=round(item['totalposition'],3)
			tempdata1=[timeStamp,totalposition]
			data1.append(tempdata1)
		newdata1=change_scatter_tocontinue(data1)
	else:
		newdata1=[]
	sql="SELECT top 2000 stockdate,totalposition  FROM [Future].[dbo].[real_quanyi_log_groupby] where ac='%s' and stockdate>='%s' order by stockdate " % (acname,nowtime)
	res2=ms.dict_sql(sql)
	data2=[]
	if res2:
		for item  in res2:
			stockdate=(item['stockdate']+ datetime.timedelta(hours = 8)).strftime("%Y-%m-%d %H:%M:%S")
			timeArray = time.strptime(stockdate, "%Y-%m-%d %H:%M:%S")
			timeStamp = int(time.mktime(timeArray))
			totalposition=round(item['totalposition'],3)
			tempdata1=[timeStamp,totalposition]
			data2.append(tempdata1)
		newdata2=change_scatter_tocontinue(data2)
	else:
		newdata2=[]
	return render_to_response('showaccompare.html',{
		'data':acname,
		'data1':newdata1,
		'data2':newdata2,
	})	


def configmonitorlist(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="SELECT [id],[type],[item],[ismonitor],[starttime],[endtime] FROM [LogRecord].[dbo].[monitorconfig]"
	res=ms.dict_sql(sql)
	data=res
	return render_to_response('configmonitorlist.html',{
		'data':data
	})	


def configmailtolist(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="SELECT [id],[name],[email],[istomail]  FROM [LogRecord].[dbo].[mailtolist]"
	res=ms.dict_sql(sql)
	data=res
	return render_to_response('configmailtolist.html',{
		'data':data
	})	

def save_mailto_info(request):
	if request.POST:
		print request.POST
		id=request.POST.get('id','')
		name=request.POST.get('name','')
		email=request.POST.get('email','')
		istomail=request.POST.get('istomail','')
		print id
		print name
		print "post"
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		sql="update [LogRecord].[dbo].[mailtolist] set name='%s',email='%s',istomail=%s where id=%s" % (name,email,istomail,id)
		print 'sql',sql
		ms.insert_sql(sql)

		print sql
	else:
		print "not post"
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')

def add_new_mailto(request):
	if request.POST:
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		sql="insert into [LogRecord].[dbo].[mailtolist](name,email,istomail) values('请输入姓名','',0)"
		ms.insert_sql(sql)
		print 333333333
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')


def delete_mailto_info(request):
	if request.POST:
		id=request.POST.get('id','')
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		sql="delete from  [LogRecord].[dbo].[mailtolist] where id=%s" % (id)
		ms.insert_sql(sql)
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')


def save_monitor_info(request):
	if request.POST:
		print request.POST
		id=request.POST.get('id','')
		type=request.POST.get('type','')
		item=request.POST.get('item','')
		ismonitor=request.POST.get('ismonitor','')
		starttime=request.POST.get('starttime','')
		endtime=request.POST.get('endtime','')
		print type,item,ismonitor,starttime,endtime
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		sql="update [LogRecord].[dbo].[monitorconfig] set type='%s',item='%s',ismonitor=%s,starttime='%s',endtime='%s' where id=%s" % (type,item,ismonitor,starttime,endtime,id)
		print 'sql',sql
		ms.insert_sql(sql)

		print sql
	else:
		print "not post"
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')

def add_new_monitor(request):
	if request.POST:
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		sql="insert into [LogRecord].[dbo].[monitorconfig](type,item,ismonitor,starttime,endtime) values('请输入','',0,'21:00:00','23:00:00')"
		ms.insert_sql(sql)
		print 333333333
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')


def delete_monitor_info(request):
	if request.POST:
		id=request.POST.get('id','')
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		sql="delete from  [LogRecord].[dbo].[monitorconfig] where id=%s" % (id)
		ms.insert_sql(sql)
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')




###function
##变化点位变成连续点位
def change_scatter_tocontinue(datalist,delta=60):
	newdatalist=[]
	newdatalist.append(datalist[0][:])
	print newdatalist
	lastdate=datalist[0][:]
	for item in datalist[1:]:
		while (item[0]-lastdate[0])>60:
			lastdate[0]=lastdate[0]+60
			newdatalist.append([lastdate[0],lastdate[1]])
		newdatalist.append(item)
		lastdate=item[:]
	return newdatalist

#变化量变成累积量
def change_delta_toaccumu(datalist1,datalist2):
	realquanyi=[]
	lilunquanyi=[]
	daylist=[]
	if datalist2==[]:
		for item in datalist1:
			daylist.append(int(item[1]))
			lilunquanyi.append(item[0])
		lastvalue=0
		for i in range(len(lilunquanyi)):
			totalvalue=lilunquanyi[i]+lastvalue
			lilunquanyi[i]=totalvalue
			lastvalue=totalvalue
		datalist2=[]
		return (daylist,lilunquanyi,realquanyi)
	comp1=datalist1[0][1]
	comp2=datalist2[0][1]
	if int(comp1)<=int(comp2):
		fisrtlist=datalist1[:]
		secondlist=datalist2[:]
	else:
		fisrtlist=datalist2[:]
		secondlist=datalist1[:]
	secondi=0
	for i in range(len(fisrtlist)):
		if secondlist[0][1]==fisrtlist[i][1]:
			secondi=i
			break
	for i in range(secondi):
		realquanyi.append(0)
	for item in fisrtlist:
		daylist.append(int(item[1]))
		lilunquanyi.append(item[0])
	for item in secondlist:
		realquanyi.append(item[0])
	lastvalue=0
	for i in range(len(lilunquanyi)):
		totalvalue=lilunquanyi[i]+lastvalue
		lilunquanyi[i]=totalvalue
		lastvalue=totalvalue
	lastvalue=0
	for i in range(len(realquanyi)):
		totalvalue=realquanyi[i]+lastvalue
		realquanyi[i]=totalvalue
		lastvalue=totalvalue
	return (daylist,lilunquanyi,realquanyi)


#对齐两个时间序列
def range_series(datalist1,datalist2):
	datalist1day=[k[1] for k in datalist1]
	datalist2day=[k[1] for k in datalist2]
	data1list={}
	for item in datalist1:
		data1list[item[1]]=item[0]
	data2list={}
	for item in datalist2:
		data2list[item[1]]=item[0]
	daylist=list(set(datalist1day).union(set(datalist2day)))
	daylist=sorted(daylist)
	realquanyi=[]
	lilunquanyi=[]
	datalist1last=0
	datalist2last=0
	for item in daylist:
		if item in datalist1day:
			lilunquanyi.append(data1list[item])
			datalist1last=data1list[item]
		else:
			lilunquanyi.append(datalist1last)

		if item in datalist2day:
			realquanyi.append(data2list[item])
			datalist2last=data2list[item]
		else:
			realquanyi.append(datalist2last)
	daylist=[int(k) for k in daylist]
	# print daylist
	# print realquanyi
	# print  lilunquanyi
	return (daylist,lilunquanyi,realquanyi)


#获得一个账号配置的所有虚拟组
def get_ac_ratio(account):
	#获取总账户配置的虚拟组的ratio
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  p_follow WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100 FROM   Emp         INNER JOIN p_follow d ON d.ac = Emp.F_ac)SELECT AC,f_AC,ratio FROM  Emp" % (account)
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

#获得账号点菜系统虚拟组
def order_get_ac_ratio(account):
	#获取总账户配置的虚拟组的ratio
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	#sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  p_follow WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100 FROM   Emp         INNER JOIN p_follow d ON d.ac = Emp.F_ac)SELECT AC,f_AC,ratio FROM  Emp" % (account)
	sql="select AC,f_AC,ratio from [LogRecord].[dbo].[order_p_follow] where ac='%s'" % (account)
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


#计算总权益
def get_dailyquanyi(account,fromDdy):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	ac_ratio=get_ac_ratio(account)
	totalquanyi=[]
	for key in ac_ratio:
		ratio=ac_ratio[key]
		if ratio>0:
			sql="SELECT [quanyisymbol]  FROM [LogRecord].[dbo].[quanyicaculatelist] where acname='%s'" % (key)
			res=ms.dict_sql(sql)
			if not res:
				# print {"ispass":0,"result":"%s does not has equity" % (key)}
				return {"ispass":0,"result":"%s does not has equity" % (key)}
			else:
				symbol=res[0]['quanyisymbol']
				acname=key
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
	return {"ispass":1,"result":totalquanyi}


#计算总权益(点菜)
def order_get_dailyquanyi(account,fromDdy):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	ac_ratio=order_get_ac_ratio(account)
	totalquanyi=[]
	#获取对齐时间
	Dlist=[]
	Dlist.append(fromDdy)
	for key in ac_ratio:
		sql="SELECT top 1  (convert(int,replace(convert(varchar(10),DATEADD(day,1,stockdate),120),'-',''))-20000000) as D  FROM [Future].[dbo].[quanyi_log_groupby_v2] where ac='%s' order by stockdate" % (key)
		tempD=ms.dict_sql(sql)
		if tempD:
			Dlist.append(tempD[0]['D'])
		else:
			Dlist.append(200000)
	fromDdy=max(Dlist)
	print Dlist
		
	for key in ac_ratio:
		ratio=ac_ratio[key]
		if ratio>0:
			sql="SELECT [quanyisymbol]  FROM [LogRecord].[dbo].[quanyicaculatelist] where acname='%s'" % (key)
			res=ms.dict_sql(sql)
			if not res:
				# print {"ispass":0,"result":"%s does not has equity" % (key)}
				return {"ispass":0,"result":"%s does not has equity" % (key)}
			else:
				symbol=res[0]['quanyisymbol']
				acname=key
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
	return {"ispass":1,"result":totalquanyi}



#两个时间序列相加
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

#统计计算
def kpi_tongji(lilunquanyi):
	Net_Profit=0
	Max_Drawdown=0
	Days=0
	Day_Winrate=0
	Daily_Std=0
	Ann_Sharpe=0
	Max_Day_Profit=0
	Max_Day_Loss=0
	Max_Win_Days=0
	Max_Loss_Days=0
	Max_Day_to_New_High=0
	deltavalue=[]
	lastvalue=0
	for item in lilunquanyi:
		tempdelta=item-lastvalue
		deltavalue.append(tempdelta)
		lastvalue=item
	Net_Profit=lilunquanyi[-1]
	Days=len(lilunquanyi)
	meandayliay=lilunquanyi[-1]/Days
	total2=0
	windays=0
	lossdays=0
	winlength=0
	losslength=0
	lastvalue=0
	for item in deltavalue:
		temp1=(meandayliay-item)*(meandayliay-item)
		total2=total2+temp1
		if item>=0:
			windays=windays+1
			losslength=0
			winlength=winlength+1
		else:
			lossdays=lossdays+1
			winlength=0
			losslength=losslength+1
		if winlength>Max_Win_Days:
			Max_Win_Days=winlength
		if losslength>Max_Loss_Days:
			Max_Loss_Days=losslength
	if Days<=2:
		totalday=1
	sharpeA=meandayliay
	sharpeB=total2/float(Days)
	Ann_Sharpe=sharpeA/math.sqrt(sharpeB-sharpeA*sharpeA)
	Ann_Sharpe=round(Ann_Sharpe,3)
	Daily_Std=math.sqrt(total2/(Days-1))
	Daily_Std=round(Daily_Std,2)
	Max_Day_Profit=max(deltavalue)
	Max_Day_Loss=min(deltavalue)
	Day_Winrate=windays/float(windays+lossdays)
	Day_Winrate=round(Day_Winrate,3)
	highvalue=0
	tempi=0
	tempdrowdown=0
	temphigh=0
	for item in lilunquanyi:
		if item>temphigh:
			temphigh=item
		tempdrowdown=temphigh-item
		if tempdrowdown>Max_Drawdown:
			Max_Drawdown=tempdrowdown
		if item>highvalue:
			highvalue=item
			tempi=0
		tempi=tempi+1
		if tempi>Max_Day_to_New_High:
			Max_Day_to_New_High=tempi
	result={"Net_Profit":Net_Profit,"Max_Drawdown":Max_Drawdown,"Days":Days,"Day_Winrate":Day_Winrate,"Daily_Std":Daily_Std,"Ann_Sharpe":Ann_Sharpe,"Max_Day_Profit":Max_Day_Profit,"Max_Day_Loss":Max_Day_Loss,"Max_Win_Days":Max_Win_Days,"Max_Loss_Days":Max_Loss_Days,"Max_Day_to_New_High":Max_Day_to_New_High}
	print result
	return result



