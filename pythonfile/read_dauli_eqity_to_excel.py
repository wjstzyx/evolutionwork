#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
import xlwt
book=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=book.add_sheet('dede',cell_overwrite_ok=True)
sheet.write(0,0,'fu对对对ck')
book.save('C:\YYfiles\\evolutionwork\\mytest\\test.xls')
