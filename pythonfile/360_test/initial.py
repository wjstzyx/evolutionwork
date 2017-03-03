#coding=utf-8 
#!/usr/bin/env python
# pymssql
import sys
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
resList = ms.dict_sql("select top 2 * from st_report")
df1=pd.DataFrame(resList)
print df1

print resList
