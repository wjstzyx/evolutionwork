#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
import math
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList


#	account=11801666,return {u'995': 5.0, u'906': 5.0, u'9B7': 10.0, u'9ZA': 5.0, u'11803593': 25.0}
# def get_ac_ratio(account):
# 	#获取总账户配置的虚拟组的ratio
# 	sql="WITH Emp AS ( SELECT ac,F_ac,ratio FROM  p_follow WHERE   ac='%s' UNION ALL  SELECT   D.AC,D.F_ac,D.ratio*emp.ratio/100 FROM   Emp         INNER JOIN p_follow d ON d.ac = Emp.F_ac)SELECT AC,f_AC,ratio FROM  Emp" % (account)
# 	res=ms.dict_sql(sql)
# 	accountlist=[]
# 	aclist=[]
# 	for item in res:
# 		accountlist.append(item['AC'])
# 		aclist.append(item['f_AC'])
# 	accountlist=list(set(accountlist))
# 	aclist=list(set(aclist))
# 	# print accountlist
# 	# print aclist
# 	ac_ratio={}
# 	for item in aclist:
# 		ac_ratio[item]=0
# 	for item in res:
# 		ac_ratio[item['f_AC']]=ac_ratio[item['f_AC']]+item['ratio']
# 	# print ac_ratio
# 	for key in accountlist:
# 		if ac_ratio.has_key(key):
# 			del ac_ratio[key]
# 	# print ac_ratio
# 	return ac_ratio


# def get_dailyquanyi(account):
# 	ac_ratio=get_ac_ratio(account)
# 	totalquanyi=[]
# 	for key in ac_ratio:
# 		ratio=ac_ratio[key]
# 		if ratio>0:
# 			sql="SELECT [quanyisymbol]  FROM [LogRecord].[dbo].[quanyicaculatelist] where acname='%s'" % (key)
# 			res=ms.dict_sql(sql)
# 			if not res:
# 				# print {"ispass":0,"result":"%s does not has equity" % (key)}
# 				return {"ispass":0,"result":"%s does not has equity" % (key)}
# 			else:
# 				symbol=res[0]['quanyisymbol']
# 				acname=key
# 				sql="select D,quanyi as  quanyia from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=160801 order by D" % (acname,symbol)
# 				res1=ms.find_sql(sql)
# 				#乘以ratio
# 				newres1=[]
# 				for item in res1:
# 					newres1.append([item[0],item[1]*ratio/10.0])
# 				totalquanyi=add_time_series(totalquanyi,newres1)
# 				totalquanyi=sorted(totalquanyi,key=lambda a :a[0])
# 				# for item in totalquanyi:
# 				# 	print item 
# 				return {"ispass":1,"result":totalquanyi}


# def add_time_series(totalquanyi,res1):
# 	totalquanyitime=[k[0] for k in totalquanyi]
# 	res1time=[k[0] for k in res1]
# 	totalquanyidict={}
# 	for item in totalquanyi:
# 		totalquanyidict[item[0]]=item[1]
# 	res1dict={}
# 	for item in res1:
# 		res1dict[item[0]]=item[1]
# 	daylist=list(set(totalquanyitime).union(set(res1time)))
# 	daylist=sorted(daylist)
# 	totalquanyilastvalue=0
# 	res1lastvalues=0
# 	result={}
# 	for item in daylist:
# 		tempvalue=0
# 		if item in totalquanyitime:
# 			totalquanyilastvalue=totalquanyidict[item]
# 		if item in res1time:
# 			res1lastvalues=res1dict[item]
# 		tempvalue=totalquanyilastvalue+res1lastvalues
# 		result[item]=tempvalue
# 	result=sorted(result.iteritems(), key=lambda d:d[1], reverse = False)
# 	return result


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
				sql="select D,(quanyi-%s) as  quanyia from dailyquanyi_V2 where ac='%s' and symbol='%s' and D>=%s order by D" % (initoalquanyi,acname,symbol,fromDdy)
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
		tempvalue=totalquanyilastvalue+res1lastvalues
		result[item]=tempvalue
	result=sorted(result.iteritems(), key=lambda d:d[1], reverse = False)
	return result


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


def kpi_tongji(result,lilunquanyi):
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





















result=get_dailyquanyi('70700132',150101)
result=result["result"]
(tempday,lilunquanyi,realquanyi)=range_series(result,[])
kpi_tongji(result,lilunquanyi)
