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
import multiprocessing
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: utf-8 -*-



stepmultilist=['StepMultigaosheng1','StepMultiI300w_up','StepMultituji1','StepMultituji2','StepMultituji3','StepMultidnhiboth','StepMultidnhiprofit','StepMultidnhisharp','StepMultidnshort']
#stepmultilist=['newtuji300']


def sub_main(item):
	cmd = "python site_generate_dissitnct_V4.py %s" % (item)
	os.system(cmd)
	cmd = "python site_acname_zhuli_equity.py %s" % (item)
	os.system(cmd)


def sub_main_merge(item):
	cmd = "python site_generate_dissitnct_V4.py %s" % (item)
	os.system(cmd)
	cmd = "python site_acname_zhuli_equity.py %s" % (item)
	os.system(cmd)


if __name__ == "__main__":
	threads_N = 6
	multiprocessing.freeze_support()
	pool = multiprocessing.Pool(processes=threads_N)

	stepmultilist = ['StepMultidnhiboth', 'StepMultidnshort', 'StepMultidnhiprofit', 'StepMultidnhisharp',
	                 'StepMultigaosheng1', 'StepMultiI300w_up', 'StepMultituji1', 'StepMultituji2', 'StepMultituji3']
	#stepmultilist = ['newtuji300']
	for item in stepmultilist:
		# add process to pool
		if threads_N > 1:
			# print multiprocessing.current_process().name
			pool.apply_async(sub_main, (item,))
		else:
			sub_main(item, )

	print "Process Pool Closed, Waiting for sub Process Finishing..."
	pool.close()
	pool.join()
	print 'Finished sub_main'

	# meger_jieti = ['newtuji300']
	# for item in meger_jieti:
	# 	# add process to pool
	# 	if threads_N > 1:
	# 		# print multiprocessing.current_process().name
	# 		pool.apply_async(sub_main_merge, (item,))
	# 	else:
	# 		sub_main_merge(item, )
	#
	# print "Process Pool Closed, Waiting for sub Process Finishing..."
	# pool.close()
	# pool.join()
	# print 'Finished sub_main_merge'
