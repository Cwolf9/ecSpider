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
    def genWatchlist(cls, tup: tuple):
        userid, pt, cookie, referer = tup[0], tup[1], tup[2], tup[3]
        return Searchinfo(userid, pt, cookie, referer)

if __name__ == "__main__":
    searchinfo = Searchinfo(1, 'TB615651833644', '淘宝', 12, 11, 13, '//detail.tmall.com/item.htm?id=615651833644', 'O1CN01qXLQ231sW59J818ds_!!0-item_pic.png')
    print(searchinfo)
    sql = utilMysql.genInsSql('watchlist', (USERID, PT, COOKIE, REFERER), searchinfo.getAttrs())
    print(sql)
    utilMysql.insert(sql)