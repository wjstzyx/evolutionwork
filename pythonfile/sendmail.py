#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: UTF-8 -*-
import smtplib  
from email.mime.text import MIMEText  
mailto_list=['794513386@qq.com'] 
mail_host="smtp.sina.com"  #设置服务器
mail_user="yuyang_998"    #用户名
mail_pass="diannaodiaole"   #口令 
mail_postfix="sina.com"  #发件箱的后缀
  
def send_mail(to_list,sub,content):  
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    #msg = MIMEText(content,_subtype='plain',_charset='utf8')
    msg = MIMEText(content,_subtype='html',_charset='utf8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
if __name__ == '__main__':  
    if send_mail(mailto_list,"hello恩啊的的","hello world的</br>点发货速度"):  
        print "发送成功"  
    else:  
        print "发送失败"
