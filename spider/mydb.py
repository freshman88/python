"""
"""

import sqlite3

dbname='test.db'

class SiteService:

    def __init__(self,reload=True):
        if reload == True:
            self._drop_table()
            self._create_table()

    def _drop_table(self):
        with MyConn(dbname) as myconn:
            myconn.execute('DROP TABLE  IF EXISTS mysite')
            myconn.commit()

    def _create_table(self):
        with MyConn(dbname) as myconn:
            myconn.execute('CREATE TABLE mysite (url text, content text)')
            myconn.commit()

    def put(self,url,content):
        with MyConn(dbname) as myconn:
            myconn.execute('INSERT INTO mysite VALUES(?,?)',(url,content))
            myconn.commit()

    def find_all_url(self):
        result=list()
        with MyConn(dbname) as myconn:
            for row in myconn.execute('SELECT url FROM mysite'):
                result.append(row)
        return result

    def find_content(self,url):
        with MyConn(dbname) as myconn:
            myconn.execute('SELECT content FROM mysite where url=?',(url,))
            result=myconn.fetchone()
        return result


class InnerUrlService:

    def __init__(self,reload=True):
        if reload == True:
            self._drop_table()
            self._create_table()

    def _drop_table(self):
        with MyConn(dbname) as myconn:
            myconn.execute('DROP TABLE  IF EXISTS myinnerurl')
            myconn.commit()

    def _create_table(self):
        with MyConn(dbname) as myconn:
            myconn.execute('CREATE TABLE myinnerurl (url text, innerurl text)')
            myconn.commit()

    def put(self,url,innerurl):
        with MyConn(dbname) as myconn:
            myconn.execute('INSERT INTO myinnerurl VALUES(?,?)',(url,innerurl))
            myconn.commit()

    def find_all(self):
        result=list()
        with MyConn(dbname) as myconn:
            for row in myconn.execute('SELECT * FROM myinnerurl'):
                result.append(row)
        return result


class OuterUrlService:

    def __init__(self,reload=True):
        if reload == True:
            self._drop_table()
            self._create_table()
    def _drop_table(self):
        with MyConn(dbname) as myconn:
            myconn.execute('DROP TABLE  IF EXISTS myouterurl')
            myconn.commit()

    def _create_table(self):
        with MyConn(dbname) as myconn:
            myconn.execute('CREATE TABLE myouterurl (url text, outerurl text)')
            myconn.commit()

    def put(self,url,outerurl):
        with MyConn(dbname) as myconn:
            myconn.execute('INSERT INTO myouterurl VALUES(?,?)',(url,outerurl))
            myconn.commit()

    def find_all(self):
        result=list()
        with MyConn(dbname) as myconn:
            for row in myconn.execute('SELECT * FROM myouterurl'):
                result.append(row)
        return result


class FetchFailedUrlService:

    def __init__(self,reload=True):
        if reload == True:
            self._drop_table()
            self._create_table()
    def _drop_table(self):
        with MyConn(dbname) as myconn:
            myconn.execute('DROP TABLE  IF EXISTS myfetch_failed_url')
            myconn.commit()

    def _create_table(self):
        with MyConn(dbname) as myconn:
            myconn.execute('CREATE TABLE myfetch_failed_url (url text, failed_url text)')
            myconn.commit()

    def put(self,url,failed_url):
        with MyConn(dbname) as myconn:
            myconn.execute('INSERT INTO myfetch_failed_url VALUES(?,?)',(url,failed_url))
            myconn.commit()

    def find_all(self):
        result=list()
        with MyConn(dbname) as myconn:
            for row in myconn.execute('SELECT * FROM myfetch_failed_url'):
                result.append(row)
        return result


class MyConn:

    def __init__(self,dbname):
        self.dbname=dbname

    def __enter__(self):
        self.connection=sqlite3.connect(self.dbname)
        self.cursor=self.connection.cursor()
        return self

    def __exit__(self,type,value,traceback):
        self.connection.close()

    def execute(self,*args,**kw):
        return self.cursor.execute(*args,**kw)

    def fetchone(self):
        return self.cursor.fetchone()

    def commit(self):
        return self.connection.commit()
