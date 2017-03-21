# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:54:04 2017

@author: jesse
"""



from datetime import datetime,timedelta
import pandas as pd
import MySQLdb
import time
import numpy as np

class PyAB_Alert():

    '''
    alert events:
    1. barcount < N
    2. log_time delta > 1min
    3. now > bar_start_time + interval
    4. now > 8:45 but log_time < 8:45

    alert struct message/json/dict :
    {INT 'type': 1/2/3/4
     STRING 'message': ''
     dict 'content'
         { 'varname': list
            
         } 
    }

    '''

    def __init__(self):

        self.alert_msgs = list()
        # self.alert_msgs.append(u'ABLog数据库无数据或损坏')
        # self.alert_msgs.append(u'AB历史数据过少')
        # self.alert_msgs.append(u'AB批处理速度降低')
        # self.alert_msgs.append(u'AB信号未更新超过1个Bar')
        # self.alert_msgs.append(u'AB批处理开盘前未开启')

        self.alert_msgs.append(u'NO ERROR')
        self.alert_msgs.append(u'AB barcount not enough')
        self.alert_msgs.append(u'AB processing SLOW')
        self.alert_msgs.append(u'AB Data NOT updated')
        self.alert_msgs.append(u'AB NOT started')

        self.mysqldb_conn = MySQLdb.connect(host='192.168.0.148', port=3306, user='root', passwd='K@ra0Key', db='LogRecord',charset='utf8')

        # python_ab process signals from 8.30 to 15.30  20.30 to 3.30
        self.ab_day_session_start = timedelta(hours=8,minutes=50)
        self.ab_night_session_start = timedelta(hours=20,minutes=50)

        self.alert_list = list()

    def alert(self,msg_type,df=pd.DataFrame()):
        '''

        :param msg_type: 0 1 2 3 4 : for
        :param df: sql query result showing in a html table
        :return: dict passed to yuyang's monitor http server
        '''
        msg = dict()
        msg['type'] = msg_type
        msg['message'] = self.alert_msgs[msg_type]
        msg['html_content'] = df.to_html(index=False).replace('class="dataframe"','class="table table-bordered table-hover table-striped"')
        #df=df.values()

        self.alert_list.append(msg)
        return msg


    def qry2pd(self,qry):
        return pd.read_sql(qry,self.mysqldb_conn)


    def get_alerts(self):
        '''

        :return: lists containing msgs
        '''

        self.alert_barcount()
        self.alert_logtime()

        self.alert_datadelay()
        self.alert_abnotstart()
        return self.alert_list

    def run(self):

        self.alert_list = list()

        self.get_alerts()

        print "list len:",len(self.alert_list),self.alert_list

        return self.alert_list


    
        
    def alert_barcount(self):
        df = self.qry2pd("select virtual_group,barcount,timeframe_in_min,ps_file from logrecord.ablog_snapshot where barcount < 2000 order by last_log_time desc , timeframe_in_min desc")
        if len(df) < 1:
            self.alert(0)
        else:
            self.alert(1,df)
            
    def alert_logtime(self):
        
        df = self.qry2pd("select distinct last_log_time from logrecord.ablog order by last_log_time desc limit 5")
        
        if len(df) < 1:
            self.alert(0)
        else:
            df.sort_index(ascending=False,inplace=True)
            delta_time = df['last_log_time'].diff().sum()
            if delta_time > timedelta(seconds=50):
                self.alert(2,df)

    def in_session(self,session='day'):
        # session = day,night
        ctime = datetime.now()
        if session == 'day':
            return ctime > datetime(ctime.year,ctime.month,ctime.day, 9 ,0,0) and ctime < datetime(ctime.year,ctime.month,ctime.day, 15 ,0,0)
        else:
            return ctime > datetime(ctime.year, ctime.month, ctime.day, 21, 0, 0) or ctime < datetime(ctime.year,ctime.month,ctime.day, 2, 30,0)

    def qry_datadelay(self,qry,session='day'):
        df = self.qry2pd(qry)
        if len(df) < 1:
            self.alert(0)
        else:
            tf = df['timeframe_in_min'].values[0]
            ctime = datetime.now()
            target_time = df['bar_start_time'] + timedelta(minutes=int(tf))
            delay_count = (df['last_log_time'] > target_time).sum()
            # if not in session that is uncorrected warning
            #print np.datetime64(ctime),(target_time + timedelta(minutes=1)).values[0]
            #print delay_count,self.in_session(session)

            if np.datetime64( ctime) > (target_time + timedelta(minutes=1)).values[0] and delay_count > 0 and self.in_session(session):
                alert(3, df)

    def alert_datadelay(self):
        # include day and daynight
        day_qry = "select last_log_time,timeframe_in_min,bar_start_time,ps_file from logrecord.ablog_snapshot where ps_file like '%\\\\_day%'  order by timeframe_in_min asc, last_log_time desc limit 5"
        # include night and daynight
        night_qry = "select last_log_time,timeframe_in_min,bar_start_time,ps_file from logrecord.ablog_snapshot where ps_file like '%night\\\\%'  order by timeframe_in_min asc, last_log_time desc limit 5"

        self.qry_datadelay(day_qry,'day')
        self.qry_datadelay(night_qry,'night')



    def alert_abnotstart(self):
        # include day and daynight
        df = self.qry2pd("select last_log_time, virtual_group, ps_file from logrecord.ablog_snapshot where  ps_file like '%\\\\_day%' order by last_log_time desc limit 5")
        if len(df) < 1:
            self.alert(0)
        else:
            ctime = datetime.now()
            today =datetime(ctime.year,ctime.month,ctime.day, 0 ,0,0)
            # before session start
            if not self.in_session('day') and np.datetime64( ctime) > today + self.ab_day_session_start and df['last_log_time'].values[0] < np.datetime64( today + self.ab_day_session_start - timedelta(minutes=2) ):
                self.alert(4,df)

        df = self.qry2pd(
            "select last_log_time, virtual_group, ps_file from logrecord.ablog_snapshot where  ps_file like '%night\\\\%' order by last_log_time desc limit 5")
        if len(df) < 1:
            self.alert(0)
        else:
            ctime = datetime.now()
            today = datetime(ctime.year, ctime.month, ctime.day, 0, 0, 0)
            # before session start
            if not self.in_session('night') and np.datetime64( ctime) > today + self.ab_night_session_start and df['last_log_time'].values[0] < np.datetime64( today + self.ab_day_session_start - timedelta(minutes=2) ):
                self.alert(4, df)


if __name__=='__main__':
    al = PyAB_Alert()
    al.run()

    
                   
                   

