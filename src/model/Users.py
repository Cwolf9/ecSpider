# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: Users
@date: 2021-03-18 21:54
@desc:
"""
import re
class Users:
    def __init__(self, userid, username, password, email='xxx@qq.com', phonenumber='12345678901', nickname='李某', sex='X'):
        self.userid = userid
        self.username = username
        self.password = password
        self.email = email
        self.phonenumber = phonenumber
        self.nickname = nickname
        self.sex = sex

    def getAttrs(self):
        return (self.username, self.password, self.email, self.phonenumber, self.nickname, self.sex)

    def __str__(self):
        return "userid: %s, username: %s, password: %s" % (self.userid, self.username, self.password)

    def self_check(self):
        invalid_symbols = ['\\', '/', ',', '<', '>', '?', ':', ';', '\'', '\"', '[', ']', '{', '}', '|', ' ', '\n',
                           '\r']
        for c in self.username + self.password + self.nickname:
            if c in invalid_symbols:
                return -1
        if min(len(self.username), len(self.password)) < 5:
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
        userid = tup[0]
        username = tup[1]
        password = tup[2]
        email = tup[3]
        phonenumber = tup[4]
        nickname = tup[5]
        sex = tup[6]
        return Users(userid, username, password, email, phonenumber, nickname, sex)
# user = Users(0, 'zs', 'zs')
# print(user)