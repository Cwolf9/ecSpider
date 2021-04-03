# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: Watchlist
@date: 2021-04-03 15:05
@desc:
"""
from src import utilMysql
from src.conf_win import *
class Watchlist:
    def __init__(self, userid, goodid, platform, nowprice, lowprice, highprice, href='', picpath=''):
        self.userid, self.goodid, self.platform, self.nowprice, self.lowprice, self.highprice, self.href, self.picpath = userid, goodid, platform, nowprice, lowprice, highprice, href, picpath

    def getAttrs(self):
        return (self.userid, self.goodid, self.platform, self.nowprice, self.lowprice, self.highprice, self.href, self.picpath)

    def showItem(self):
        return (self.userid, self.goodid, self.platform, self.nowprice, self.lowprice, self.highprice, self.href)

    def __str__(self):
        return "userid: %s, goodid: %s, nowprice: %f" % (self.userid, self.goodid, self.nowprice)

    @classmethod
    def genWatchlist(cls, tup: tuple):
        userid, goodid, platform, nowprice, lowprice, highprice, href, picpath = \
            tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]
        return Watchlist(userid, goodid, platform, nowprice, lowprice, highprice, href, picpath)

if __name__ == "__main__":
    watchlist = Watchlist(1, 'TB615651833644', '淘宝', 12, 11, 13, '//detail.tmall.com/item.htm?id=615651833644', 'O1CN01qXLQ231sW59J818ds_!!0-item_pic.png')
    print(watchlist)
    sql = utilMysql.genInsSql('watchlist', (USERID, GOODID, PLATFORM, NOWPRICE, LOWPRICE, HIGHPRICE, HREF, PICPATH), watchlist.getAttrs())
    print(sql)
    utilMysql.insert(sql)