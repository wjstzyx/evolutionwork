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



stepmultilist=['StepMultigaosheng1','StepMultiI300w_up','StepMultituji1','StepMultituji2','StepMultituji3','StepMultidnhiboth','StepMultidnhiprofit','StepMultidnhisharp','StepMultidnshort']
for item in stepmultilist:
	cmd="python site_generate_dissitnct_V2.py %s" % (item)
	os.system(cmd)