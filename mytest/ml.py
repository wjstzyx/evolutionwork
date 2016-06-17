#coding=utf-8 
#!/usr/bin/env python
import urlparse

import sys
import datetime
import time
reload(sys)
sys.setdefaultencoding('utf8')
a='\r\ndfdddd\r\ndfddd'
print a.strip('\r\n')

ac='9DUD1'
symbol='IF'
type=0
D=160616
sql="select * into  #temp_quanyi_new from (select '%s' as ac,'%s' as symbol,'%s' as type,temp.id,p,PP,p_size,ratio,st,o.stockdate from tsymbol o inner join (select st_report.id,st_report.p,st_report.pp,p.symbol,st_report.stockdate,st_report.st,p.p_size,p.ac,p.ratio,st_report.type from st_report  inner join p_log p on p.st=st_report.st and p.ac='%s' and p.symbol='%s' and p.d=%s and st_report.type=%s ) temp on temp.stockdate=o.stockdate and o.symbol=temp.symbol where o.symbol='%s' ) temp " % (ac,symbol,type,ac,symbol,D,type,symbol)
print sql