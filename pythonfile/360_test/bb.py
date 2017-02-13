import os
#coding=utf-8
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
import datetime
import time
import os
import numpy as np
import pandas as pd
#from openpyxl.writer.excel import ExcelWriter
from pandas.tseries import offsets
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
#ms = MSSQL(host="27.115.14.62:3888",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-
