#coding=utf-8 
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pymssql
class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.cur=self.__GetConnect()


    def __GetConnect(self):

        if not self.db:
            raise(NameError,"no database info")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"failed connection")
        else:
            return cur

    def find_sql(self,sql):
        # cur = self.__GetConnect()
        self.cur.execute(sql)
        resList = self.cur.fetchall()
        # self.conn.close()
        return resList

    def dict_sql(self,sql):
        # cur = self.__GetConnect()
        self.cur.execute(sql)
        resList = dictfetchall(self.cur)

        # self.conn.close()
        return resList

    def insert_sql(self,sql):   
        self.cur.execute(sql)
        self.conn.commit()
        # self.conn.close()

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def main():
    ms = MSSQL(host="192.168.0.5",user="future",pwd="K@ra0Key",db="future")
    ms.insert_sql('select 1')
    resList = ms.dict_sql("select top 2 * from st_report")
    # print resList
    for item in resList:
        print item['D']

if __name__ == '__main__':
    main()