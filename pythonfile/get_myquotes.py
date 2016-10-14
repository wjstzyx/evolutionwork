#coding=utf-8 
#!/usr/bin/env python
import sys
import csv
import os 
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")

#清理已有的数据记录
def del_quotes():
	delcmd="del /s C:\\_wenhua_\\wh6all\\Data\\*00*.dat"
	os.system(delcmd)
	delcmd="rd/s/q C:\\_wenhua_\\wh6all\\Data_Out"
	os.system(delcmd)



def change_to_csv(csvname='sss.csv',symbol=''):
	origincsvfile=r'C:\_wenhua_\wh6all\Data_Out\DCE\min1\%s' % (csvname)
	targetcsvfile=r'E:\data\%s.csv' % (symbol)
	print origincsvfile
	print targetcsvfile
	n=3
	csvfile = file(origincsvfile, 'rb')
	reader = csv.reader(csvfile)
	linelist=[]
	for line in reader:
		linelist.append(line)
	csvfile.close()
	csvfile = file(targetcsvfile, 'wb')
	writer = csv.writer(csvfile)
	for item in linelist[1:]:
		insertdate=item
		Date=insertdate[0]
		stockdate=Date[0:4]+'-'+Date[4:6]+'-'+Date[6:9]+' '+insertdate[1]
		Date=Date[0:4]+'/'+Date[4:6]+'/'+Date[6:9]
		Time=insertdate[1][0:5]
		Open=round(float(insertdate[2]),n)
		High=round(float(insertdate[3]),n)
		Low=round(float(insertdate[4]),n)
		Close=round(float(insertdate[5]),n)
		Volume=round(float(insertdate[6]),n)
		OpenInterest=round(float(insertdate[7]),n)
		content=[Date,Time,Open,High,Low,Close,Volume,OpenInterest]
		writer.writerow(content)
	csvfile.close()











#del_quotes()
change_to_csv(csvname='00001111.csv',symbol='DP')
