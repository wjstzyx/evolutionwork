#coding=utf-8 
#!/usr/bin/env python
import sys
import os
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
# username  用户名
# password_md5   密码
# mobile  手机号
# apikey  apikey秘钥
# content  短信内容
# startTime  UNIX时间戳，不写为立刻发送，http://tool.chinaz.com/Tools/unixtime.aspx （UNIX时间戳网站）
# 1、GBK编码提交的
#	首先urlencode短信内容（content），然后在API请求时，带入encode=gbk
#
#	2、UTF-8编码的
#
#	将content 做urlencode编码后，带入encode=utf8或utf-8
#	http://m.5c.com.cn/api/send/index.php?username=XXX&password_md5=XXX&apikey=36e74088db48842ce54ee65643b8667a&mobile=XXX&content=%E4%BD%A0%E5%A5%BD%E6%89%8D%E6%94%B6%E7%9B%8A%E9%9F%A6&encode=utf8
#
#示例
# 
#Return Code										Description
#success:msgid								提交成功，发送状态请见4.1
#error:msgid								提交失败
#error:Missing username						用户名为空
#error:Missing password 					密码为空
#error:Missing apikey						APIKEY为空
#error:Missing recipient					手机号码为空
#error:Missing message content				短信内容为空
#error:Account is blocked					帐号被禁用
#error:Unrecognized encoding				编码未能识别
#error:APIKEY or password error				APIKEY 或密码错误
#error:Unauthorized IP address				未授权 IP 地址
#error:Account balance is insufficient		余额不足
#error:Black keywords is:党中央				屏蔽词

#import urllib.parse
import urllib
import urllib2

def sendsms(mobile='',content=''):
	try:
		url = 'http://m.5c.com.cn/api/send/index.php'		#如连接超时，可能是您服务器不支持域名解析，请将下面连接中的：【m.5c.com.cn】修改为IP：【115.28.23.78】
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		encode = 'UTF-8'									#页面编码和短信内容编码为GBK。重要说明：如提交短信后收到乱码，请将GBK改为UTF-8测试。如本程序页面为编码格式为：ASCII/GB2312/GBK则该处为GBK。如本页面编码为UTF-8或需要支持繁体，阿拉伯文等Unicode，请将此处写为：UTF-8
		username = 'yuanlan'									#用户名
		password_md5 = '200820E3227815ED1756A6B531E7E0D2'	#32位MD5密码加密，不区分大小写（qwe123）
		apikey = 'b4679c42c3712dfa214aa88cad90cd9d';		#apikey秘钥（请登录 http://m.5c.com.cn 短信平台-->账号管理-->我的信息 中复制apikey）
		# mobile='17091925075'								#手机号,只发一个号码：13800000001。发多个号码：13800000001,13800000002,...N 。使用半角逗号分隔。					
		# content = '【Thunder】\r\nasas1程序出错2016-09-08 14:51:12\r\nasas1程序出错2016-09-08 14:51:12\r\nasas1程序出错2016-09-08 14:51:12\r\n'		# 要发送的短信内容，特别注意：签名必须设置，网页验证码应用需要加添加【图形识别码】。
		if len(mobile)<7:
			mobile='13764504303'  #如果手机号不符合规范，则默认发送到13764504303
		values = {'username' : username,    
		         'password_md5' : password_md5,    
		         'apikey' : apikey,
		         'mobile' : mobile,
		         'content' : content,
				'encode' : encode }
		headers = { 'User-Agent' : user_agent }
		#data = urllib.parse.urlencode(values)
		data = urllib.urlencode(values)
		req = urllib2.Request(url+'?'+data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		if "success" in the_page:
			return 1

		else:
			return 0

		print(the_page)
	except:
		return 0

result=sendsms('13764504303','huhuuhu')
print "ddd"
print result