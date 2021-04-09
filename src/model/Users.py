# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: Users
@date: 2021-03-18 21:54
@desc:
"""
import re
from src import utilMysql
from src.conf_win import *


class Users:
    def __init__(self, userid, username, password, email='xxx@qq.com', phonenumber='12345678901', nickname='李某', sex='X'):
        self.userid, self.username, self.password, self.email, self.phonenumber, self.nickname, self.sex = \
            userid, username, password, email, phonenumber, nickname, sex

    def getAttrs(self):
        return (self.username, self.password, self.email, self.phonenumber, self.nickname, self.sex)

    def __str__(self):
        return "userid: %s, username: %s, password: %s, %s, %s, %s, %s" % (self.userid, self.username, self.password, self.email, self.phonenumber, self.nickname, self.sex)

    def self_check(self):
        invalid_symbols = ['\\', '/', ',', '<', '>', '?', ':', ';', '\'', '\"', '[', ']', '{', '}', '|', ' ', '\n',
                           '\r']
        for c in self.username + self.password + self.nickname:
            if c in invalid_symbols:
                return -1
        if min(len(self.username)+4, len(self.password)) < 5:
            return -2
        reg = r'^([\w]{1,19}@[0-9a-zA-Z]{2,10}.(com)|(cn)|(net))$'
        reg2 = r'^([\d]{11})$'
        result = re.search(reg, self.email, re.IGNORECASE)
        result2 = re.search(reg2, self.phonenumber)
        print(self.email, " ", self.phonenumber)
        print(result, " ", result2)
        if not result or not result2:
            return -3
        return 0

    @classmethod
    def genUsers(cls, tup: tuple):
        userid, username, password, email, phonenumber, nickname, sex = tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]
        return Users(userid, username, password, email, phonenumber, nickname, sex)

    @classmethod
    def queryWithUserid(cls, userid):
        sql = utilMysql.genQuerySql('users', (USERID,), (userid,))
        return Users.genUsers(utilMysql.query(sql)[0])

    @classmethod
    def updateUsers1(cls, f1, v1, f2, v2):
        sql = utilMysql.genUpdSql('users', f1, v1, f2, v2)
        return utilMysql.update(sql)

if __name__ == "__main__":
    user = Users(0, 'zs', 'zs')
    print(user)