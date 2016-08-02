#coding:utf-8
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
import time
from django.utils import simplejson
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from dbconn import MSSQL
# ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
# ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")


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
		sql="select quanyi-%s as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=151020 order by D" % (tempquanyi,acname,symbol)
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



