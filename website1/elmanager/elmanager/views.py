#coding:utf-8
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
import time
import csv
import math
from django.utils import simplejson
import hashlib
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from dbconn import MSSQL
# ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
# ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")


def account_lilun_distinct(request):
	data=""
	isres=0
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.POST:
		sttype=request.POST.get("sttype","")
		print sttype
		if sttype=='day':
			sql="SELECT top 400 a.st,a.TradName,b.address,b.stockdate  FROM [Future].[dbo].[Trading_logSymbol] a  inner join(  SELECT [st],address,stockdate   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3 and type in (1,12)  ) b on a.ST=b.st"
		else:
			sql="SELECT top 400 a.st,a.TradName,b.address,b.stockdate  FROM [Future].[dbo].[Trading_logSymbol] a  inner join(  SELECT [st],address,stockdate   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3 and type in (2,12)  ) b on a.ST=b.st"
		res=ms.dict_sql(sql)
		data=res
		if data:
			isres=1
		else:
			isres=2

	return render_to_response('account_lilun_distinct.html',{
		'data':data,
		'isres':isres
	})	


def realshowmonitor_huifu(request):
	if request.POST:
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		id=request.POST.get("date","")
		sql="update [LogRecord].[dbo].[all_monitor_info] set isactive=1 where id=%s" % (id)
		ms.insert_sql(sql)
	result={'res1':1}
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')



def realshowmonitor_hulue(request):
	if request.POST:
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		id=request.POST.get("date","")
		sql="update [LogRecord].[dbo].[all_monitor_info] set isactive=0 where id=%s" % (id)
		ms.insert_sql(sql)
	result={'res1':1}
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')




def realshowmonitor_newalert(request):
	ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	sql="SELECT a.id,a.[type],a.[item]+'_'+b.Symbol as item  ,a.[msg], b.Symbol,classcode ,convert(nvarchar,[inserttime],120) as updatetime FROM [LogRecord].[dbo].[all_monitor_info] a inner join symbol_id b on substring(a.item,CHARINDEX('_',a.item)+1,3)=b.S_ID and len(b.Symbol)<3 where isactive=1 and issolved=0 order by updatetime "
	res1=ms.dict_sql(sql)
	sql="SELECT top 50 a.id,a.[type],a.[item]+'_'+b.Symbol as item  ,a.[msg], b.Symbol,classcode ,convert(nvarchar,[inserttime],120) as updatetime FROM [LogRecord].[dbo].[all_monitor_info] a inner join symbol_id b on substring(a.item,CHARINDEX('_',a.item)+1,3)=b.S_ID and len(b.Symbol)<3 where isactive=1 and issolved=1  order by updatetime desc"
	res_solved=ms.dict_sql(sql)
	sql="SELECT a.id,a.[type],a.[item]+'_'+b.Symbol as item  ,a.[msg], b.Symbol,classcode ,convert(nvarchar,[inserttime],120) as updatetime FROM [LogRecord].[dbo].[all_monitor_info] a inner join symbol_id b on substring(a.item,CHARINDEX('_',a.item)+1,3)=b.S_ID and len(b.Symbol)<3 where isactive=0 and issolved=0  order by updatetime desc"
	res_noactive=ms.dict_sql(sql)

	result={'res1':res1,'res_solved':res_solved,'res_noactive':res_noactive}
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')

def rt_newalert(request):
	ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	sql="SELECT a.id,a.[type],a.[item],a.[msg],'symbol' as symbol, classcode ,convert(nvarchar,[inserttime],120) as updatetime FROM [LogRecord].[dbo].[all_monitor_info] a where type='Account' and isactive=1 and issolved=0 order by updatetime "
	account_distinct=ms.dict_sql(sql)

	sql="SELECT a.id,a.[type],a.[item],a.[msg],'symbol' as symbol, classcode ,convert(nvarchar,[inserttime],120) as updatetime FROM [LogRecord].[dbo].[all_monitor_info] a where type='Thunder' and isactive=1 and issolved=0 order by updatetime "
	Thunder=ms.dict_sql(sql)

	sql="SELECT a.id,a.[type],a.[item],a.[msg],'symbol' as symbol, classcode ,convert(nvarchar,[inserttime],120) as updatetime FROM [LogRecord].[dbo].[all_monitor_info] a where type='quotes' and isactive=1 and issolved=0 order by updatetime "
	quotes=ms.dict_sql(sql)

	sql="SELECT a.id,a.[type],a.[item],a.[msg],'symbol' as symbol, classcode ,convert(nvarchar,[inserttime],120) as updatetime FROM [LogRecord].[dbo].[all_monitor_info] a where type='AB' and isactive=1 and issolved=0 order by updatetime "
	AB=ms.dict_sql(sql)



	result={'account_distinct':account_distinct,'Thunder':Thunder,'quotes':quotes,'AB':AB}
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')




