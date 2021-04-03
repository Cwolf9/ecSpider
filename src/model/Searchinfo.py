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
    def __init__(self, userid, pt, cookie, referer=''):
        self.userid, self.pt, self.cookie, self.referer = userid, pt, cookie, referer

    def getAttrs(self):
        return (self.userid, self.pt, self.cookie, self.referer)

    def showItem(self):
        return (self.userid, self.pt, self.cookie, self.referer)

    def __str__(self):
        return "userid: %s, pt: %s, cookie: %s" % (self.userid, self.pt, self.cookie)

    @classmethod
    def genSearchinfo(cls, tup: tuple):
        userid, pt, cookie, referer = tup[0], tup[1], tup[2], tup[3]
        return Searchinfo(userid, pt, cookie, referer)

if __name__ == "__main__":
    searchinfo = Searchinfo(1,  '淘宝',  '44', 'Og')
    print(searchinfo)
    sql = utilMysql.genInsSql('searchinfo', (USERID, PT, COOKIE, REFERER), searchinfo.getAttrs())
    print(sql)
    utilMysql.insert(sql)