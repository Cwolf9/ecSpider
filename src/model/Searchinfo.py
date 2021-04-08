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
        return (self.userid, self.pt, self.cookie, self.referer, self.state)

    def showItem(self):
        return (self.userid, self.pt, self.cookie, self.referer, self.state)

    def __str__(self):
        return "userid: %s, pt: %s, cookie: %s, state: %d" % (self.userid, self.pt, self.cookie, self.state)

    @classmethod
    def genSearchinfo(cls, tup: tuple):
        userid, pt, cookie, referer, state = tup[0], tup[1], tup[2], tup[3], tup[4]
        return Searchinfo(userid, pt, cookie, referer, state)

if __name__ == "__main__":
    searchinfo = Searchinfo(1,  '淘宝',  '44', 'Og', 0)
    print(searchinfo)
    sql = utilMysql.genInsSql('searchinfo', (USERID, PT, COOKIE, REFERER, STATE), searchinfo.getAttrs())
    print(sql)
    utilMysql.insert(sql)