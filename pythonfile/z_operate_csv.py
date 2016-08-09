# coding: utf-8
import csv
csvfile = file('E:\data\STTrendlYP.csv', 'rb')
reader = csv.reader(csvfile)
for line in reader:

	# while '' in line:
	# 	line.remove('')
	dllName=line[2]
	stratid=line[1]
	period=int(line[4])*60
	numDoubleParas=len(line)-5
	mynum=0
	str0=''
	for i  in range(numDoubleParas):
		if line[5+i]!='':
			mynum=mynum+1
			str=' dblPara%s="%s"' % (i,line[5+i])
			str0=str0+str
	str1='<Strategy dllName="%s" stratid="%s" basebar="1m" period="%s" numDoubleParas="%s"' % (dllName,stratid,period,mynum)
	str2=str1+str0+' conid="RB" />'
	print str2




