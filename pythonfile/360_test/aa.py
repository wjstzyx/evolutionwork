#coding=utf-8
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import  os
import csv
import datetime
from dbconn import MSSQL
#ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
##读入excel

def in_putdata():
	xlsfile = r'D:\test\aaa.csv'
	df0 = pd.read_csv(xlsfile,encoding='gbk',dtype=str)
	mydata=df0[[u'买卖方向',u'合约',u'数量',u'价格',u'成交日期',u'成交时间']]
	mydata=mydata[pd.notnull(mydata[u'成交时间'])]

	mydata=mydata.as_matrix()
	for item in mydata:
		conid=item[1]
		if item[0]==u'买':
			ratio=1
		else:
			ratio=-1
		amont=item[2]
		price=item[3].replace(',','')
		sql="insert into [Future].[dbo].[test_tradelog]([Direction],[InstrumentID],[Volume],[Price],[TradeDate],[TradeTime]) values(%s,'%s',%s,%s,'%s','%s')" % (ratio,conid,amont,price,item[4],item[5])
		print sql
		ms.insert_sql(sql)





def get_delta_info(symbol):
	sql="  select Future.dbo.m_getstr([InstrumentID]) as symbol,Direction,[Volume],  Price,convert(datetime,substring(TradeDate,0,5)+'-'+substring(TradeDate,5,2)+'-'+substring(TradeDate,7,2)+' '+[TradeTime],120) as stockdate from      [Future].[dbo].[test_tradelog] where Future.dbo.m_getstr([InstrumentID])='%s' order by stockdate " % (symbol)
	res=ms.dict_sql(sql)
	newdata = []
	lastrecord = res[0]
	deltaequity = 0
	tempresult=[[lastrecord['Direction'],lastrecord['Volume'],lastrecord['Price']]]
	for item in res:
		mydatetime=item['stockdate'].strftime('%Y-%m-%d %H:%M')
		if mydatetime == lastrecord['stockdate'].strftime('%Y-%m-%d %H:%M'):
			tempresult.append([item['Direction'],item['Volume'],item['Price']])
			#deltaequity = ((item['Price']) - (lastrecord['Price'])) * item['Volume'] * item['Direction']+0.01
		if mydatetime > lastrecord['stockdate'].strftime('%Y-%m-%d %H:%M'):
			#computer deltaequity
			if len(tempresult)>1:
				#print tempresult
				myprice = tempresult[-1][2]
				#print 'tempresult',mydatetime,myprice,tempresult
				for item1 in tempresult:
					#print deltaequity
					deltaequity =deltaequity+(item1[2] - myprice) * (-item1[1]) * item1[0]
			else:
				deltaequity=0

			newdata.append([lastrecord['stockdate'].strftime('%Y-%m-%d %H:%M') + ':00', lastrecord['symbol'], lastrecord['Price'], deltaequity])
			deltaequity = 0
			tempresult=[ [item['Direction'], item['Volume'], item['Price']]]
		lastrecord = item
	# add last line
	newdata.append([mydatetime + ':00', lastrecord['symbol'], lastrecord['Price'], deltaequity])
	aaa=pd.DataFrame(newdata,columns=['stockdate','symbol','price','deltapoint'])
	return aaa



def write_position_csv(type,symbol,endtime='2017-11-12',df1=1):
	filepath = os.path.split(os.path.realpath(__file__))[0]

	parentpath = os.path.dirname(filepath)
	newpath=parentpath+'\\all_future_position\\'+str(endtime)+"\\"+str(symbol)+'.csv'
	a_parent=os.path.dirname(newpath)
	if  not os.path.isdir(a_parent):
		os.makedirs(a_parent)
	df1.to_csv(newpath,sep=',',)
	print '## generate  position file ',symbol,newpath





print  1
# in_putdata()
# get_delta_info('ru')
#write_position_csv(11,1)
exit()
