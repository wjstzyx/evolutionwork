#coding=utf-8 
#!/usr/bin/env python
import urllib2
import urllib
import re
from bs4 import BeautifulSoup
import time

def get_html_fisrt(company_name):
    url="http://www.qichacha.com/search?key=%s&index=1" % (company_name)
    data={}
    data['form-username']='yy'
    data['form-password']='yy'
    head={}
    head['Host']='www.qichacha.com'
    head['Cookie']='gr_user_id=ebae3fa1-0b62-401e-acf1-eb5e8b41e64a; _uab_collina=148289743557944427699563; _umdata=BA335E4DD2FD504FDEC9FAE73C3930C7409B9CF2A1B73C7EFD2A8B822728E1A8A9A33920E2EC98FA5362A6130ADF3A03D95E18ADB9D27BC839392DF9A2E1B0DAA59E0C1C1AB29795B1C49F68AB8A4E54A2E42A51987920ED400BA858E232B6B7; PHPSESSID=pckr52088mfgo9rc3b2p12eh24; gr_session_id_9c1eb7420511f8b2=a48b0b10-d534-4f5e-ad5e-6589e98fae39; CNZZDATA1254842228=1940133115-1482893051-%7C1482903851'
    data = urllib.urlencode(data)
    req=urllib2.Request(url,data,head)
    response=urllib2.urlopen(req)
    html=response.read()
    return html


def company_detail(uniqueid,companyname):
    url="http://www.qichacha.com/company_getinfos?unique=%s&companyname=apple&tab=base" % (uniqueid)
    data={}
    data['form-username']='yy'
    data['form-password']='yy'
    head={}
    head['Host']='www.qichacha.com'
    head['Cookie']='gr_user_id=ebae3fa1-0b62-401e-acf1-eb5e8b41e64a; _uab_collina=148289743557944427699563; _umdata=BA335E4DD2FD504FDEC9FAE73C3930C7409B9CF2A1B73C7EFD2A8B822728E1A8A9A33920E2EC98FA5362A6130ADF3A03D95E18ADB9D27BC839392DF9A2E1B0DAA59E0C1C1AB29795B1C49F68AB8A4E54A2E42A51987920ED400BA858E232B6B7; PHPSESSID=pckr52088mfgo9rc3b2p12eh24; gr_session_id_9c1eb7420511f8b2=a48b0b10-d534-4f5e-ad5e-6589e98fae39; CNZZDATA1254842228=1940133115-1482893051-%7C1482903851'
    data = urllib.urlencode(data)
    req=urllib2.Request(url,data,head)
    response=urllib2.urlopen(req)
    html=response.read()
    return html


def get_wantedname(myname,unique_n):
    html=company_detail(unique_n,myname)
    soup=BeautifulSoup(html,"html.parser")
    listaaa=soup.find_all('li')
    recon=[]
    for item in listaaa:
        # print item 
        cont= item.get_text()
        aaa=cont.split(u'\uff1a')
        tempc=[aaa[0].strip(' '),aaa[1].strip(' ')]
        recon.append(tempc)
    return recon





def soup_parse(company_name=""):
    html=get_html_fisrt(company_name)
    soup=BeautifulSoup(html,"html.parser")
    lista=soup.find_all(href=re.compile("firm_.*.shtml"))
    content_li = list()
    for item in lista:
        myname=item.get_text()
        unique_id=item.attrs['href']
        unique_id=unique_id.split('/firm_')[1].split('.shtml')[0]
        if myname!='  ':
            content_li.append( [ myname,  unique_id ] )
    #begin search detail
    contentlist=[]
    for item in content_li:
        to_write=get_wantedname(item[0],item[1])
        mydict={}
        for item1  in to_write:
            mydict[item1[0]]=item1[1]
            # print item[0],item1[0],item1[1]
        #judge is have
        wanted_title=[u'组织机构代码',u'法定代表人']
        for iitem in wanted_title:
            tempc=[item[0]]
            if mydict.has_key(iitem):
                tempc.append(mydict[iitem])
            else:
                tempc.append(u'无')
        contentlist.append(tempc)
        time.sleep(0.5)
    for tiem in contentlist:
        print item 

        
    


   
soup_parse('远澜')




