# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: Searchinfo
@date: 2021-04-03 15:25
@desc:
"""
from src import utilMysql
from src.conf_win import *


class Searchinfo:
    def __init__(self, userid, pt, cookie, referer='', state=0):
        self.userid, self.pt, self.cookie, self.referer, self.state = userid, pt, cookie, referer, state

    def getAttrs(self):
        return self.userid, self.pt, self.cookie, self.referer, self.state

    def showItem(self):
        return self.userid, self.pt, self.cookie, self.referer, self.state

    def __str__(self):
        return "userid: %s, pt: %s, cookie: %s, state: %d" % (self.userid, self.pt, self.cookie, self.state)

    @classmethod
    def genSearchinfo(cls, tup: tuple):
        userid, pt, cookie, referer, state = int(tup[0]), tup[1], tup[2], tup[3], tup[4]
        return Searchinfo(userid, pt, cookie, referer, state)

    @classmethod
    def insert(cls, tup):
        sql = utilMysql.genInsSql('searchinfo', (USERID, PT, COOKIE, REFERER, STATE), tup)
        return utilMysql.insert(sql)

    @classmethod
    def getSearchInfo(cls, userid, pt):
        f1 = (USERID, PT)
        v1 = (userid, pt)
        sql = utilMysql.genQuerySql('searchinfo', f1, v1)
        return utilMysql.query(sql)

if __name__ == "__main__":
    searchinfo = Searchinfo(1,  '淘宝',  '44', 'Og', 0)
    print(searchinfo)
    Searchinfo.insert(searchinfo.getAttrs())
