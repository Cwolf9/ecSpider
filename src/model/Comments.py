# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: Comments
@date: 2021-04-20 21:38
@desc:
"""
from src import utilMysql
from src.conf_win import *


class Comments:
    def __init__(self, goodid, comment, ctime='2021-01-01 00:00:00'):
        self.goodid, self.comment, self.ctime = goodid, comment, ctime

    def getAttrs(self):
        return self.goodid, self.comment, self.ctime

    def showItem(self):
        return self.goodid, self.comment, self.ctime

    def __str__(self):
        return "goodid: %s, comment: %s, ctime: %s" % (self.goodid, self.comment, self.ctime)

    @classmethod
    def genComments(cls, tup: tuple):
        goodid, comment, ctime = tup[0], tup[1], tup[2]
        return Comments(goodid, comment, ctime)

    @classmethod
    def insert(cls, tup):
        sql = utilMysql.genInsSql('comments', (GOODID, COMMENT, CTIME), tup)
        return utilMysql.insert(sql)

    @classmethod
    def getComments(cls, goodid):
        f1 = (GOODID, )
        v1 = (goodid, )
        sql = utilMysql.genQuerySql('comments', f1, v1)
        return utilMysql.query(sql)


if __name__ == "__main__":
    comments = Comments('TB13612371112',  'good', '2021-01-01 00:00:00')
    print(comments)
    Comments.insert(comments.getAttrs())

