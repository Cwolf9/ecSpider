# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: Records
@date: 2021-04-03 14:27
@desc:
"""
from src import utilMysql
from src.conf_win import *
class Records:
    def __init__(self, userid, searchterm, wordcloud='', wcpath='', tags=''):
        self.userid, self.searchterm, self.wordcloud, self.wcpath, self.tags = userid, searchterm, wordcloud, wcpath, tags

    def getAttrs(self):
        return (self.userid, self.searchterm, self.wordcloud, self.wcpath, self.tags)

    def showItem(self):
        return (self.userid, self.searchterm, self.wordcloud, self.wcpath, self.tags)

    def __str__(self):
        return "userid: %s, searchterm: %s, wordcloud: %s" % (self.userid, self.searchterm, self.wordcloud)

    @classmethod
    def genRecords(cls, tup: tuple):
        userid, searchterm, wordcloud, wcpath, tags = \
            tup[0], tup[1], tup[2], tup[3], tup[4]
        return Records(userid, searchterm, wordcloud, wcpath, tags)

    @classmethod
    def getRecords(cls, userid):
        f1 = (USERID, )
        v1 = (userid, )
        sql = utilMysql.genQuerySql('records', f1, v1)
        return utilMysql.query(sql)


if __name__ == "__main__":
    record = Records(1, '手机', '', '', '')
    print(record)
    sql = utilMysql.genInsSql('records', (USERID, SEARCHTERM, WORDCLOUD, WCPATH, TAGS), record.getAttrs())
    print(sql)
    utilMysql.insert(sql)