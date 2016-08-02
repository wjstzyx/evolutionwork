# -*- coding: gb18030 -*- 
import string, os
import shutil
from dbconn import MSSQL
from collections import Counter
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
import sys
reload(sys)
import pydot
sys.setdefaultencoding('utf-8')
import datetime

# sql="select quanyi as quanyia,D from dailyquanyi where ac='RBQGSTTR_TG' and symbol='RB' and D>=151020 order by D" 
# res1=ms.find_sql(sql)
# print res1[:3]
sql="select top 17 acname as ac,quanyisymbol as symbol from [LogRecord].[dbo].[quanyicaculatelist] where quanyisymbol in ('RB') and iscaculate=1 order by sortnum"

				else:
					if iskeep==1:
						temp=[StockDate,C,temppositionlist[-1][2]]
						mymewquote.append(temp)
						lastappend=temp