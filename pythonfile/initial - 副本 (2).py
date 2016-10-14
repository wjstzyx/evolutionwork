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


res1=[(-2832.7, 20160926), (-2832.7, 20160927), (109023.8, 20161014)]
res2=[]

(tempday,lilunquanyi,realquanyi)=change_delta_toaccumu(res1,res2)
print lilunquanyi