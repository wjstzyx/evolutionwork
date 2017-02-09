from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import datetime
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
sql="select top 10 c,stockdate from Tsymbol"
res=ms.dict_sql(sql)
print res
aa=pd.DataFrame(res)
bb=pd.DataFrame([{'c':np.nan,'stockdate':'2016-12-20 09:47:00'},{'stockdate':'2017-12-20 09:39:00'}])
print aa
print bb
cc=aa.append(bb,ignore_index=True)
cc['stockdate'] = pd.to_datetime(cc['stockdate'])
#cc.sort(columns='stockdate')

cc['index'] = cc.index
cc = cc.sort_values(['stockdate','index'],ascending=[True,True])
cc = cc.fillna(method='ffill')


print cc

print 1
