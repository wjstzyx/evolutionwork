import csv
import datetime
def aa():
	path=r'C:\Users\YuYang\Documents\Tencent Files\794513386\FileRecv\Index_20160923_zs.csv'
	reader = csv.reader(file(path, 'rb'))
	for line in reader:
		time=line[1]
		if len(time)==5:
			time='0'+time
		stockdate=datetime.datetime.strptime(line[0]+" "+time,"%Y%m%d %H%M%S")
		print stockdate

		print line 
aa()