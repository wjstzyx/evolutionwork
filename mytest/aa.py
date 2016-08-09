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

filepath="C:\\Users\\YuYang\\Documents\\Tencent Files\\794513386\\FileRecv\\00009206.csv"

def write_to_database(tablename,lastquotes,n):
	#Date  0,Time1,Open2,High3,Low4,Close5,Volume6,OpenInterest7,SettlementPrice
	insertdate=lastquotes
	Date=insertdate[0]
	stockdate=Date[0:4]+'-'+Date[4:6]+'-'+Date[6:9]+' '+insertdate[1]
	Date=Date[0:4]+'/'+Date[4:6]+'/'+Date[6:9]
	Time=insertdate[1][0:5]
	sql="select 1 from %s where stockdate='%s'" % (tablename,stockdate)
	res=ms.find_sql(sql)
	if res:
		sql="update %s set O=%s,C=%s,H=%s,L=%s,V=%s,OPI=%s where stockdate='%s'" % (tablename,round(float(insertdate[2]),n),round(float(insertdate[5]),n),round(float(insertdate[3]),n),round(float(insertdate[4]),n),round(float(insertdate[6]),n),round(float(insertdate[7]),n),stockdate)
		ms.insert_sql(sql)
	else:
		sql="insert into %s(O,C,H,L,V,OPI,D,T,stockdate) values(%s,%s,%s,%s,%s,%s,'%s','%s','%s')" % (tablename,round(float(insertdate[2]),n),round(float(insertdate[5]),n),round(float(insertdate[3]),n),round(float(insertdate[4]),n),round(float(insertdate[6]),n),round(float(insertdate[7]),n),Date,Time,stockdate)
		ms.insert_sql(sql)




def read_to_datanbase(filepath,tablename,n):
	csvfile = file(filepath, 'rb')
	reader = csv.reader(csvfile)
	linelist=[]
	for line in reader:
		linelist.append(line)
	line0=linelist[-1]
	line1=linelist[-2]
	line2=linelist[-3]
	if line0==line1:
		newquotes=line1	
		lastquotes=line2
	write_to_database(tablename,lastquotes,n)
	write_to_database(tablename,newquotes,n)





while(1):
	wenhuapath=""
	isdone1=0
	try:
		cmd="C:\\catchquotes\\readwenhua.exe"
		os.system(cmd)
		isdone1=1
	except:
		pass
	if isdone1=1:
		quoteslist=["\\CZCE\\min1\\00020140.csv"]
		for item in quoteslist:
			filepath=wenhuapath+item
			read_to_datanbase(filepath,'AG001_test',2)
	time.sleep(10)
	





#write_to_database('AG001_test',['20160803', '13:15:34', '408.000000', '408.000000', '408.000000', '408.000000', '15.000000', '40504.000000', '408.000000'],2)

