# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: conf_win
@date: 2021-03-19 11:11
@desc:
"""
import hashlib
import codecs
# the configuration file of windows(develop) environment

# path configure
DATA_ROOT_PATH = 'D:\\document\\PyCharmProject\\ecSpider\\src\\data\\'

# mysql configure
DB_USER = "ecspider"
DB_PWD = "ecspider"
DB_SERVER = "localhost"
DB_PORT = "3306"
DB_NAME = "ecspider"


USERID, USERNAME, PASSWORD, EMAIL, PHONENUMBER, NICKNAME, SEX = 'userid', 'username', 'password', 'email', 'phonenumber', 'nickname', 'sex'

GOODID, PLATFORM, TITLE, PRICE, MSALES, SHOPNAME, HREF, PICPATH, TAGS = 'goodid', 'platform', 'title', 'price', 'msales', 'shopname', 'href', 'picpath', 'tags'

USERID, SEARCHTERM, WORDCLOUD, WCPATH, TAGS = 'userid', 'searchterm', 'wordcloud', 'wcpath', 'tags'

NOWPRICE, LOWPRICE, HIGHPRICE, HREF, PICPATH = 'nowprice', 'lowprice', 'highprice', 'href', 'picpath'

USERID, PT, COOKIE, REFERER, STATE = 'userid', 'pt', 'cookie', 'referer', 'state'

GOODID, COMMENT, CTIME = 'goodid', 'comment', 'ctime'


def getMD5(s) :
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()


def utf_8ToStr(bs):
    """
    手机gb2312编码 %CA%D6%BB%FA
    笔记本utf-8编码 \xE7\xAC\x94\xE8\xAE\xB0\xE6\x9C\xAC
    将utf-8内容的字符串格式还原decode成utf-8编码的字符串
    :param bs:
    :return:
    """
    # s = "%E7%AC%94%E8%AE%B0%E6%9C%AC" #笔记本
    # s = s.replace('%', '\\x')
    # '\xE7\xAC\x94\xE8\xAE\xB0\xE6\x9C\xAC'
    # ss = codecs.escape_decode(s, 'hex-escape')[0]
    # print(ss.decode('utf-8'))
    bs = bs.replace('%', '\\x')
    bss = codecs.escape_decode(bs, 'hex-escape')[0]
    bss = bss.decode('utf-8')
    return bss


def strToBytes(bs, code='utf-8'):
    """
    将字符串变成其utf-8/gb2312编码内容,并把\\x转换成%
    :param bs:
    :return:
    """
    bs = str(bs.encode(code))[2:-1]
    bss = bs.replace('\\x', '%').upper()
    return bss


def changeStrSize(s, width, wordSize=12):
    num = int(width/wordSize)
    nstr = ''
    for i in range(int(len(s) / num)):
        nstr += s[i * num: (i + 1) * num] + '\n'
    nstr += s[int(len(s) / num) * num:]
    return nstr


if __name__ == "__main__":
    print("conf_win")
    print(strToBytes('酒疯狼'))