def realshowmonitor(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	#获取没有解决的问题
	sql="SELECT id, [type],[item] ,[msg], classcode ,[updatetime]FROM [LogRecord].[dbo].[all_monitor_info] where isactive=1 and issolved=0 order by updatetime "
	res1=ms.dict_sql(sql)


	return render_to_response('realshowmonitor.html',{
		'data':'',
		'lilunres':'',
		'res1':res1,
		# 'realres':realres,


	})	



def rt(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	#获取没有解决的问题
	sql="SELECT id, [type],[item] ,[msg], classcode ,[updatetime]FROM [LogRecord].[dbo].[all_monitor_info] where isactive=1 and issolved=0 order by updatetime "
	res1=ms.dict_sql(sql)


	return render_to_response('rt.html',{
		'data':'',
		'lilunres':'',
		'res1':res1,
		# 'realres':realres,


	})	




def distinct_cplus_ab(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.GET:
		sttype=request.GET.get("st","")
		print sttype
		symbol=sttype.split('@')[0]
		s_id=sttype.split('@')[1]
		type=sttype.split('@')[2]
		if type=='jieti1':
			ac_count="StepMultiI300w"
		if type=='jieti2':
			ac_count="StepMulti2"
		if type=='tuji1':
			ac_count="StepMultituji1"

		sql="select p,st,tradetime,TradName from Trading_logSymboltest where st in (select st from P_BASIC_cplus where ac in ( select f_ac from p_follow where ac='%s' and stock='%s')) order by p" % (ac_count,s_id)
		realres=ms.dict_sql(sql)
		sql="select p,st,tradetime,TradName from for_backtest_Trading_logSymbol where st in (select st from P_BASIC where ac in ( select f_ac from p_follow where ac='%s' and stock='%s')) order by p" % (ac_count,s_id)
		lilunres=ms.dict_sql(sql)



	return render_to_response('distinct_cplus_ab.html',{
		'data':'',
		'lilunres':lilunres,
		'realres':realres,


	})	



def st_heart_analysis(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.GET:
		sttype=request.GET.get("st","")
		print sttype
		# sql="SELECT TOP 100    [st]     ,[computername]    ,convert(nvarchar,[stockdate],120) as stockdate  ,[p]    ,[signCON]   ,[Period]     ,[Timenum]    ,[baropen]    ,[barhigh]    ,[barlow]     ,[barclose]    ,[barvolume]     ,[symbol]   FROM [LogRecord].[dbo].[cache_st_heart] where st='%s' order by stockdate desc" % (sttype)
		# realres=ms.dict_sql(sql)
		sql="SELECT TOP 100    [st]     ,[computername]    ,convert(nvarchar,[stockdate],120) as stockdate    ,[p]    ,[signCON]   ,[Period]     ,[Timenum]    ,[baropen]    ,[barhigh]    ,[barlow]     ,[barclose]    ,[barvolume]     ,[symbol]   FROM [LogRecord].[dbo].[backtest_cache_st_heart] where st='%s' order by stockdate desc" % (sttype)
		lilunres=ms.dict_sql(sql)













	return render_to_response('st_heart_analysis.html',{
		'data':'',
		'lilunres':lilunres,
		# 'realres':realres,


	})	




def jieti_st_position(request):
	data=""
	whichtype=0
	res1=""
	res2=""
	res3=""
	res11=""
	res21=""
	res31=""
	sttype=""
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.POST:
		sttype=request.POST.get("sttype","")
		print sttype
		if sttype=="jieti1":
			sql=" select *from (  select mmk.*,symbol_id.S_ID from ( select sum(t.P) as sump_number,round(sum(t.P*ma.ratio),0) as ratio,t.symbol from (   select pb.st,pb.p_size*ac.ratio/100 as ratio from p_follow p inner join p_basic_cplus pb on p.F_ac=pb.ac and p.AC='StepMultiI300w'   inner join AC_RATIO ac on p.F_ac=ac.AC) ma   left join  [Future].[dbo].[Trading_logSymbolTest] t on   ma.st=t.ST   where t.typeac='stair1'   group by t.symbol  )mmk inner join symbol_id on mmk.symbol=symbol_id.Symbol  ) ja full outer join ( select sum(st.P) as ab_sump_number,round(sum(st.P*sma.ratio),0) as ab_ratio,sma.STOCK from (    select spb.st,spb.p_size*sac.ratio/100 as ratio,spb.STOCK from p_follow sp inner join p_basic spb on sp.F_ac=spb.ac and sp.AC='StepMultiI300w'   inner join AC_RATIO sac on sp.F_ac=sac.AC   ) sma    left join  [Future].[dbo].[for_backtest_Trading_logSymbol] st on    sma.st=st.ST   group by sma.STOCK  ) jb on ja.S_ID=jb.STOCK   order by ja.symbol "			

			res1=ms.dict_sql(sql)
			whichtype=1

		if sttype=="jieti2":
			sql=" select *from (  select mmk.*,symbol_id.S_ID from ( select sum(t.P) as sump_number,round(sum(t.P*ma.ratio),0) as ratio,t.symbol from (   select pb.st,pb.p_size*ac.ratio/100 as ratio from p_follow p inner join p_basic_cplus pb on p.F_ac=pb.ac and p.AC='StepMulti2'   inner join AC_RATIO ac on p.F_ac=ac.AC) ma   left join  [Future].[dbo].[Trading_logSymbolTest] t on   ma.st=t.ST   where t.typeac='stair2'   group by t.symbol  )mmk inner join symbol_id on mmk.symbol=symbol_id.Symbol  ) ja full outer join ( select sum(st.P) as ab_sump_number,round(sum(st.P*sma.ratio),0) as ab_ratio,sma.STOCK from (    select spb.st,spb.p_size*sac.ratio/100 as ratio,spb.STOCK from p_follow sp inner join p_basic spb on sp.F_ac=spb.ac and sp.AC='StepMulti2'   inner join AC_RATIO sac on sp.F_ac=sac.AC   ) sma    left join  [Future].[dbo].[for_backtest_Trading_logSymbol] st on    sma.st=st.ST   group by sma.STOCK  ) jb on ja.S_ID=jb.STOCK   order by ja.symbol "
			res1=ms.dict_sql(sql)
			whichtype=1

		if sttype=="tuji1":
			sql=" select *from (  select mmk.*,symbol_id.S_ID from ( select sum(t.P) as sump_number,round(sum(t.P*ma.ratio),0) as ratio,t.symbol from (   select pb.st,pb.p_size*ac.ratio/100 as ratio from p_follow p inner join p_basic_cplus pb on p.F_ac=pb.ac and p.AC='StepMultituji1'   inner join AC_RATIO ac on p.F_ac=ac.AC) ma   left join  [Future].[dbo].[Trading_logSymbolTest] t on   ma.st=t.ST   where t.typeac='tuji1'   group by t.symbol  )mmk inner join symbol_id on mmk.symbol=symbol_id.Symbol  ) ja full outer join ( select sum(st.P) as ab_sump_number,round(sum(st.P*sma.ratio),0) as ab_ratio,sma.STOCK from (    select spb.st,spb.p_size*sac.ratio/100 as ratio,spb.STOCK from p_follow sp inner join p_basic spb on sp.F_ac=spb.ac and sp.AC='StepMultituji1'   inner join AC_RATIO sac on sp.F_ac=sac.AC   ) sma    left join  [Future].[dbo].[for_backtest_Trading_logSymbol] st on    sma.st=st.ST   group by sma.STOCK  ) jb on ja.S_ID=jb.STOCK   order by ja.symbol "
			res1=ms.dict_sql(sql)
			whichtype=1

		if sttype=="jieti2_st_symbol":
			#阶梯2--理论VS实际策略差异
			sql="select t.P,t.tradetime,t.TradName,replace(p.AC,'StepMulti2','') as symbol,t.st from p_follow pf inner join P_BASIC  p on pf.F_ac=p.AC and pf.AC='StepMulti2' left join Trading_logSymbol t on p.ST=t.ST order by p.ac,t.p"
			res1=ms.dict_sql(sql)
			whichtype=2
		if sttype=="jieti1_st_symbol":
			#阶梯2--理论VS实际策略差异
			sql="select t.P,t.tradetime,t.TradName,replace(p.AC,'StepMultiI','') as symbol,t.st from p_follow pf inner join P_BASIC  p on pf.F_ac=p.AC and pf.AC='StepMultiI300w' left join Trading_logSymbol t on p.ST=t.ST order by p.ac,t.p"
			res1=ms.dict_sql(sql)
			whichtype=2
		if sttype=="jieti2_st_name":
			#阶梯2--理论VS实际策略差异
			sql="select t.P,t.tradetime,t.TradName,replace(p.AC,'StepMulti2','') as symbol,t.st from p_follow pf inner join P_BASIC  p on pf.F_ac=p.AC and pf.AC='StepMulti2' left join Trading_logSymbol t on p.ST=t.ST order by t.TradName,t.p"
			res1=ms.dict_sql(sql)
			whichtype=2
		if sttype=="jieti1_st_name":
			#阶梯2--理论VS实际策略差异todays_withdraw
			sql="select t.P,t.tradetime,t.TradName,replace(p.AC,'StepMultiI','') as symbol,t.st from p_follow pf inner join P_BASIC  p on pf.F_ac=p.AC and pf.AC='StepMultiI300w' left join Trading_logSymbol t on p.ST=t.ST order by  t.TradName,t.p"
			res1=ms.dict_sql(sql)
			whichtype=2

		if sttype=="catch_distinct":
			sql="SELECT [stno]      ,aa.Symbol      ,[stname]      ,[ps]      ,[refps]      ,[doing]      ,t.TradName  FROM [LogRecord].[dbo].[jt_strategy_state] a   inner join Trading_logSymbol t   on a.stno=t.ST   inner join symbol_id aa   on a.stockid=aa.S_ID  where ps<>0 and len(aa.Symbol)<=2 order by t.TradName  "
			res1=ms.dict_sql(sql)
			whichtype=3








	return render_to_response('jieti_st_position.html',{
		'data':data,
		'whichtype':whichtype,
		'res1':res1,
		'sttype':sttype,

	})	





def total_monitor(request):
	data=""
	whichtype=0
	res1=""
	res2=""
	res3=""
	res11=""
	res21=""
	res31=""
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.POST:
		sttype=request.POST.get("sttype","")
		if sttype=="day_quotes_lack":
			#日盘行情数据缺失报警
			sql=" select top(200) a.*,t.TradName from (select st,stockdate,timenum,period, [address] ,DATEDIFF(MINUTE, CONVERT(datetime,case when LEN(CAST(timenum as nvarchar))=6 then left(CAST(timenum as nvarchar),2)+':'+SUBSTRING(CAST(timenum as nvarchar),3,2)+':'+RIGHT(CAST(timenum as nvarchar),2) when LEN(CAST(timenum as nvarchar))=5 then left('0'+CAST(timenum as nvarchar),2)+':'+SUBSTRING('0'+CAST(timenum as nvarchar),3,2)+':'+RIGHT('0'+CAST(timenum as nvarchar),2) end,114),convert(datetime,CONVERT(nvarchar,stockdate,114),114)) as mydatediff  from [LogRecord].[dbo].[ST_heart] where type in (1,12) )a  left join Trading_logSymbol t on  a.st=t.ST  where ABS(mydatediff)>a.period+17  order by ABS(mydatediff) desc"
			res1=ms.dict_sql(sql)
			whichtype=1

		if sttype=="night_quotes_lack":
			#夜盘行情数据缺失报警
			sql=" select top(200) a.*,t.TradName from (select st,stockdate,timenum,period, [address] ,DATEDIFF(MINUTE, CONVERT(datetime,case when LEN(CAST(timenum as nvarchar))=6 then left(CAST(timenum as nvarchar),2)+':'+SUBSTRING(CAST(timenum as nvarchar),3,2)+':'+RIGHT(CAST(timenum as nvarchar),2) when LEN(CAST(timenum as nvarchar))=5 then left('0'+CAST(timenum as nvarchar),2)+':'+SUBSTRING('0'+CAST(timenum as nvarchar),3,2)+':'+RIGHT('0'+CAST(timenum as nvarchar),2) end,114),convert(datetime,CONVERT(nvarchar,stockdate,114),114)) as mydatediff  from [LogRecord].[dbo].[ST_heart] where type in (2,12) )a  left join Trading_logSymbol t on  a.st=t.ST  where ABS(mydatediff)>a.period+17  order by ABS(mydatediff) desc"
			res1=ms.dict_sql(sql)
			whichtype=1

		if sttype=="day_quotes_lasttime":
			#日盘行情采集最新时间
			sql="  select DATEDIFF(MINUTE,stockdate,GETDATE()) as mydatediff ,stockdate, Symbol from (  select MAX(stockdate) as stockdate,Symbol,GETDATE() as nowtime from TSymbol group by Symbol) a  where DATEDIFF(MINUTE,stockdate,GETDATE())>2 order by DATEDIFF(MINUTE,stockdate,GETDATE()) desc"
			res=ms.dict_sql(sql)
			sql="SELECT [symbol]  FROM [LogRecord].[dbo].[catch_quotes] where isday in (1,12) and symbol not in ('RMZL')"
			tempres=ms.dict_sql(sql)
			selectsymbol=[]
			for item in tempres:
				selectsymbol.append(item['symbol'])
			selectres=[]
			for item in res:
				if item['Symbol'] in selectsymbol:
					selectres.append(item)
			res1=selectres


			# sql="  select a.stockdate,GETDATE() as nowtime,DATEDIFF(MINUTE,a.stockdate,GETDATE()) as mydatediff ,a.Symbol from (  select MAX(stockdate) as stockdate,Symbol from TSymbol group by Symbol) a   inner join [LogRecord].[dbo].[catch_quotes] b   on a.Symbol=b.symbol    where b.isday in (1,12)   and a.symbol not in ('RMZL') and DATEDIFF(MINUTE,a.stockdate,GETDATE())>2  order by stockdate "
			# res1=ms.dict_sql(sql)
			whichtype=2

		if sttype=="night_quotes_lasttime":
			#日盘行情采集最新时间

			sql="  select DATEDIFF(MINUTE,stockdate,GETDATE()) as mydatediff ,stockdate, Symbol from (  select MAX(stockdate) as stockdate,Symbol,GETDATE() as nowtime from TSymbol group by Symbol) a  where DATEDIFF(MINUTE,stockdate,GETDATE())>2  order by DATEDIFF(MINUTE,stockdate,GETDATE()) desc"
			res=ms.dict_sql(sql)
			sql="SELECT [symbol]  FROM [LogRecord].[dbo].[catch_quotes] where isday =0 and symbol not in ('RMZL')"
			tempres=ms.dict_sql(sql)
			selectsymbol=[]
			for item in tempres:
				selectsymbol.append(item['symbol'])
			selectres=[]
			for item in res:
				if item['Symbol'] in selectsymbol:
					selectres.append(item)
			res1=selectres

			# sql="  select a.stockdate,GETDATE() as nowtime,DATEDIFF(MINUTE,a.stockdate,GETDATE()) as mydatediff ,a.Symbol from (  select MAX(stockdate) as stockdate,Symbol from TSymbol group by Symbol) a   inner join [LogRecord].[dbo].[catch_quotes] b   on a.Symbol=b.symbol    where b.isday=0   and a.symbol not in ('RMZL') and DATEDIFF(MINUTE,a.stockdate,GETDATE())>2  order by stockdate "
			# res1=ms.dict_sql(sql)
			whichtype=2


		if sttype=="time_adjust":
			#夜盘行情数据缺失报警
			sql="SELECT distinct address,abs(DATEDIFF(SECOND,[databasetime],[stockdate])) as mydatediff FROM [LogRecord].[dbo].[ST_heart]   where ABS(DATEDIFF(SECOND,[databasetime],[stockdate]))>=3 order by ABS(DATEDIFF(SECOND,[databasetime],[stockdate])) desc"
			res1=ms.dict_sql(sql)
			whichtype=3

		if sttype=="real_lilun_position":
			real_miss_set,lilun_miss_set,disticnt_set=show_distinct()
			res1={}
			sql="select distinct symbol,s_id from future.dbo.symbol_id where symbol not like '%%night%%'  and symbol not in ('CUN','AUN','AGN','LZL','MEZL','RMZL')"
			res=ms.dict_sql(sql)
			symboldict={}
			for item in res:
				symboldict[item['s_id']]=item['symbol']

			for item in real_miss_set:
				item['stockID']=symboldict[item['stockID']]+"-"+str(item['stockID'])

			for item in lilun_miss_set:
				if item['realstockID'] in symboldict.keys():
					item['realstockID']=symboldict[item['realstockID']]+"-"+str(item['realstockID'])
				else:
					item['realstockID']='error'

			for item in disticnt_set:
				item['realstockID']=symboldict[item['realstockID']]+"-"+str(item['realstockID'])
				# print symboldict[item['stockID']]
			res1['real_miss_set']=real_miss_set
			res1['lilun_miss_set']=lilun_miss_set
			res1['disticnt_set']=disticnt_set	
			nowtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			res1['nowtime']=nowtime

			whichtype=4




	return render_to_response('total_monitor.html',{
		'data':data,
		'whichtype':whichtype,
		'res1':res1,

	})	






def jieti_distinct_position(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="select aaa.*,bbb.address,kkk.positionsymbol from ( select a.p as backtest,b.P as real ,a.tradetime as backtest_time,b.tradetime as real_time,a.st,a.ticknum as backtest_bar,b.TickNum as real_bar,b.TradName from (SELECT p,st,tradetime,TickNum FROM  (select mbb.* from p_follow mpp   inner join P_BASIC maa   on mpp.F_ac=maa.AC and mpp.AC='StepMultiI300w'  inner join [for_backtest_Trading_logSymbol] mbb  on maa.ST=mbb.ST) maa ) a left join ( SELECT p,st ,tradetime,TickNum ,TradName FROM [Future].[dbo].[Trading_logSymbol]) b  on a.st=b.st  where a.p<>b.P) aaa inner join LogRecord.dbo.ST_heart bbb on aaa.ST=bbb.st left join (select positionsymbol,st from  P_BASIC p inner join LogRecord.dbo.quanyicaculatelist pp on p.AC=pp.acname)kkk on aaa.ST=kkk.ST"
	res=ms.dict_sql(sql)
	return render_to_response('jieti_distinct_position.html',{
		'data':1,
		'data1':1,
		'res':res,
	})	


def jieti_position_monitor(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	#sql="select kk.symbol,jj.stock,round(jj.Expr1,0) as real, round(kk.position,0) as backtest from [Future].[dbo].[View_StepMulti300w] jj left join (select cast(right(LEFT(aa.st,5),2) as int) as stock,round(SUM(aa.p*aa.ratio*bb.ratio),4) as position ,bb.Symbol from   [Future].[dbo].[for_backtest_Trading_logSymbol]  aa left join ( select b.S_ID,a.ratio,b.Symbol from [LogRecord].[dbo].[forbacktest_symbol_ratio] a left join Symbol_ID b  on a.symbol=b.Symbol ) bb on cast(right(LEFT(aa.st,5),2) as int)=bb.s_id  group by cast(right(LEFT(aa.st,5),2) as int),bb.Symbol   ) kk on jj.stock=kk.stock order by abs(round(kk.position,0)) desc"
	sql="select kk.symbol,jj.stock,round(jj.Expr1,0) as real, round(kk.position,0) as backtest,round(kk.totalposition,0) as totalposition ,round((abs(kk.position)/kk.totalposition*100),1) as myhpercent from [Future].[dbo].[View_StepMulti300w] jj left join (select cast(right(LEFT(aa.st,5),2) as int) as stock,round(SUM(aa.p*aa.ratio*bb.ratio),4) as position ,bb.Symbol,round(SUM(aa.ratio*bb.ratio),4) as totalposition from  (select mbb.* from p_follow mpp   inner join P_BASIC maa   on mpp.F_ac=maa.AC and mpp.AC='StepMultiI300w'  inner join [for_backtest_Trading_logSymbol] mbb  on maa.ST=mbb.ST) aa left join ( select b.S_ID,a.ratio,b.Symbol from [LogRecord].[dbo].[forbacktest_symbol_ratio] a left join Symbol_ID b  on a.symbol=b.Symbol ) bb on cast(right(LEFT(aa.st,5),2) as int)=bb.s_id  group by cast(right(LEFT(aa.st,5),2) as int),bb.Symbol   ) kk on jj.stock=kk.stock order by ABS(round(kk.position,0)) desc"

	res=ms.dict_sql(sql)
	return render_to_response('jieti_position_monitor.html',{
		'data':1,
		'data1':1,
		'res':res,
	})	




def accountdetail_ac(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==3:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response

	userid='账户为空'
	if request.GET:
		userid=request.GET.get("userid","")
		if '__' in userid:
			muquanyisymbol=userid.split('__')[-1]
			userid=userid.split('__')[0]
		# userid=userid.strip('/')
	#如果是账号则以下逻辑：
	sql="select 1 as aa from p_basic where ac='%s'" % (userid)
	res111=ms.dict_sql(sql)
	resultlist={}
	res={}
	rbdata=[]
	message=""
	if not  res111:
		sql="SELECT [AC]  ,[F_ac]+'__'+CAST(stock as nvarchar) as F_ac  ,stock,bb.Symbol,[ratio],1 as isac  FROM [Future].[dbo].[p_follow] p left join (SELECT *  FROM [Future].[dbo].[Symbol_ID] where (Symbol not like '%%night%%'  and (Symbol not like '%%N' ) and Symbol not like '%%ZL') OR  Symbol='ZN' or Symbol='RMZL') bB  on p.stock=bb.S_ID where ac='%s ' and ratio<>0" % (userid)
		res=ms.dict_sql(sql)
		print 'res',res
		#res是商品的配置信息
		#增加 resstock 映射股指的配置信息
		ms105 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")
		sql="SELECT account as AC ,REVERSE('0'+SUBSTRING(REVERSE([acanme]),2,100)) as F_ac,Symbol,SUM(ratio)*100 as ratio,'股指映射' as isac   FROM [future].[dbo].[account_position_stock_yingshe]   where account='%s'   group by account,REVERSE('0'+SUBSTRING(REVERSE([acanme]),2,100)),symbol" % (userid)
		resstock=ms105.dict_sql(sql)


		for item in res:
			sql="SELECT 1 isac  FROM [Future].[dbo].[p_follow] where ac='%s' " % (item['F_ac'])
			res1=ms.dict_sql(sql)
			if res1:
				item['isac']='账号'
			else:
				item['isac']='虚拟组'


		aclistresult=order_get_ac_ratio_three(userid)
		resultlist={}
		if aclistresult:
			newaclistresult={}
			testnewaclistresult={}
			for key in aclistresult:
				newaclistresult[key.lower().split('__')[0]]=aclistresult[key]
			for key in aclistresult:
				testnewaclistresult[key.lower()]=aclistresult[key]
			aclistresult=testnewaclistresult
			keylist=""
			for key in newaclistresult:
				keylist=keylist+",'"+key+"'"
			keylist=keylist.strip(",")


			sql="select kk.acname+'__'+cast(sss.s_id as nvarchar) as acname,quanyisymbol,case when issumps=0 then pp.position when issumps=1 then 10 end as position from LogRecord.dbo.quanyicaculatelist kk inner join (select round(SUM(p.P_size*a.ratio/100.0),0) as position,p.ac,p.STOCK from p_basic p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.AC in (%s) where p.ac in (%s) group by p.ac,p.STOCK) pp on kk.acname=pp.AC inner join Symbol_ID sss on kk.quanyisymbol=sss.Symbol" % (keylist,keylist)
			#sql="select kk.acname,quanyisymbol,case when issumps=0 then pp.position when issumps=1 then 10 end as position from LogRecord.dbo.quanyicaculatelist kk inner join (select round(SUM(p.P_size*a.ratio/100.0),0) as position,p.ac,p.STOCK from p_basic p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.AC in (%s) where p.ac in (%s) group by p.ac,p.STOCK) pp on kk.acname=pp.AC" % (keylist,keylist)
			tmpres11=ms.dict_sql(sql)
			resultlist={}
			for item in tmpres11:
				resultlist[item['quanyisymbol']]=0
			for item in tmpres11:
				if aclistresult.has_key(item['acname'].lower()):
					resultlist[item['quanyisymbol']]=resultlist[item['quanyisymbol']]+item['position']*aclistresult[item['acname'].lower()]/100.0
					del aclistresult[item['acname'].lower()]
			for key in aclistresult:
				resultlist[key]="此虚拟组没有找到对应手数"
			resultlist=[(key,resultlist[key]) for key in resultlist]
			resultlist.sort(key=lambda x:x[0])
		else:
			resultlist=[('没有配置虚拟组','或虚拟组配置手数为0')]
		if res==[]:
			res=[{'AC':'此账号没有相关配置','F_ac':'请联系小仇','ratio':'账号：'+userid,'isac':''}]
			resultlist=[('没有配置虚拟组','或虚拟组配置手数为0')]
		print 'resultlist',resultlist
		#添加股指映射后的结果
		sql="SELECT account as AC ,Symbol,SUM(ratio) as ratio FROM [future].[dbo].[account_position_stock_yingshe]   where account='%s'  group by account,symbol" % (userid)
		tmepres=ms105.dict_sql(sql)
		for item in tmepres:
			resultlist.append((item['Symbol'],item['ratio']))


		return render_to_response('accountdetail_ac.html',{
			'res':res,
			'resstock':resstock,
			'userid':userid,
			'username':username,
			'resultlist':resultlist,
		})
	#如果是虚拟组：
	else:
		print request.GET
		begintime=request.GET.get("begintime","")
		if begintime:
			begintime=int(request.GET.get("begintime",""))-20000000
			endtime=int(request.GET.get("endtime",""))-20000000
		else:
			begintime=151020
			endtime=200000

		#查看他是否在计算之列：
		if muquanyisymbol:
			sql=" SELECT top 1 * from [LogRecord].[dbo].[quanyicaculatelist] where acname='%s' and [quanyisymbol] in ( select Symbol from Symbol_ID where S_ID='%s')" % (userid,muquanyisymbol)
			myquanyisymbol=ms.dict_sql(sql)[0]['quanyisymbol']
		else:
			myquanyisymbol='nono'

		sql="select top(1) 1 as aa from dailyquanyi_V2 where ac='%s' and symbol='%s'" % (userid,myquanyisymbol)
		res222=ms.dict_sql(sql)
		if res222:
			sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where acname='%s' and quanyisymbol='%s' and iscaculate in (1,2) order by sortnum" % (userid,myquanyisymbol)
			res=ms.dict_sql(sql)
			for item in res:
				acname=item['ac']
				symbol=item['symbol']
				#第一个价格
				sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,begintime)
				tempquanyi=ms.find_sql(sql)
				if tempquanyi==[]:
					tempquanyi=0
				else:
					tempquanyi=tempquanyi[0][0]
				sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s and D<=%s order by D" % (tempquanyi,acname,symbol,begintime,endtime)
				res1=ms.find_sql(sql)
				sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s and D<=%s order by D" % (acname,symbol,begintime,endtime)
				res2=ms.find_sql(sql)		
				(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
				tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
				rbdata.append(tempdict)	
		else:
			message="此虚拟组没有统计表现，请联系俞洋"
		sql="select 1 as aa from p_follow where ac='%s'" % (userid)
		res33=ms.dict_sql(sql)
		if res33:
			message="请检查账号配置！！在p_basic 和p_follow中都存在配置"

		begintime=str(begintime+20000000)
		begintime=begintime[0:4]+'-'+begintime[4:6]+'-'+begintime[6:8]
		endtime=str(endtime+20000000)
		endtime=endtime[0:4]+'-'+endtime[4:6]+'-'+endtime[6:8]
		return render_to_response('detail_ac_chart.html',{
			'res':res,
			'userid':userid,
			'username':username,
			'resultlist':resultlist,
			'message':message,
			'rbdata':rbdata,
			'begintime':begintime,
			'endtime':endtime,

		})








def register(request):
	# if request.method=='POST':
	# 	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	# 	print request.POST
	# 	username=request.POST.get('username','')
	# 	userid=request.POST.get('userid','')
	# 	password=request.POST.get('password','')
	# 	m2=hashlib.md5()
	# 	m2.update(password)
	# 	password=m2.hexdigest()
	# 	if len(userid)>=1:
	# 		sql="insert into [LogRecord].[dbo].[account_user]([username]  ,[password]  ,[groupname]  ,[isactive]  ,[userid]) values('%s','%s','策略人员',1,'%s')" % (username,password,userid)
	# 		ms.insert_sql(sql)
	# 		response = HttpResponse('用户创建成功，请<a href="/index/login/">登录</a>')
	# 	else:
	# 		response = HttpResponse('输入有误')
	# 		#清理cookie里保存username
	# 	response.delete_cookie('username')
	# 	response.delete_cookie('userid')
	# 	return response
	if request.method=='POST':
		response = HttpResponse('注册系统已经关闭')
		return response
	else:
		return render_to_response('register.html',{
				'ispass':0,
				'message':'用户名或者密码错误，请重新登录',
				'username':'正在注册',
				})	




def change_password(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	if len(userid)<=1:
		response = HttpResponseRedirect('/index/login')
		return response

	if request.method=='POST':
		userid = request.COOKIES.get('userid','')
		username = request.COOKIES.get('username','')
		newpassword=request.POST.get('newpassword','')
		m2=hashlib.md5()
		m2.update(newpassword)
		newpassword=m2.hexdigest()
		if len(userid)>=1:
			sql="update top(1) [LogRecord].[dbo].[account_user] set password='%s' where userid='%s'" % (newpassword,userid)
			ms.insert_sql(sql)
			response = HttpResponse('密码修改成功，请返回重新登录')
		else:
			response = HttpResponse('用户未登录，请重新登录')
			#清理cookie里保存username
		response.delete_cookie('username')
		response.delete_cookie('userid')
		return response
	else:
		return render_to_response('change_password.html',{
				'ispass':0,
				'message':'用户名或者密码错误，请重新登录',
				'username':username,
				})	




def mylogout(req):
	response = HttpResponseRedirect('/index/login')
	#清理cookie里保存username
	response.delete_cookie('username')
	response.delete_cookie('userid')
	return response

def mylogin(request):
	if request.method=='POST':
		userid=request.POST.get("form-username","")
		password=request.POST.get("form-password","")

		m2=hashlib.md5()
		m2.update(password)
		password=m2.hexdigest()
		#获取的表单数据与数据库进行比较（验证密码是否正确）
		ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
		sql="select username,password,userid from [LogRecord].[dbo].[account_user] where userid='%s' and password='%s' and isactive=1" % (userid,password)
		res=ms.dict_sql(sql)
		if len(res)==1:
			username=res[0]['username']
			#比较成功，跳转index
			response = HttpResponseRedirect('/index/')
			#将username写入浏览器cookie,失效时间为3600
			response.set_cookie('userid',userid,3600)
			response.set_cookie('username',username,3600)
			return response
		else:
			#比较失败，还在login
			return render_to_response('mylogin.html',{
					'ispass':0,
					'message':'用户名或者密码错误，请重新登录',
					})	


	RBdata=0
	return render_to_response('mylogin.html',{
		'RBdata':RBdata,
		'ispass':1,
	})	





def futureaccountone(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==3:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response

	userid='账户为空'
	mybegintime=19900101
	myendtime=20200000
	if request.GET:
		userid=request.GET.get("userid","")
		mydate=request.GET.get("mydate","")
		mybegintime=request.GET.get("mybegintime","")
		myendtime=request.GET.get("myendtime","")
		if myendtime<mybegintime:
			response = HttpResponse("结束时间小于开始时间，无法显示，请返回")
			return response

	# res.reverse()
	data=[]
	acname=userid
	symbol=""
	rbdata=[]
	rbdata1=[]
	#画出盈亏的每天统计图

	sql="select date,deposit,Withdraw,CloseBalance,Commission from [LogRecord].[dbo].[AccountsBalance] where userid='%s'  order by date" % (userid)
	res=ms.dict_sql(sql)
	allequates=[]
	selectequates=[]
	selectequatesallquanyi=[]

	if mybegintime=="" or myendtime=="":
		mybegintime=19900101
		myendtime=20200000




	if res:
		last_closebalance=res[0]['CloseBalance']
		last_withdraw=res[0]['Withdraw']
		for item in res:
			date=item['date']
			equity=item['CloseBalance']+item['Withdraw']
			commission=item['Commission']
			daily_equity=(item['CloseBalance']+item['Withdraw']-item['deposit'])-(last_closebalance)
			daily_ratio=daily_equity/(last_closebalance+last_withdraw+0.00002)*100
			last_closebalance=item['CloseBalance']
			last_withdraw=item['Withdraw']
			tempcon=[date,round(equity,1),round(commission,1),round(daily_equity,1),round(daily_ratio,2)]
			allequates.append(tempcon)
		data=allequates[:]
		data.reverse()
		#计算画图用的数据
		firsttime=allequates[0][0]
		lasttime=allequates[-1][0]


		selectequates=[item for item in allequates if item[0]>=int(mybegintime)]
		selectequates=[item for item in selectequates if item[0]<=int(myendtime)]
		# fisrtvalue=selectequates[0][3]
		fisrtvalue=0
		selectequatesallquanyi=[[item[1],item[0]] for item in selectequates]
		selectequates=[[item[3]-fisrtvalue,item[0]] for item in selectequates]
		selectequates[0][0]=0
		mybegintime=selectequates[0][1]
		myendtime=selectequates[-1][1]



	sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='nnnnnnnnnnnn'"
	res2=ms.find_sql(sql)
	(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(selectequates,res2)
	(tempday1,lilunquanyi1,realquanyi1)=range_series(selectequatesallquanyi,res2)	
	tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
	tempdict1={'acname':acname,'symbol':symbol,'xaxis':tempday1,'lilunquanyi':lilunquanyi1,'realquanyi':realquanyi1}
	rbdata.append(tempdict)
	rbdata1.append(tempdict1)
	#计算KPI
	realtongji=kpi_tongji(lilunquanyi)
	realtongji['Net_Profit']=round(realtongji['Net_Profit']/10000,3)
	realtongji['Max_Drawdown']=round(realtongji['Max_Drawdown']/10000,3)
	realtongji['Daily_Std']=round(realtongji['Daily_Std']/10000,3)
	realtongji['Max_Day_Profit']=round(realtongji['Max_Day_Profit']/10000,3)
	realtongji['Max_Day_Loss']=round(realtongji['Max_Day_Loss']/10000,3)


	#查看账户理论权益
	ishowconfig=1
	account=userid
	ICdata=[]
	totalquanyiresult=order_get_dailyquanyi_forLilun(account,150521)
	# print "totalquanyiresult['result']",totalquanyiresult['result'][0:10]
	#计算相应的股指映射权益 [[date,value],[]]
	stock_yingshe_quanyi=order_get_stock_yingshe_quanyi(account,150521)
	if totalquanyiresult['ispass']==0:
		result=totalquanyiresult['result']
		return render_to_response('futureaccountone.html',{
			'data':data,
			'userid':userid,
			'rbdata':rbdata,
			'rbdata1':rbdata1,
			'ICdata':[],
			'username':username,
			'mybegintime':mybegintime,
			'myendtime':myendtime,
			'firsttime':firsttime,
			'lasttime':lasttime,
			'realtongji':realtongji,
			'liluntongji':{},
			'ispass':0,
			'result':result,


		})
	else:
		ispass=1
		result=totalquanyiresult['result']
		#加入股指的权益
		result=[[item[1],item[0]] for item in result]
		result=add_time_series(result,stock_yingshe_quanyi)
		result=sorted(result,key=lambda a :a[0])
		result=[[item[1],item[0]] for item in result]
		#####

		selectequates=[item for item in result if int(item[1])>=(int(mybegintime)-20000000)]
		selectequates=[item for item in selectequates if int(item[1])<=(int(myendtime)-20000000)]
		fisrtvalue=selectequates[0][0]
		selectequates=[[round(item[0]-fisrtvalue,2),item[1]] for item in selectequates]
		result=selectequates

		configinfo=totalquanyiresult['configinfo']
		# print "1######################################################"
		(tempday,lilunquanyi,realquanyi)=range_series(result,[])
		# print "2######################################################"
		tempdict={'acname':account,'symbol':"",'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		ICdata.append(tempdict)
		liluntongji=kpi_tongji(lilunquanyi)
		liluntongji['Net_Profit']=round(liluntongji['Net_Profit']/10000,3)
		liluntongji['Max_Drawdown']=round(liluntongji['Max_Drawdown']/10000,3)
		liluntongji['Daily_Std']=round(liluntongji['Daily_Std']/10000,3)
		liluntongji['Max_Day_Profit']=round(liluntongji['Max_Day_Profit']/10000,3)
		liluntongji['Max_Day_Loss']=round(liluntongji['Max_Day_Loss']/10000,3)

	return render_to_response('futureaccountone.html',{
		'data':data,
		'userid':userid,
		'rbdata':rbdata,
		'rbdata1':rbdata1,
		'ICdata':ICdata,
		'username':username,
		'mybegintime':mybegintime,
		'myendtime':myendtime,
		'firsttime':firsttime,
		'lasttime':lasttime,
		'realtongji':realtongji,
		'liluntongji':liluntongji,
		'ispass':1,


	})



def futureaccounttotal(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==3:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response

	#更新下hongsong合并信息
	general_HongsongAll()

	sql="SELECT[primarymoney],[future_company],userid,[beizhu] FROM [LogRecord].[dbo].[Future_AccountsBalance]  order by [ordernum]"
	res=ms.dict_sql(sql)
	returnlist=[]
	for item in res:
		userid=item['userid']
		#获取现在的月份
		#month=int(datetime.datetime.now().strftime('%Y%m'))*100
		sql="SELECT MAX(date) as date  FROM [LogRecord].[dbo].[AccountsBalance] where userid='%s' " % (userid)
		month=ms.dict_sql(sql)[0]['date']
		month=int(month)
		month=int(month/100.0)*100
		#month=20160900
		#print 'month',month
		#计算月初权益
		sql="SELECT top 1 [date] ,[userid],[CloseBalance],Withdraw FROM [LogRecord].[dbo].[AccountsBalance] where userid='%s'  and date< '%s' order by date desc" % (userid,month)
		temp1res=ms.dict_sql(sql)
		if temp1res:
			equity_on_month_begin=round(float(temp1res[0]['CloseBalance']+temp1res[0]['Withdraw']),1)
			Withdraw_on_month_begin=round(float(temp1res[0]['Withdraw']),1)
		else:
			equity_on_month_begin=0.1
			Withdraw_on_month_begin=0
		tempbegin=equity_on_month_begin
		if item['primarymoney']>10 and equity_on_month_begin<10:
			equity_on_month_begin=item['primarymoney']
		real_equity_on_month_begin=equity_on_month_begin-Withdraw_on_month_begin

		#获得当天权益，如果有出金，则标记出来
		sql="SELECT top 2 [date] ,[userid] ,[prebalance] ,[deposit] ,[Withdraw] ,[CloseProfit]  ,[PositionProfit]  ,[Commission]  ,[CloseBalance]  FROM [LogRecord].[dbo].[AccountsBalance] where userid='%s'  and date>='%s' order by date desc" % (userid,month)
		res=ms.dict_sql(sql)
		if len(res)>=1:
			todays_equity=round((res[0]['CloseBalance']+res[0]['Withdraw']),2)
			todays1_withdraw=res[0]['Withdraw']
		else:
			todays_equity=0
			todays1_withdraw=0
		if len(res)==2:
			yesterdays_equity=round((res[1]['CloseBalance']+res[1]['Withdraw']),2)
		else:
			yesterdays_equity=equity_on_month_begin


		#计算每月收益
		sql="select sum(Withdraw-deposit) as deltawithdeposit from  [LogRecord].[dbo].[AccountsBalance] where userid='%s'  and date>='%s'" % (userid,month)
		temp1res=ms.dict_sql(sql)
		if temp1res[0]['deltawithdeposit'] is not None:
			deltawithdeposit=temp1res[0]['deltawithdeposit']
		else:
			deltawithdeposit=0
		# print  "################"
		# print (todays_equity-todays1_withdraw)
		# print (equity_on_month_begin-Withdraw_on_month_begin)
		# print deltawithdeposit
		real_equity_on_month_begin=real_equity_on_month_begin-deltawithdeposit+todays1_withdraw
		monthly_equity=(todays_equity-todays1_withdraw)-(tempbegin-Withdraw_on_month_begin)+deltawithdeposit
		monthly_rate=round(monthly_equity/(real_equity_on_month_begin+0.00002)*100,2)

		#lastmonth
		sql="SELECT distinct floor([date]/100)*100 as date FROM [LogRecord].[dbo].[AccountsBalance] order by  floor([date]/100)*100 desc "
		tmep11res=ms.dict_sql(sql)
		lastmonth=tmep11res[-2]['date']
		sql="SELECT [date] ,[userid] ,[prebalance] ,[deposit] ,[Withdraw] ,[CloseProfit]  ,[PositionProfit]  ,[Commission]  ,[CloseBalance]  FROM [LogRecord].[dbo].[AccountsBalance] where userid='%s'  and date>='%s' order by date" % (userid,lastmonth)
		tempres=ms.dict_sql(sql)
		equity=0
		monthly_commitssion=0
		daily_profit=0
		daily_rate=0
		commission=0
		if tempres:
			#计算当月手续费		
			for item1 in tempres:
				monthly_commitssion=monthly_commitssion+item1['Commission']
			#计算当日盈利率：
			if len(tempres)>=2:			
				yesterdays_equity=tempres[-2]['CloseBalance']+tempres[-2]['Withdraw']
				yesterdays_withdraw=tempres[-2]['Withdraw']
			else:
				yesterdays_equity=0
				yesterdays_withdraw=0
			if len(tempres)>=1:
				equity=tempres[-1]['CloseBalance']+tempres[-1]['Withdraw']
				todays_withdraw=tempres[-1]['Withdraw']
				todays_deposit=tempres[-1]['deposit']
			else:
				equity=0
				todays_withdraw=0
				todays_deposit=0		
			commission=tempres[-1]['Commission']
			daily_profit=round(equity-todays_deposit-yesterdays_equity+yesterdays_withdraw,2)
			daily_rate=round(daily_profit/(yesterdays_equity+0.00002)*100,2)
			templist=[tempres[-1]['date'],int(item['primarymoney']),item['future_company'],item['userid'],round(equity_on_month_begin,1),round(monthly_equity,1),str(monthly_rate)+"%",round(equity,1),round(commission,1),round(daily_profit,1),str(daily_rate)+"%",item['beizhu'],todays_withdraw]
		else:
			todays_withdraw=0
			templist=[19900101,int(item['primarymoney']),item['future_company'],item['userid'],round(equity_on_month_begin,1),round(monthly_equity,1),str(monthly_rate)+"%",round(equity,1),round(commission,1),round(daily_profit,1),str(daily_rate)+"%",item['beizhu'],todays_withdraw]		
		returnlist.append(templist)
	return render_to_response('futureaccounttotal.html',{
		'data':returnlist,
		'username':username,
	})



def fixdatacrtab(request):
	if request.POST:
		ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
		D=request.POST.get('D','')
		print "##################",D
		newD=D.replace('/','')
		print newD
		#查找是否已经存在
		sql="SELECT top 1 result  FROM [LogRecord].[dbo].[get_quotes_date] where Date='%s' order by ID desc" % (newD)
		result1=ms.dict_sql(sql)
		if result1:
			msg="该天数据曾经补全过，如果发现仍有缺失请联系仇蓓蕾手工补全"
		else:
			cmd='python /home/yuyang/myfile/evolutionwork/pythonfile/get_quotes_from_ftp_daily.py %s' % (newD)
			sql="select * from [LogRecord].[dbo].[task_todo] where type='datafix' and cmd='%s' and status=0" % (cmd)
			res=ms.dict_sql(sql)
			if res:
				msg="已经插入过该补全数据任务，该任务将在16:00执行"
			else:
				sql="insert into [LogRecord].[dbo].[task_todo](type,cmd,todotime,status) values('datafix','%s','1550',0)" % (cmd)
				ms.insert_sql(sql)
				msg="成功插入定时任务，任务将在16:00执行"
	result=msg
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')




def fixdata(request):
	data=""
	whichtype=0
	res1=""
	res2=""
	res11=""
	res21=""
	symbol=""
	symbollist=""
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="select distinct symbol from Future.dbo.TSymbol order by symbol"
	symbollist=ms.dict_sql(sql)
	if request.POST:
		print "request.POST",request.POST
		sttype=request.POST.get("sttype","")
		print sttype
		if sttype=="night":
			symbol=request.POST.get("period","")
			sql="select '%s' as symbol,SUM(1) as sum,D from Future.dbo.TSymbol where symbol='%s' group by D order by sum(1),D " % (symbol,symbol)
			res2=ms.dict_sql(sql)
			whichtype=2
	return render_to_response('fixdata.html',{
		'data':data,
		'whichtype':whichtype,
		'res1':res1,
		'res2':res2,
		'res11':res11,
		'res21':res21,
		'symbollist':symbollist,
		'symbol':symbol
	})	



def acname_p_basic(request):
	data=""
	whichtype=0
	res1=""
	res2=""
	accountlist=""
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.GET:
		acname=request.GET.get("acname","")
		sql="select p.AC,p.ST,t.TradName,isnull(ss.Symbol,p.stock) as stock , ISNULL(convert(nvarchar,t.tradetime,120),'0未产生信号') as tradetime,ISNULL(convert(nvarchar,kk.stockdate,120),'无心跳') as heart from P_BASIC p left join Trading_logSymbol t on p.ST=t.ST left join Symbol_ID ss on p.STOCK=ss.S_ID left join LogRecord.dbo.ST_heart kk on p.ST=kk.st where p.ac='%s' order by tradetime" % (acname)
		res=ms.dict_sql(sql)
		sql="select distinct ac from p_follow where F_ac='%s' order by ac" % (acname)
		tempres=ms.dict_sql(sql)
		for item in tempres:
			temp="【"+item['ac']+"】 "
			accountlist=accountlist+temp
	if accountlist=="":
		accountlist="【未查到-请手工确认，如果仍然需要查看权益，请修复】"


	return render_to_response('acname_p_basic.html',{
		'data':data,
		'whichtype':whichtype,
		'res':res,
		'accountlist':accountlist,
	})	



def remove_whitelist(request):
	if request.POST:
		acname=request.POST.get('acname','')
		type=request.POST.get('type','')
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		sql="update [LogRecord].[dbo].[white_list] set isactive=0 where itemname='%s' and type='%s'" % (acname,type)
		print sql 
		ms.insert_sql(sql)
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')


def add_whitelist(request):
	if request.POST:
		acname=request.POST.get('acname','')
		type=request.POST.get('type','')
		ms= MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
		import socket
		outIP = socket.gethostbyname(socket.gethostname())#这个得到本地ip
		ipList = socket.gethostbyname_ex(socket.gethostname())
		computername=ipList[0]
		iplist=ipList[2]
		localIP=""
		for item in iplist:
			if item !=outIP:
				localIP=item
		if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
		    localIP =  request.META['HTTP_X_FORWARDED_FOR']  
		else:  
		    localIP = request.META['REMOTE_ADDR']
		sql="select 1 from [LogRecord].[dbo].[white_list] where itemname='%s' and type='%s'" % (acname,type)
		res1=ms.dict_sql(sql)
		if res1:
			sql="update [LogRecord].[dbo].[white_list] set isactive=1,ope_person='%s',ope_localIP='%s',ope_outIP='%s' where itemname='%s' and type='%s'" % (computername,localIP,outIP,acname,type)
			ms.insert_sql(sql)
		else:
			sql="insert into [LogRecord].[dbo].[white_list]([type],[itemname],[ope_person],[ope_localIP],[ope_outIP]) values('%s','%s','%s','%s','%s')" % (type,acname,computername,localIP,outIP)
			ms.insert_sql(sql)
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')



def lasttime_p_basic(request):
	data=""
	whichtype=0
	res1=""
	res2=""
	res3=""
	res11=""
	res21=""
	res31=""
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.POST:
		print "request.POST",request.POST
		sttype=request.POST.get("sttype","")
		print sttype
		if sttype=="day":
			#策略上线未产生信号
			sql="select distinct ac from (select p.AC,p.ST,p.STOCK from P_BASIC p left join Trading_logSymbol t on p.ST=t.ST where t.id is null and p.P_size<>0) a where ac not in (select itemname from [LogRecord].[dbo].[white_list] where isactive=1 and TYPE='nosignal') order by ac"
			res1=ms.dict_sql(sql)
			whichtype=1
		if sttype=="night":
			period=request.POST.get("period","")
			sql="select distinct ac from (select p.AC,p.P_size,p.ST,p.STOCK,t.tradetime,t.TradName from P_BASIC p left join Trading_logSymbol t on p.ST=t.ST where p.P_size<>0 and DATEDIFF(day,t.tradetime,GETDATE())>%s) a  where ac not in (select itemname from [LogRecord].[dbo].[white_list] where isactive=1 and TYPE='longtimenosignal')order by ac" % (period)
			res2=ms.dict_sql(sql)
			whichtype=2
		if sttype=="day_white":
			#策略上线未产生信号_白名单
			sql="SELECT itemname as ac FROM [LogRecord].[dbo].[white_list] where TYPE='nosignal' and isactive=1 order by itemname"
			res11=ms.dict_sql(sql)
			whichtype=11
		if sttype=="night_white":
			#策略上线未产生信号_白名单
			sql="SELECT itemname as ac FROM [LogRecord].[dbo].[white_list] where TYPE='longtimenosignal' and isactive=1 order by itemname"
			res21=ms.dict_sql(sql)
			whichtype=21
		if sttype=="type3":
			#存在没有心跳策略的虚拟组
			sql="select distinct ac from (select distinct a.AC from P_BASIC a left join LogRecord.dbo.ST_heart b on a.ST=b.st  where b.st is null and a.P_size <>0 ) a where ac not in (select itemname from [LogRecord].[dbo].[white_list] where isactive=1 and TYPE='noheart')  order by ac"
			res3=ms.dict_sql(sql)
			whichtype=3
		if sttype=="type3_white":
			#策略上线未产生信号_白名单
			sql="SELECT itemname as ac FROM [LogRecord].[dbo].[white_list] where TYPE='noheart' and isactive=1 order by itemname"
			res31=ms.dict_sql(sql)
			whichtype=31
	return render_to_response('lasttime_p_basic.html',{
		'data':data,
		'whichtype':whichtype,
		'res1':res1,
		'res2':res2,
		'res11':res11,
		'res21':res21,
		'res3':res3,
		'res31':res31
	})	




def st_heart(request):
	data=""
	isres=0
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	if request.POST:
		sttype=request.POST.get("sttype","")
		print sttype
		if sttype=='day':
			sql="SELECT top 400 a.st,a.TradName,b.address,b.stockdate  FROM [Future].[dbo].[Trading_logSymbol] a  inner join(  SELECT [st],address,stockdate   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3 and type in (1,12)  ) b on a.ST=b.st"
		else:
			sql="SELECT top 400 a.st,a.TradName,b.address,b.stockdate  FROM [Future].[dbo].[Trading_logSymbol] a  inner join(  SELECT [st],address,stockdate   FROM [LogRecord].[dbo].[ST_heart]   where DATEDIFF(MINUTE, [stockdate], getdate())>=3 and type in (2,12)  ) b on a.ST=b.st"
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
		data=request.POST.get("data","")
		data=data.strip('#')
		data=data.split('#')
		isdel=0
		sql="select distinct acname as ac from [LogRecord].[dbo].[quanyicaculatelist] union all select distinct ac from [LogRecord].[dbo].order_p_follow order by ac"
		order_p_follow_res=ms.find_sql(sql)
		order_p_follow_res=[str(a[0]) for a in order_p_follow_res]
		for item in data:
			item=item.strip(';')
			item=item.split(';')
			if len(item)==4:
				if isdel==0:
					sql="delete from [LogRecord].[dbo].[order_p_follow] where ac='%s'" % (item[0])
					ms.insert_sql(sql)
					isdel=1
				#将一行中的多个“ss,ff,f”拆分
				F_aclist=item[1].split(',')
				for temitem in F_aclist:
					#symbol的确认
					print 'temitem',temitem
					if item[2]=='default':
						sql="select  quanyisymbol from LogRecord.dbo.quanyicaculatelist  where acname='%s'" % (temitem)
						tempres1=ms.dict_sql(sql)
						if tempres1:
							realsymbol=tempres1[0]['quanyisymbol']
						else:
							realsymbol=item[2]
					else:
						realsymbol=item[2]
					print 'realsymbol',realsymbol

					#检查temitem是否是 order_p_follow 中的项目，如果是则继续，如果不是，则检查是否是p_follow中的ac
					if temitem in order_p_follow_res:
						sql="insert into [LogRecord].[dbo].[order_p_follow](ac,F_ac,ratio,Pratio,stock) values('%s','%s',%s,%s,'%s')" % (item[0],temitem,item[3],item[3],realsymbol)
						ms.insert_sql(sql)
						# print sql 
					else:
						#temitem 在p_follow中，需要执行copy
						sql="insert into [LogRecord].[dbo].[order_p_follow](ac,F_ac,ratio,Pratio,stock)   select '%s',F_ac,sum(ratio)*(%s),100,s.symbol from [Future].[dbo].[p_follow] p   left join  (select * from [Future].[dbo].[Symbol_ID] where id in (SELECT min(id)  FROM [Future].[dbo].[Symbol_ID] where (Symbol not like '%%night%%'  and (Symbol not like '%%N' ) and Symbol not like '%%ZL') OR  Symbol='ZN' or Symbol='RMZL'group by s_id)) s on   p.stock=s.S_ID    where ac='%s'    group by p.F_ac,s.Symbol" % (item[0],float(item[3])/100.0,temitem)
						#sql="insert into [LogRecord].[dbo].[order_p_follow](ac,F_ac,ratio,Pratio,stock) select '%s',F_ac,sum(ratio)*(%s),100,'default' from [Future].[dbo].[p_follow]  where ac='%s' group by F_ac" % (item[0],float(item[3])/100.0,temitem)
						ms.insert_sql(sql)
						# print sql 

	else:
		print "not post"
	result=1
	result=simplejson.dumps(result,ensure_ascii = False)
	return HttpResponse(result,mimetype='application/json')




def order_account_equity(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response

	sql="SELECT distinct ac from [LogRecord].[dbo].[order_p_follow] order by ac"
	aclist=ms.dict_sql(sql)
	ICdata=[]
	ispass=0
	ishowconfig=0
	tongji={}
	account=""
	res=""
	F_aclist=""
	configinfo=0
	#开始查询
	if request.POST:
		print request.POST
		whichform=request.POST.get('query','')
		if whichform=='query':
			account=request.POST.get('searchaccount','')
			sql="select ID as myid,row_number()OVER(ORDER BY [AC] DESC) as id,ac,F_ac,ratio,stock from [LogRecord].[dbo].[order_p_follow] where ac='%s' order by F_ac" % (account)
			res=ms.dict_sql(sql)
			sql="select distinct quanyisymbol from LogRecord.dbo.quanyicaculatelist order by quanyisymbol"
			quanyisymbollist=ms.dict_sql(sql)
			#监测account名字是否与p_basic或者p_foloow一致 
			sql="select 1 from [Future].[dbo].[P_BASIC] where ac='%s' union all select 2 from [Future].[dbo].[P_follow] where ac='%s'" % (account,account)
			testres=ms.dict_sql(sql)
			if testres:
				account="Test_"+account
			#sql="select distinct acname as ac from [LogRecord].[dbo].[quanyicaculatelist] order by acname"
			sql="select distinct acname as ac,'虚拟组' as type from [LogRecord].[dbo].[quanyicaculatelist] union all select distinct ac,'测试账户' as type from [LogRecord].[dbo].order_p_follow   union all  select distinct ac,'真实账户' as type from [Future].[dbo].[p_follow] order by type,ac"
			F_aclist=ms.dict_sql(sql)
			# amount_list

			aclistresult=order_get_ac_ratio_two(account)
			resultlist={}
			# if aclistresult:
			# 	newaclistresult={}
			# 	for key in aclistresult:
			# 		newaclistresult[key.lower()]=aclistresult[key]
			# 	aclistresult=newaclistresult
			# 	keylist=""
			# 	for key in aclistresult:
			# 		keylist=keylist+",'"+key+"'"
			# 	keylist=keylist.strip(",")

			if aclistresult:
				newaclistresult={}
				testnewaclistresult={}
				for key in aclistresult:
					newaclistresult[key.lower().split('__')[0]]=aclistresult[key]
				for key in aclistresult:
					testnewaclistresult[key.lower()]=aclistresult[key]
				aclistresult=testnewaclistresult
				keylist=""
				for key in newaclistresult:
					keylist=keylist+",'"+key+"'"
				keylist=keylist.strip(",")

				sql="select kk.acname+'__'+cast(sss.s_id as nvarchar) as acname,quanyisymbol,case when issumps=0 then pp.position when issumps=1 then 10 end as position from LogRecord.dbo.quanyicaculatelist kk inner join (select round(SUM(p.P_size*a.ratio/100.0),0) as position,p.ac,p.STOCK from p_basic p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.AC in (%s) where p.ac in (%s) group by p.ac,p.STOCK) pp on kk.acname=pp.AC inner join Symbol_ID sss on kk.quanyisymbol=sss.Symbol" % (keylist,keylist)		
				#sql="select kk.acname,quanyisymbol,case when issumps=0 then pp.position when issumps=1 then 10 end as position from LogRecord.dbo.quanyicaculatelist kk inner join (select round(SUM(p.P_size*a.ratio/100.0),0) as position,p.ac,p.STOCK from p_basic p inner join AC_RATIO a on p.AC=a.AC and p.STOCK=a.Stock and p.AC in (%s) where p.ac in (%s) group by p.ac,p.STOCK) pp on kk.acname=pp.AC" % (keylist,keylist)
				tmpres11=ms.dict_sql(sql)
				resultlist={}
				for item in tmpres11:
					resultlist[item['quanyisymbol']]=0
				for item in tmpres11:
					if aclistresult.has_key(item['acname'].lower()):
						resultlist[item['quanyisymbol']]=resultlist[item['quanyisymbol']]+item['position']*aclistresult[item['acname'].lower()]/100.0
						del aclistresult[item['acname'].lower()]
				for key in aclistresult:
					resultlist[key]="此虚拟组没有找到对应手数"
				resultlist=[(key,resultlist[key]) for key in resultlist]
				resultlist.sort(key=lambda x:x[0])
			else:
				resultlist=[('没有配置虚拟组','或虚拟组配置手数为0')]


			return render_to_response('order_account_equity.html',{
				'account':account,
				'res':res,
				'F_aclist':F_aclist,
				'aclist':aclist,
				'ishowconfig':ishowconfig,
				'resultlist':resultlist,
				'quanyisymbollist':quanyisymbollist,
			})
		if whichform=='equity':
			ishowconfig=1
			account=request.POST.get('account','')
			totalquanyiresult=order_get_dailyquanyi(account,150521)
			if totalquanyiresult['ispass']==0:
				result=totalquanyiresult['result']
				configinfo=totalquanyiresult['configinfo']
				return render_to_response('order_account_equity.html',{
					'aclist':aclist,
					'ispass':ispass,
					'result':result,
					'configinfo':configinfo,
					'ishowconfig':ishowconfig
				})
			else:
				ispass=1
				result=totalquanyiresult['result']
				configinfo=totalquanyiresult['configinfo']
				print "1######################################################"
				print result[0:10]
				(tempday,lilunquanyi,realquanyi)=range_series(result,[])
				print "2######################################################"
				tempdict={'acname':account,'symbol':"",'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
				ICdata.append(tempdict)
				print 3,lilunquanyi
				tongji=kpi_tongji(lilunquanyi)
		isadd_new_line=request.POST.get('add_new_line','')
		if isadd_new_line=='query':
			account=request.POST.get('account','')
			sql="insert into [LogRecord].[dbo].[order_p_follow](ac,F_ac,ratio,Pratio,stock) values('%s','请选择',100,100,'default')" % (account)
			ms.insert_sql(sql)
			sql="select ID as myid,row_number()OVER(ORDER BY [AC] DESC) as id,ac,F_ac,ratio,stock from [LogRecord].[dbo].[order_p_follow] where ac='%s' order by F_ac" % (account)
			res=ms.dict_sql(sql)
			sql="select distinct quanyisymbol from LogRecord.dbo.quanyicaculatelist order by quanyisymbol"
			quanyisymbollist=ms.dict_sql(sql)
			#监测account名字是否与p_basic或者p_foloow一致 
			sql="select 1 from [Future].[dbo].[P_BASIC] where ac='%s' union all select 2 from [Future].[dbo].[P_follow] where ac='%s'" % (account,account)
			testres=ms.dict_sql(sql)
			if testres:
				account="Test_"+account
			#sql="select distinct acname as ac from [LogRecord].[dbo].[quanyicaculatelist] order by acname"
			sql="select distinct acname as ac,'虚拟组' as type from [LogRecord].[dbo].[quanyicaculatelist] union all select distinct ac,'测试账户' as type from [LogRecord].[dbo].order_p_follow   union all  select distinct ac,'真实账户' as type from [Future].[dbo].[p_follow] order by type,ac"
			F_aclist=ms.dict_sql(sql)
			return render_to_response('order_account_equity.html',{
				'account':account,
				'res':res,
				'F_aclist':F_aclist,
				'aclist':aclist,
				'ishowconfig':ishowconfig,
				'quanyisymbollist':quanyisymbollist,
			})



	return render_to_response('order_account_equity.html',{
		'ispass':ispass,
		'aclist':aclist,
		'ICdata':ICdata,
		'tongji':tongji,
		'account':account,
		'res':res,
		'F_aclist':F_aclist,
		'configinfo':configinfo,
		'ishowconfig':ishowconfig,
		'username':username,
	})	








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
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponseRedirect('/index/login')
		return response
	#验证登录用户
	# ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	# sql="select username from [LogRecord].[dbo].[account_user]  where userid='%s' and isactive=1"
	# res=ms.dict_sql(sql)
	# if res:
	# 	username = res[0]['username']
	# else:
	# 	username='匿名用户'

	now = datetime.datetime.now()
	t = get_template('myindex.html')
	html = t.render(Context({
		'current_date':now,
		'username':username,

		}))
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
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


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
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response

	if request.POST:
		id=request.POST.get('id','')

	if request.GET:
		starttime=request.GET.get("starttime","")
	else:
		starttime=151001

	newD=160621
	startdate=starttime
	IFdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('IF') and iscaculate in (1,2)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum" 
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (tempquanyi,acname,symbol,startdate)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		if tempday:
			tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}

		else:
			tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':0}
		IFdata.append(tempdict)


	ICdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('IC') and iscaculate in (1,2)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum" 
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (tempquanyi,acname,symbol,startdate)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		if tempday:
			tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}

		else:
			tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':0}
		ICdata.append(tempdict)





	# IFdata=[]
	# sql="select distinct ac,symbol from dailyquanyi where symbol='IF' and D>151020  order by ac"
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
	# 	IFdata.append(tempdict)

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

	return render_to_response('acwantedequlitystock.html',{
		'ICdata':ICdata,
		'IFdata':IFdata,
		'username':username,
	})	



def acwantedequlity(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


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


def acwantedequlityhistory(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


	if request.POST:
		id=request.POST.get('id','')
	newD=160621
	RBlist=[]


	rbdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RB','RBnight') and iscaculate in (1,2)  and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		rbdata.append(tempdict)

	AGdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('AG') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}

		AGdata.append(tempdict)

	CUdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('CU') and iscaculate in (1,2) and [isstatistic] =1  and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		CUdata.append(tempdict)

	RUdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RU') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		RUdata.append(tempdict)

	TAdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('TA') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		TAdata.append(tempdict)

	JDdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('JD') and iscaculate in (1,2) and [isstatistic] =1  and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		JDdata.append(tempdict)

	BUdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('BU') and iscaculate in (1,2) and [isstatistic] =1  and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		BUdata.append(tempdict)

	CSdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('CS') and iscaculate in (1,2) and [isstatistic] =1  and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		CSdata.append(tempdict)

	HCdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('HC') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1  order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		HCdata.append(tempdict)

	Pdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('P') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		Pdata.append(tempdict)

	PPdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('PP') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		PPdata.append(tempdict)

	NIdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('NI') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		NIdata.append(tempdict)
	
	Idata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('I') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		Idata.append(tempdict)

	Mdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('M') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=1 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
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
		'username':username,
	})	


def map_acname_position(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	ms105 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


	if request.POST:
		id=request.POST.get('id','')
	newD=160621
	RBlist=[]
	timeArray = time.strptime('2016-11-03 14:19:00', "%Y-%m-%d %H:%M:%S")
	timeStamp = int(time.mktime(timeArray))
	print 'timeStamp',timeStamp



	IFdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where [quanyisymbol] in ('IF') and  iscaculate in (3)  and [isstatistic] =1  and [isforhistory]=0 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']

		#acname='9KDHPM'
		##获取5日前日期
		nowtime=(datetime.datetime.now()-datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
		sql="SELECT top 2000 datetime as stockdate,vp as totalposition from [future].[dbo].[real_map_backup] where name='%s'  and datetime>='%s' order by datetime" % (acname,nowtime)
		res1=ms105.dict_sql(sql)
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
		sql="SELECT top 2000 datetime as stockdate,rp as totalposition from [future].[dbo].[real_map_backup] where name='%s'  and datetime>='%s' order by datetime" % (acname,nowtime)
		res2=ms105.dict_sql(sql)
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

		tempdict={'acname':acname,'symbol':symbol,'data1':newdata1,'data2':newdata2}
		IFdata.append(tempdict)

		nowtime=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
		sql="SELECT top 2000 datetime as stockdate,vp as totalposition from [future].[dbo].[real_map_backup] where name='%s'  and datetime>='%s' order by datetime" % (acname,nowtime)
		res1=ms105.dict_sql(sql)
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
		sql="SELECT top 2000 datetime as stockdate,rp as totalposition from [future].[dbo].[real_map_backup] where name='%s'  and datetime>='%s' order by datetime" % (acname,nowtime)
		res2=ms105.dict_sql(sql)
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

		tempdict={'acname':acname+'_today','symbol':symbol,'data1':newdata1,'data2':newdata2}
		IFdata.append(tempdict)





	return render_to_response('map_acname_position.html',{
		'IFdata':IFdata,
		'username':username,
	})	




def stockmapequty(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


	if request.POST:
		id=request.POST.get('id','')


	if request.GET:
		starttime=request.GET.get("starttime","")
	else:
		starttime=151001

	newD=160621
	startdate=starttime
	RBlist=[]


	IFdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where [quanyisymbol] in ('IF') and  iscaculate in (3)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (tempquanyi,acname,symbol,startdate)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		res2=ms.find_sql(sql)
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		IFdata.append(tempdict)

	ICdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where [quanyisymbol] in ('IC') and  iscaculate in (3)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (tempquanyi,acname,symbol,startdate)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		ICdata.append(tempdict)

	IHdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where [quanyisymbol] in ('IH') and  iscaculate in (3)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (tempquanyi,acname,symbol,startdate)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		IHdata.append(tempdict)


	TFdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where [quanyisymbol] in ('TF') and  iscaculate in (3)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (tempquanyi,acname,symbol,startdate)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		TFdata.append(tempdict)

	Tdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where [quanyisymbol] in ('T') and  iscaculate in (3)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (tempquanyi,acname,symbol,startdate)
		res1=ms.find_sql(sql)
		sql="select quanyi as  quanyia,D from real_dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,startdate)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		Tdata.append(tempdict)


	return render_to_response('stockmapequity.html',{
		'IFdata':IFdata,
		'ICdata':ICdata,
		'IHdata':IHdata,
		'TFdata':TFdata,
		'Tdata':Tdata,
		'username':username,
	})	



def acwantedequlitynew_jieti(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


	if request.GET:
		ac=request.GET.get("ac","")

	rbdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist]  where  acname in ( select f_ac from p_follow where ac='%s' ) order by symbol" % (ac)
	print sql 
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		if tempday:
			tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}

		else:
			tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':0}
		rbdata.append(tempdict)



	#计算整个阶梯组权益
	ICdata={}
	totalquanyiresult=order_get_dailyquanyi_forLilun(ac,150521)
	if totalquanyiresult['ispass']==0:
		message="配置似乎不是很正确，请俞洋检查下配置"
	else:
		result=totalquanyiresult['result']
		selectequates=[item for item in result]
		fisrtvalue=selectequates[0][0]
		selectequates=[[round(item[0]-fisrtvalue,2),item[1]] for item in selectequates]
		result=selectequates
		(tempday,lilunquanyi,realquanyi)=range_series(result,[])
		# print "2######################################################"
		tempdict={'acname':ac,'symbol':"",'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi}
		# ### write to _csv
		# tmpdata=pd.DataFrame({'day':tempday,'lilunquanyi':lilunquanyi})
		# tmpdata.to_csv(r'D:\test'+"\\"+ac+".csv")
		ICdata=tempdict
		liluntongji=kpi_tongji(lilunquanyi)
		liluntongji['Net_Profit']=round(liluntongji['Net_Profit']/10000,3)
		liluntongji['Max_Drawdown']=round(liluntongji['Max_Drawdown']/10000,3)
		liluntongji['Daily_Std']=round(liluntongji['Daily_Std']/10000,3)
		liluntongji['Max_Day_Profit']=round(liluntongji['Max_Day_Profit']/10000,3)
		liluntongji['Max_Day_Loss']=round(liluntongji['Max_Day_Loss']/10000,3)







	return render_to_response('acwantedequlitynew_jieti.html',{
		'AGdata':rbdata,
		'ICdata':ICdata,
		'username':username,
		'realtongji':liluntongji,
		'ac':ac,
	})	





def acwantedequlitynew_oneacname(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


	if request.GET:
		symbol=request.GET.get("symbol","")
		begintime=request.GET.get("begintime","")
	quanyisymbol=symbol
	# begintime=161020
	if begintime=='onemonth':
		mydate=datetime.datetime.now()-datetime.timedelta(days=60)
		mydate=mydate.strftime('%y%m%d')
		begintime=int(mydate)



	rbdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('%s') and iscaculate in (1,2,8,9)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum" % (symbol)
	res=ms.dict_sql(sql)
	for item in res:
		acname=item['ac']
		symbol=item['symbol']
		#第一个价格
		sql="select top 1 quanyi as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,begintime)
		tempquanyi=ms.find_sql(sql)
		if tempquanyi==[]:
			tempquanyi=0
		else:
			tempquanyi=tempquanyi[0][0]
		sql="select quanyi-(%s) as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (tempquanyi,acname,symbol,begintime)
		res1=ms.find_sql(sql)
		sql="select position as  quanyia,D from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (acname,symbol,begintime)
		res2=ms.find_sql(sql)		
		(tempday,lilunquanyi,realquanyi)=range_series(res1,res2)
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		if tempday:
			tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}

		else:
			tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':0}
		rbdata.append(tempdict)









	return render_to_response('acwantedequlity_onesymbol.html',{
		'AGdata':rbdata,
		'username':username,
		'quanyisymbol':quanyisymbol,
	})	



def acwantedequlitynew(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


	sql="select distinct quanyisymbol from [LogRecord].[dbo].[quanyicaculatelist]  order by quanyisymbol"
	res=ms.dict_sql(sql)
	lenres=len(res)
	aa=int(lenres/2)
	print 'aa',aa
	res1=res[:aa]
	res2=res[aa:]

	#sql="select distinct ac from p_follow where ac like '%stepmulti%' and ac not in ('StepMultiI300w','StepMulti2') order by ac"
	sql="select bb.* from (select distinct ac from p_follow where ac like '%stepmulti%' )aa inner join (select a.ac,convert(nvarchar,MIN(inserttime),102) as starttime from [LogRecord].[dbo].[update_p_follow] a inner join (SELECT distinct ac  FROM [LogRecord].[dbo].[update_p_follow] where ac like '%Stepmulti%'  and ac not in ('StepMultiI300w','StepMulti2','StepMultigaosheng2')) b on a.AC=b.AC group by a.AC )bb on aa.AC=bb.AC order by bb.AC"
	res3=ms.dict_sql(sql)









	return render_to_response('acwantedequlityindex.html',{
		'res1':res1,
		'res2':res2,
		'res3':res3,
		'username':username,
	})	




def acwantedequlitynew1(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==2:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response


	if request.POST:
		id=request.POST.get('id','')
	newD=160621
	RBlist=[]


	rbdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RB','RBnight') and iscaculate in (1,2)  and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		rbdata.append(tempdict)

	AGdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('AG') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		AGdata.append(tempdict)

	CUdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('CU') and iscaculate in (1,2) and [isstatistic] =1  and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		CUdata.append(tempdict)

	RUdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RU') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		RUdata.append(tempdict)

	TAdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('TA') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		TAdata.append(tempdict)

	JDdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('JD') and iscaculate in (1,2) and [isstatistic] =1  and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		JDdata.append(tempdict)

	BUdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('BU') and iscaculate in (1,2) and [isstatistic] =1  and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		BUdata.append(tempdict)

	CSdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('CS') and iscaculate in (1,2) and [isstatistic] =1  and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		CSdata.append(tempdict)

	HCdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('HC') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0  order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		HCdata.append(tempdict)

	Pdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('P') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		Pdata.append(tempdict)

	PPdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('PP') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		PPdata.append(tempdict)

	NIdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('NI') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		NIdata.append(tempdict)
	
	Idata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('I') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
		Idata.append(tempdict)

	Mdata=[]
	sql="select acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('M') and iscaculate in (1,2) and [isstatistic] =1 and [isforhistory]=0 order by sortnum"
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
		#计算交易次数(200天平均)
		sql="select round(AVG(times)/10,2) as avg from (  select top 200 * from [Future].[dbo].[dailyquanyi_V2] where ac='%s' order by D desc) a where abs(position)+ABS(quanyi)+abs(times)<>0" % (acname)
		res1=ms.dict_sql(sql)
		avgtime=res1[0]['avg']
		tempdict={'acname':acname,'symbol':symbol,'xaxis':tempday,'lilunquanyi':lilunquanyi,'realquanyi':realquanyi,'avgtime':avgtime,'lastday':tempday[-1]}
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
		'username':username,
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
	ms105 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future") 
	if requst.GET:
		acname=requst.GET.get('acname','')
	else:
		acname='Rb_QGpLud'
	#acname='9KDHPM'
	##获取5日前日期
	p_followac='StepMultigaosheng1'
	realaccount='666061010'
	begintime='2017-01-01'
	endtime='2017-02-15 16:00:00'
	totaldata=[]
	sql=" select  f_ac from p_follow where ac='%s' order by f_ac" % (p_followac)
	totalres=ms.dict_sql(sql)
	for totalitem in totalres:
		acname=totalitem['f_ac']
		print acname
		nowtime=(datetime.datetime.now()-datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
		sql="select q.stockdate,round(q.totalposition*1,0) as totalposition ,q.symbol,sid.S_ID from p_follow p inner join quanyi_log_groupby_v2 q on p.F_ac=q.AC and p.AC='%s' inner join LogRecord.dbo.test_margin mr on q.symbol=mr.symbol inner join symbol_id sid on q.symbol=sid.Symbol where q.AC='%s' and stockdate>='%s' and stockdate<='%s' order by stockdate" % (p_followac,acname,begintime,endtime)
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
		realstokid=res1[0]['S_ID']
		#sql="SELECT [inserttime] as stockdate ,[longhave]-[shorthave] as totalposition FROM [LogRecord].[dbo].[account_position] where userid='%s'   and inserttime<='%s' and inserttime>='%s' and stockid=%s order by inserttime" % (realaccount,endtime,begintime,realstokid)
		sql="select q.stockdate,round(q.totalposition*1,0) as totalposition ,q.symbol,sid.S_ID from p_follow p inner join quanyi_log_groupby_v3 q on p.F_ac=q.AC and p.AC='%s' inner join LogRecord.dbo.test_margin mr on q.symbol=mr.symbol inner join symbol_id sid on q.symbol=sid.Symbol where q.AC='%s' and stockdate>='%s' and stockdate<='%s' order by stockdate" % (p_followac,acname,begintime,endtime)
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
		totaldata.append([acname,newdata1,newdata2])


	return render_to_response('showaccompare.html',{
		'data':acname,
		'data1':newdata1,
		'data2':newdata2,
		'totaldata':totaldata,
	})	


def configmonitorlist(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==4:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="SELECT [id],[type],[item],[ismonitor],[starttime],[endtime] FROM [LogRecord].[dbo].[monitorconfig]"
	res=ms.dict_sql(sql)
	data=res
	return render_to_response('configmonitorlist.html',{
		'data':data
	})	


def configmailtolist(request):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	userid = request.COOKIES.get('userid','')
	username = request.COOKIES.get('username','')
	#验证权限
	sql="SELECT a.username,b.function_id,b.function_content  FROM [LogRecord].[dbo].[account_user] a  inner join [LogRecord].[dbo].[account_group] b  on   a.groupname=b.groupname where a.userid='%s' " % (userid)
	res=ms.dict_sql(sql)
	isauthpass=0
	if res:
		for item in res:
			if int(item['function_id'])==4:
				isauthpass=1
	if isauthpass==0:
		response = HttpResponse("该功能正在完善，请返回 !! <a href='/index/'>返回</a>")
		return response

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
	lastdate=datalist[0][:]
	for item in datalist[1:]:
		while (item[0]-lastdate[0])>60:
			lastdate[0]=lastdate[0]+60
			newdatalist.append([lastdate[0],lastdate[1]])
		newdatalist.append(item)
		lastdate=item[:]
	#return newdatalist

	####### delete replecate record
	tempc=[]
	tempc.append(newdatalist[0])
	for i in range(1,len(newdatalist)-1):
		if newdatalist[i][1]==newdatalist[i-1][1] and newdatalist[i][1]==newdatalist[i+1][1]:
			pass
		else:
			tempc.append(newdatalist[i])
	tempc.append(newdatalist[-1])
	return tempc



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
			lilunquanyi[i]=round(totalvalue,2)
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
		lilunquanyi[i]=round(totalvalue,2)
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

#获得账号点菜系统虚拟组(第一版本)
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

#获得账号点菜系统虚拟组(第二版本)
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
	sql="WITH Emp AS ( SELECT ac,F_ac,ratio,stock FROM  [LogRecord].[dbo].[order_p_follow]  WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100,D.stock FROM   Emp          INNER JOIN [LogRecord].[dbo].[order_p_follow] d ON d.ac = Emp.F_ac)      select '%s' as AC,f_AC+'__'+CAST(ss.S_ID as nvarchar) as f_AC,SUM(ratio) as ratio from Emp   inner join  Symbol_ID ss on Emp.stock=ss.Symbol     where  Emp.f_ac not in (select ac from Emp)  and Emp.ratio<>0 group by Emp.F_ac,ss.S_ID order by Emp.F_ac" % (account,account)
	#sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  [LogRecord].[dbo].[order_p_follow] WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100 FROM   Emp         INNER JOIN [LogRecord].[dbo].[order_p_follow] d ON d.ac = Emp.F_ac)     select '%s' as AC,f_AC,SUM(ratio) as ratio from Emp where  f_ac not in (select ac from Emp)  and ratio<>0 group by F_ac" % (account,account)
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

#获得账号点菜系统虚拟组(第三版本-p_follow)
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


#计算总权益
def get_dailyquanyi(account,fromDdy):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	ac_ratio=get_ac_ratio(account)
	totalquanyi=[]
	for key in ac_ratio:
		ratio=ac_ratio[key]
		if ratio<>0:
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
	ac_ratio=order_get_ac_ratio_two(account)
	totalquanyi=[]
	#获取对齐时间
	Dlist=[]
	tempresult=""
	configinfo=[]
	Dlist.append(fromDdy)
	if ac_ratio==[]:
		return {"ispass":0,"result":"存在有自己跟随自己的配置，请修正"}
	for key in ac_ratio:
		realac=key.split("__")[0]
		quanyisymbols_id=key.split("__")[-1]
		sql="select top(1) [positionsymbol] from [LogRecord].[dbo].[quanyicaculatelist]  where acname='%s'" % (realac)
		positionsymbol=ms.dict_sql(sql)[0]['positionsymbol']
		sql="select  a.acname,s.S_ID,s.Symbol from LogRecord.dbo.quanyicaculatelist a left join Symbol_ID s on a.quanyisymbol=s.Symbol where a.acname='%s' and  s.S_ID='%s'" % (realac,quanyisymbols_id)
		tempres1=ms.dict_sql(sql)
		if tempres1:
			quanyisymbol=ms.dict_sql(sql)[0]['Symbol']
		else:
			return {"ispass":0,"result":"权益计算配置表未配置该选项 %s" % (key),"configinfo":[]}
		sql="SELECT top 1  (convert(int,replace(convert(varchar(10),DATEADD(day,1,stockdate),120),'-',''))-20000000) as D  FROM [Future].[dbo].[quanyi_log_groupby_v2] where ac='%s' and symbol='%s' order by stockdate" % (realac,positionsymbol)
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

def order_get_dailyquanyi_backup(account,fromDdy):
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	ac_ratio=order_get_ac_ratio_two(account)
	totalquanyi=[]
	#获取对齐时间
	Dlist=[]
	tempresult=""
	configinfo=[]
	Dlist.append(fromDdy)
	if ac_ratio==[]:
		return {"ispass":0,"result":"存在有自己跟随自己的配置，请修正"}
	for key in ac_ratio:
		sql="SELECT top 1  (convert(int,replace(convert(varchar(10),DATEADD(day,1,stockdate),120),'-',''))-20000000) as D  FROM [Future].[dbo].[quanyi_log_groupby_v2] where ac='%s' order by stockdate" % (key)
		tempD=ms.dict_sql(sql)
		if tempD:
			Dlist.append(tempD[0]['D'])
			configinfo.append([key,ac_ratio[key],tempD[0]['D']])
		else:
			Dlist.append(200000)
			sql="select ac from [LogRecord].[dbo].[order_p_follow]  where F_ac='%s'" % (key)
			tempres=ms.dict_sql(sql)
			tempresult=tempresult+" 基本账户 %s 中 %s 没有产生过信号,请补全近两年策略信号</br>" % (tempres[0]['ac'],key)
			configinfo.append([key,ac_ratio[key],200000])
	fromDdy=max(Dlist)
	if 200000 in Dlist:
		return {"ispass":0,"result":tempresult,"configinfo":configinfo}

		
	for key in ac_ratio:
		ratio=ac_ratio[key]
		if ratio<>0:
			sql="SELECT [quanyisymbol]  FROM [LogRecord].[dbo].[quanyicaculatelist] where acname='%s'" % (key)
			res=ms.dict_sql(sql)
			if not res:
				# print {"ispass":0,"result":"%s does not has equity" % (key)}
				return {"ispass":0,"result":"%s 不在配置表 quanyicaculatelist 中，请加上并获得历史信号" % (key),"configinfo":configinfo}
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





#计算账户股指映射的权益
def order_get_stock_yingshe_quanyi(account,fromDdy):
	ms105 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="future")
	ms05 = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	sql="SELECT account,REVERSE('0'+SUBSTRING(REVERSE([acanme]),2,100)) as acname,symbol,SUM(ratio) as ratio   FROM [future].[dbo].[account_position_stock_yingshe]   where account='%s'   group by account,REVERSE('0'+SUBSTRING(REVERSE([acanme]),2,100)),symbol" % (account)
	res=ms105.dict_sql(sql)
	totalquanyi=[]
	for item in res:
		sql="SELECT D  ,[quanyi] FROM [Future].[dbo].[dailyquanyi_V2] where ac='%s' and symbol='%s' and D>=%s" %(item['acname'],item['symbol'],fromDdy)
		re1=ms05.dict_sql(sql)
		tempquanyi=[[item1['D'],item1['quanyi']] for item1 in re1]
		totalquanyi=add_time_series(totalquanyi,tempquanyi)
	totalquanyi=sorted(totalquanyi,key=lambda a :a[0])
	return totalquanyi




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
	if lilunquanyi:
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
	return result


#红松普票账户和期货账户合并
def general_HongsongAll():
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
	sql="select max(date) as date from [LogRecord].[dbo].[AccountsBalance] where userid in ('HongsongStock','666061008') group by userid"
	res=ms.dict_sql(sql)
	sql="select max(date) as date from [LogRecord].[dbo].[AccountsBalance] where userid ='HongsongAll'"
	maxHongsongAll=ms.dict_sql(sql)[0]['date']
	nowtime=int(datetime.datetime.now().strftime("%H%M"))

	if res[0]['date']==res[1]['date'] and res[1]['date']>maxHongsongAll and nowtime>=1501:
		sql="insert into [LogRecord].[dbo].[AccountsBalance] select date,'HongsongAll' as userid, 0 as prebalance, SUM(deposit) as deposit,SUM(Withdraw)as Withdraw,0 as CloseProfit,0 as PositionProfit,SUM(Commission) as Commission,SUM(CloseBalance) as CloseBalance  from [LogRecord].[dbo].[AccountsBalance] where userid in ('HongsongStock','666061008') and date>%s group by date " % (maxHongsongAll)
		ms.insert_sql(sql)


#将账号仓位快照入库
def cal_distinct_position_lilun():
	#1 put lilun equity into account_position_lilun,添加不存在报警机制
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	sql="truncate table [LogRecord].[dbo].account_position_lilun"
	ms.insert_sql(sql)
	sql="select distinct userid from [LogRecord].[dbo].[account_position] order by userid"
	res=ms.dict_sql(sql)
	totalsql=""
	for item in res:
		userid=item['userid']
		ispass=0
		try:
			sql="select 1 from future.dbo.view_%s" % (userid)
			ms.insert_sql(sql)
			ispass=1
		except:
			sql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime],beizhu) values('%s',0,'%s',getdate(),'%s')" % (userid,0,'No view in 0.5 database')
			print sql
			ms.insert_sql(sql)
		if ispass==1:
			tempsql="select '%s' as [userID],STOCK as [stockID],Expr1 as position,GETDATE() as nowtime from future.dbo.view_%s" % (userid,userid)
			totalsql=totalsql+" union all "+tempsql
	totalsql=totalsql.strip(" union all ")
	totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) "+ totalsql
	ms.insert_sql(totalsql)

	#2 shangpin yingshe
	totalsql=""
	ms1 = MSSQL(host="139.196.104.105",user="future",pwd="K@ra0Key",db="Future")
	res=['05810058','032442']
	for item in res:
		userid=item
		tempsql="select '%s' as [userID],STOCK as [stockID],Expr1 as position,GETDATE() as inserttime from future.dbo.view_%s" % (userid,userid)
		totalsql=totalsql+" union all "+tempsql
	totalsql=totalsql.strip(" union all ")
	#totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) "+ totalsql
	tempres=ms1.dict_sql(totalsql)

	#3 stock yinghse
	sql="SELECT [Symbol]  ,[S_ID] FROM [Future].[dbo].[Symbol_ID] where Symbol in ('IC','IF','IH','TF','T')"
	res=ms.dict_sql(sql)
	symboldict={}
	for item in res:
		symboldict[item['Symbol']]=item['S_ID']
	sql="SELECT a.account,a.symbol,sum(a.ratio*b.position ) as Position  FROM [future].[dbo].[account_position_stock_yingshe] a left join [future].[dbo].[RealPosition] b on a.acanme=b.Name group by a.account,a.symbol"
	res=ms1.dict_sql(sql)
	for item in res:
		print "'"+item['symbol']+"'"
		symbol_id=symboldict[item['symbol']]
		sql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) values('%s','%s','%s',getdate())" % (item['account'],symbol_id,item['Position'])
		ms.insert_sql(sql)
	totalsql=""
	tempv=""
	for item in tempres:
		tempv=",('%s','%s','%s','%s')" % (item['userID'],item['stockID'],int(item['position']),item['inserttime'].strftime("%Y-%m-%d %H:%M:%S"))
		totalsql=totalsql+tempv
	totalsql=totalsql.strip(",")
	totalsql="insert into [LogRecord].[dbo].account_position_lilun([userID],[stockID],[position],[inserttime]) values%s" % (totalsql)
	ms.insert_sql(totalsql)




#得到账户，数据库仓位差异 三个list
def show_distinct():
	ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future") 
	nowday=datetime.datetime.now().strftime('%Y%m%d')
	#sql=" select aaa.userID as realuserID,aaa.stockID as realstockID,aaa.position as realposition,aaa.inserttime as realinserttime,  bbb.* from (        select * from  (   select a.userID,a.stockID,(a.longhave-a.shorthave) as position,inserttime from [LogRecord].[dbo].[account_position] a inner join (  select MAX(time) as time  ,userid   FROM [LogRecord].[dbo].[account_position]  where date='20161129' group by userid) b  on a.time=b.time and a.userID=b.userID )ka ) aaa full outer join (    select * from [LogRecord].[dbo].[account_position_lilun]  ) bbb     on aaa.userID=bbb.userID and aaa.stockID=bbb.stockID     where aaa.position<>bbb.position or (bbb.userID is null and aaa.position<>0) or (aaa.userID is null and bbb.position<>0 )    "
	sql="select aaa.userID as realuserID,aaa.stockID as realstockID,aaa.position as realposition,aaa.inserttime as realinserttime,  bbb.* from (        select * from  (   select a.userID,a.stockID,(a.longhave-a.shorthave) as position,inserttime from [LogRecord].[dbo].[account_position] a inner join (  select MAX(time) as time  ,userid   FROM [LogRecord].[dbo].[account_position]  where date='%s' group by userid) b  on a.time=b.time and a.userID=b.userID and a.date='%s')ka ) aaa full outer join (     select userID,stockID,sum(position)as position,MAX(inserttime)as inserttime  from [LogRecord].[dbo].[account_position_lilun]  group by userID,stockID ) bbb       on aaa.userID=bbb.userID and aaa.stockID=bbb.stockID  where aaa.position<>bbb.position or (bbb.userID is null and aaa.position<>0) or (aaa.userID is null and bbb.position<>0 ) and (bbb.userID in (select distinct userID from [LogRecord].[dbo].account_position)) order by aaa.userID" % (nowday,nowday)

	res=ms.dict_sql(sql)
	disticnt_set=[]
	lilun_miss_set=[]
	real_miss_set=[]
	for item in res:
		if item['realuserID'] is None:
			real_miss_set.append(item)
		if item['userID'] is None:
			lilun_miss_set.append(item)
		if item['realuserID'] is not None and item['userID'] is not None:
			disticnt_set.append(item)
	# print real_miss_set
	# print lilun_miss_set
	# print disticnt_set
	return real_miss_set,lilun_miss_set,disticnt_set


 