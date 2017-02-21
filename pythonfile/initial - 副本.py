#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

aaalist=[
[datetime.datetime(2016, 1, 1, 0, 0), ['pStepMultituji1_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultituji1_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultituji1_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultituji1_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultituji1_P.csv']]
,[datetime.datetime(2016, 3, 1, 0, 0), ['pStepMultituji1_P.csv']]
,[datetime.datetime(2016, 4, 30, 0, 0), ['pStepMultituji2_P.csv', 'pStepMultituji2_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultituji2_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultituji2_P.csv', 'pStepMultituji2_P.csv', 'pStepMultidnhiprofit_P.csv']]
,[datetime.datetime(2016, 6, 29, 0, 0), ['pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultituji1_P.csv']]
,[datetime.datetime(2016, 8, 28, 0, 0), ['pStepMultiI_up_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultituji1_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultiI_up_P.csv']]
,[datetime.datetime(2016, 10, 27, 0, 0), ['pStepMultidnhiprofit_P.csv', 'pStepMultituji1_P.csv', 'espp_P.csv', 'Pmid_P.csv', 'pStepMultituji1_P.csv', 'pStepMultituji1_P.csv', 'pStepMultituji1_P.csv', 'pStepMultidnhiprofit_P.csv', 'espp_P.csv']]
,[datetime.datetime(2016, 12, 26, 0, 0), ['pStepMultidnhiprofit_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultiI_up_P.csv', 'pStepMultidnhiprofit_P.csv', 'pStepMultidnhiprofit_P.csv']]
]
print aaalist