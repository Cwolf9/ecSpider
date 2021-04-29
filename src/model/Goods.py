# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: Goods
@date: 2021-04-02 11:36
@desc:
"""
from src import utilMysql
from src.conf_win import *


class Goods:
    def __init__(self, goodid, platform, title, price, msales, shopname, href, picpath, tags=''):
        self.goodid, self.platform, self.title, self.price, self.msales, self.shopname, self.href, \
        self.picpath, self.tags = goodid, platform, title, price, msales, shopname, href, picpath, tags

    def getAttrs(self):
        return (self.goodid, self.platform, self.title, self.price, self.msales, self.shopname, self.href,
                self.picpath, self.tags)

    def showItem(self):
        return (self.goodid, self.platform, self.title, self.price, self.msales, self.shopname, self.href)

    def __str__(self):
        return "goodid: %s, title: %s, price: %f" % (self.goodid, self.title, self.price)

    @classmethod
    def genGoods(cls, tup: tuple):
        if tup[4] == '不显示':
            tup = list(tup)
            tup[4] = 0
            tup = tuple(tup)
        goodid, platform, title, price, msales, shopname, href, picpath, tags = \
            tup[0], tup[1], tup[2], float(tup[3]), int(tup[4]), tup[5], tup[6], tup[7], tup[8]
        return Goods(goodid, platform, title, price, msales, shopname, href, picpath, tags)

    @classmethod
    def queryWithGoodid(cls, goodid):
        sql = utilMysql.genQuerySql('goods', (GOODID,), (goodid,))
        return Goods.genGoods(utilMysql.query(sql)[0])


if __name__ == "__main__":
    good = Goods('TB617738137391', '淘宝', '【限时低至1899元起】HONOR/荣耀X10手机5G麒麟820全面屏官方旗舰店新品正品10X拍照手机', 2399.00, 9500, '荣耀官方旗舰店', '//detail.tmall.com/item.htm?id=617738137391', '', '')
    good = Goods('TB615651833644', '淘宝', '【分期免息/顺丰速发】HONOR/荣耀Play4T 4G手机6.39英寸指纹解锁4000mAh荣耀官方旗舰店正品官网游戏智能机', 1399.00, 32, '创汇通达数码旗舰店', '//detail.tmall.com/item.htm?id=615651833644', '', '')
    print(good)
    sql = utilMysql.genInsSql('goods', (GOODID, PLATFORM, TITLE, PRICE, MSALES, SHOPNAME, HREF, PICPATH, TAGS), good.getAttrs())
    print(sql)
    utilMysql.insert(sql)