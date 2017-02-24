#coding=utf-8
#!/usr/bin/env python
import sys, urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
import os
import pandas as pd
import numpy as np
import datetime
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-

root=r'C:\Users\YuYang\Desktop\homework2\data'
mnistdata=r'C:\Users\YuYang\Downloads\mnist.pkl.gz'
x_data=np.load(root+"\\X.npy")
y_data=np.load(root+"\\T.npy")

import pickle
import gzip


with gzip.open(mnistdata) as fp:
	(training_data_x,training_data_y), (test_data_x,test_data_y) = pickle.load(fp)

print 1

