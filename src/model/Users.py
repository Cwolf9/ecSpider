# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: Users
@date: 2021-03-18 21:54
@desc:
"""

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