#coding=utf-8 
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import os
import csv
import pandas as pd
import numpy as np
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-



stepmultilist=['StepMultidnhiboth','StepMultidnshort','StepMultidnhiprofit','StepMultidnhisharp','StepMultigaosheng1','StepMultiI300w_up','StepMultituji1','StepMultituji2','StepMultituji3']
stepmultilist=['StepMultigaosheng1']
equity_day='2017-02-15'
backday=60
ratio=1
for item in stepmultilist:
	cmd="python _step1_multi_lilun_real_time_equity_model.py %s %s % s %s position" % (item,equity_day,ratio,backday)
	print cmd
	os.system(cmd)
	cmd='python _step2_merge_all_future.py %s %s position' % (equity_day,item)
	print cmd 
	os.system(cmd)