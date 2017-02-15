#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime
import time
import os
import numpy as np
import pandas as pd
#from openpyxl.writer.excel import ExcelWriter
from pandas.tseries import offsets
from pandas import  Timestamp
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
#ms = MSSQL(host="27.115.14.62:3888",user="future",pwd="K@ra0Key",db="future")

class Global_value:
	def __init__(self,account,equity_day,backdays,backup_account):
		ms = MSSQL(host="192.168.0.5", user="future", pwd="K@ra0Key", db="future")
		self.account=account
		self.equity_day=equity_day
		self.backdays=backdays
		accountvalue=backup_account[account]
		self.step_acname=accountvalue[0]
		self.totalratio=accountvalue[1]
		self.lilun_result = []
		self.real_account_result = []
		self.real_huibao_result = []
		self.lilun_total = []
		self.real_total = []
		self.lilun_total_ZL = []
		self.real_total_ZL = []
		self.endtime = equity_day + " 16:00:00"
		sql = "select  distinct top (%s) convert(nvarchar(10),stockdate,120) as day from TSymbol where StockDate<='%s' order by day desc" % (
			backdays,equity_day)
		self.beginday = ms.find_sql(sql)
		self.begintime = self.beginday[-1][0]

def cal_ac_day_equity(g,acname):
	p_followac=g.step_acname
	ratio=g.totalratio
	postionpd, symbol = get_origin_position_list(g,acname)
	#获取 指数 价格 系列权益
	totalpo = get_Tsymbol_by_symbol(symbol, postionpd)
	newtotalpo = cal_equity(symbol, totalpo)
	write_position_csv(type='Lilun', symbol=symbol, endtime=equity_day, df1=newtotalpo)
	day_equity = equity_resharp(newtotalpo)
	tempdf=day_equity
	tempdf['day']=day_equity.index
	write_position_csv(type='Lilun_dayli_equity', symbol=symbol, endtime=equity_day, df1=tempdf)
	lastday_equity=day_equity['equity'][-1]
	lastday_equity_ZL=day_equity['equity_ZL'][-1]
	cal_day=day_equity.index[-1]
	lilun_total.append(lastday_equity)
	lilun_total_ZL.append(lastday_equity_ZL)
	print cal_day,acname,lastday_equity,lastday_equity_ZL
	lilun_result.append([cal_day,acname,lastday_equity,lastday_equity_ZL])




def main_get_lilun(lilun_g):
	sql="select * from (select distinct f_ac from p_follow where ac='%s') a order by f_ac" % (lilun_g.step_acname)
	myres=ms.dict_sql(sql)
	for myitem in myres:
		#print myitem
		cal_ac_day_equity(lilun_g,myitem['f_ac'])
	print '####lilun_total',sum(lilun_g.lilun_total)





backup_account = {'666061010':['StepMultiI300w_up',2.2],'':[]}

print 'step1 lilun equity'
lilun_g=Global_value('666061010','2017-01-20',21,backup_account)
main_get_lilun(lilun_g)