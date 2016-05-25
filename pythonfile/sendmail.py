#coding=utf-8 
#!/usr/bin/env python
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
from dbconn import MSSQL
ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
# resList = ms.find_sql("select top 2 * from st_report")
# print resList
# -*- coding: UTF-8 -*-
import smtplib  
from email.mime.text import MIMEText  
# mailto_list=['yuyang_998@sina.com'] 
mailto_list=['794513386@qq.com','yuyang@evolutionlabs.com.cn'] 
mail_host="smtp.evolutionlabs.com.cn"  #设置服务器
mail_user="warning@evolutionlabs.com.cn"    #用户名
mail_pass="El104104"   #口令 
mail_postfix="evolutionlabs.com.cn"  #发件箱的后缀
sendmail='warning@evolutionlabs.com.cn'
#rwecstmzqbwzbchh
# mailto_list=['yuyang_998@sina.com'] 
# mail_host="smtp.qq.com"  #设置服务器
# mail_user="794513386@qq.com"    #用户名
# mail_pass="rwecstmzqbwzbchh"   #口令 
# mail_postfix="qq.com"  #发件箱的后缀
# sendmail='794513386@qq.com'

# mailto_list=['elwarning@sina.com'] 
# mail_host="smtp.sina.com"  #设置服务器
# mail_user="elwarning"    #用户名
# mail_pass="qwe123"   #口令 
# mail_postfix="sina.com"  #发件箱的后缀
# sendmail='elwarning@sina.com'

def send_mail(to_list,sub,content):  
    #me="elwarning"+"<"+mail_user+"@"+mail_postfix+">"  
    me=sendmail
    # msg = MIMEText(content,_subtype='plain',_charset='utf8')
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
    time=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    if send_mail(mailto_list,"测试报警%s" % (time),"这是一封测试邮件，请忽略 %s" % (time)):  
        print "这是一封测试邮件，请忽略 %s" % (time)
        print "发送成功"  
    else:  
        print "发送失败"
