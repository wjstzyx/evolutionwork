#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList

def change_lianxu(stname):
	sql="select top 1 stockdate from st_report where st=%s order by stockdate" % (stname)
	firsttime=ms.find_sql(sql)[0][0]
	sql="select 'update st_report set pp='+str(pp)+' where id='+str(id)+';' as script,pp,id,p from st_report where stockdate='%s' and st=%s" % (firsttime,stname)
	myscript=ms.find_sql(sql)[0]
	if myscript[1]!=0:
		print '--**** backup-script:'
		print myscript[0]
		print "--**** Need to do"
		sql="update st_report set pp=0 where id=%s" % (myscript[2])
		print sql
	lastpsig=myscript[3]
	sql="select stockdate,p,pp,id from st_report where st=%s and stockdate>'%s' order by stockdate" % (stname,firsttime)
	tiemres=ms.find_sql(sql)
	print "--************  Ready to Backup *************"
	for item in tiemres:
		if item[2]!=lastpsig:
			sql="update st_report set pp=%s where id=%s" % (lastpsig,item[3])
			ms.insert_sql(sql)
			tempsql="update st_report set pp=%s where id=%s;" % (item[2],item[3])
			print tempsql
		lastpsig=item[1]

def set_pp_zerp():
	sql="select id,p,pp,a.st,a.d,a.t from st_report a right join (select min(stockdate) as stockdate,st from st_report  group by st) temp on temp.ST=a.ST and temp.stockdate=a.stockdate where pp!=0 and PP is not null "
	res=ms.find_sql(sql)
	for item in res:
		if 	item[2]!=0:
			sql="update st_report set pp=%s where id=%s" % (item[2],item[0])
			print "--Ready to backup:"
			print sql
			sql="update st_report set pp=0 where id=%s" % (item[0])
			ms.insert_sql(sql)


def set_p_zerp():
	sql="select id,p,pp,a.st,a.d,a.t from st_report a right join (select max(stockdate) as stockdate,st from st_report  group by st) temp on temp.ST=a.ST and temp.stockdate=a.stockdate where p!=0 and P is not null and a.stockdate<='2016-04-1 09:49:00.000' order by a.stockdate "
	res=ms.find_sql(sql)
	for item in res:
		if 	item[1]!=0:
			sql="update st_report set p=%s where id=%s" % (item[1],item[0])
			print "--Ready to backup:"
			print sql
			sql="update st_report set p=0 where id=%s" % (item[0])
			ms.insert_sql(sql)





def fix_lianxu():
	sql="select * from (select SUM(P) as p,SUM(pp) as pp,SUM(p-pp) as aap,st from st_report group by st )aaa where aap!=0 order by st "
	#sql="select distinct ST_REPORT.ST from st_report inner join p_log p on p.st=st_report.st and p.ac='RbCX_QGtr' and p.symbol='RB' and p.d=st_report.d and st_report.type=0"
	res=ms.find_sql(sql)
	for item in res:
		print "--st: ",item[3]
		st=item[3]
		change_lianxu(st)




#检查特定的虚拟组和产品是否有问题


#set_pp_zerp()
#set_p_zerp()
fix_lianxu()
# change_lianxu('40768')