#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def check_P_log_short_date():
	sql="select a.*,tD from P_log a right join (select distinct D as tD from st_report) temp on a.D=temp.tD where d is  null"
	res=ms.dict_sql(sql)
	if res:
		print "p_log  表中记录与 st_report 表比较 缺少的时间点："
		print "补全 p_log 表中相关记录"
		for item in res:
			print item['tD']
	else:
		print "Same! Ok!"



def check_Tsymbol_short_date():
	sql="select a.stockdate,tstockdate from Tsymbol a right join (select distinct stockdate as tstockdate from st_report where stockdate>='2015-03-03 00:00:00.000') temp on a.stockdate=temp.tstockdate where stockdate is  null"
	res=ms.dict_sql(sql)
	if res:
		print "Tsymbol  表中记录与 st_report 表比较 缺少的时间点："
		print "可以删除st_report中的相关记录或者补全Tsymbol表中相关记录"
		for item in res:
			print item['tstockdate']
	else:
		print "Same! Ok!"





def check_P_log_short_date_teli(acname,symbol):
	sql="select a.*,tD from P_log a right join (select distinct D as tD from st_report) temp on a.D=temp.tD where d is  null"
	res=ms.dict_sql(sql)
	if res:
		print "p_log  表中记录与 st_report 表比较 缺少的时间点："
		print "补全 p_log 表中相关记录"
		for item in res:
			print item['tD']
	else:
		print "Same! Ok!"



def check_Tsymbol_short_date_teli(acname,symbol):
	sql="select a.stockdate,tstockdate from Tsymbol a right join (select distinct stockdate as tstockdate from st_report where stockdate>='2015-03-03 00:00:00.000') temp on a.stockdate=temp.tstockdate where a.symbol='%s' and stockdate is  null" % (symbol)
	res=ms.dict_sql(sql)
	if res:
		print "Tsymbol  表中记录与 st_report 表比较 缺少的时间点："
		print "可以删除st_report中的相关记录或者补全Tsymbol表中相关记录"
		for item in res:
			print item['tstockdate']
	else:
		print "Same! Ok!"





check_Tsymbol_short_date()
# check_P_log_short_date()
print "Finish"