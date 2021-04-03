# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: conf_win
@date: 2021-03-19 11:11
@desc:
"""
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

USERID, PT, COOKIE, REFERER = 'userid', 'pt', 'cookie', 'referer'

if __name__ == "__main__":
    print("conf_win")