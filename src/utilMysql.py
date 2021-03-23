# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: utilsDB
@date: 2021-03-17 21:59
@desc:
"""
import platform
import conf_win
import pymysql
import threading
from src.model import Users
from typing import List
import time


# 跨环境配置
platform_os = platform.system()
config = conf_win


# 连接配置信息
mysql_config = {
    'host': config.DB_SERVER,
    'port': int(config.DB_PORT),
    'user': config.DB_USER,
    'password': config.DB_PWD,
    'db': config.DB_NAME,
    'charset': 'utf8',
    # 执行完毕返回的结果集默认以元组显示
    # 得到一个可以执行SQL语句并且将结果作为字典返回的游标
    # 'cursorclass': pymysql.cursors.DictCursor,
}

class MySQLConnection(object):
    """单例模式，数据库链接句柄
    Attributes:
            _instance_lock: 创建实例时的锁
            _instance: 类的唯一实例
            conn: 数据库连接对象
            cursor: 可以执行SQL语句的游标对象
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        super().__init__()
        # print('init mysql connection!')

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with MySQLConnection._instance_lock:
                if not hasattr(cls, '_instance'):
                    MySQLConnection._instance = super().__new__(cls)
                    try:
                        # 连接MySQL数据库
                        MySQLConnection._instance.conn = pymysql.connect(**mysql_config)
                        # 得到一个可以执行SQL语句的光标对象
                        MySQLConnection._instance.cursor = MySQLConnection._instance.conn.cursor()
                        print('create mysql connection!')
                    except pymysql.Error as e:
                        raise ConnectionError(e)
        return MySQLConnection._instance
    def getConn(self):
        return self.conn
    def getCursor(self):
        return self.cursor
    def __del__(self):
        # 关闭光标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()
        # print("destory mysql connection!")


def get_now_time():
    """获取现在的时间，字符串格式：%Y-%m-%d %H:%M:%S
    例如：2021-03-19 21:57:53
    :return:
        一个字符串表示时间
    """
    return time.strftime('%Y-%m-%d %H:%M:%S')
def genPH(num):
    """创建若干个placeholders
    :param num: 占位符个数
    :return: 字符串
    """
    if num <= 1:
        return "(" + "%s" * num + ")"
    else:
        return "(" + "%s" + ", %s" * (num - 1) + ")"
def tuple_str(tup, ip = 0):
    """将tuple变成字符串
    用于生成insert sql语句时，fields和values部分
    :param tup: 元组
    :param ip:
        是否在字符串左右加单引号，ip=0表示不加单引号
    :return: 字符串
    """
    cnt = 0
    string = '('
    for x in tup:
        if cnt != 0:
            string += ', '
        if ip == 0:
            string += repr(x)[1:-1]
        else:
            string += "'" + repr(x)[1:-1] + "'"
        cnt += 1
    string += ')'
    return string

def tuple_str2(tup, val):
    """
    将tuple变成字符串
    用于生成delete, select, update sql语句时，field = value部分
    :param tup: 元组
    :param val: 元组
    :return: 字符串
    """
    cnt = 0
    string = ""
    for x in tup:
        if cnt != 0:
            string += ' and '
        if '%' not in val[cnt]:
            string += repr(x)[1:-1] + ' = ' + "'" + repr(val[cnt])[1:-1] + "'"
        else:
            string += repr(x)[1:-1] + ' like ' + "'" + repr(val[cnt])[1:-1] + "'"
        cnt += 1
    return string

def genInsSql(table_name, fields, values):
    return "insert into " + table_name + ' ' + tuple_str(fields) + \
    ' values ' + tuple_str(values, 1)
def insertUsers(sql: str):
    """插入数据到users表，提供sql语句
    :param sql: sql语句
    :return: bool，是否插入成功
    """
    result = True
    mysql_conn = MySQLConnection()
    conn = None
    try:
        conn = mysql_conn.getConn()
        cursor = mysql_conn.getCursor()
        # 使用 execute()  方法执行 SQL 查询
        exe_res = cursor.execute(sql)
        # 使用 fetchall() 方法获取所有数据, 返回元组
        fet_res = cursor.fetchall()
        # 提交修改 (事务机制)
        conn.commit()
    except AttributeError as e:
        result = False
        print('AttributeError: ', e)
        # 发生错误时回滚
        conn.rollback()
    except Exception as e:
        result = False
        print(e)
        # print(e.args)
        # print(str(e))
        print(repr(e))
        conn.rollback()
    return result
def testInsertSql():
    """测试使用占位符能否防止因字段值不规范导致的sql注入
    :return:
    """
    fields = ('username', 'password')
    sql = "insert into " + 'users' + ' ' + tuple_str(fields) + \
    ' values ' + genPH(2)
    print(sql)
    username = '\t1223'
    password = '\t123'
    mysql_conn = MySQLConnection()
    conn = None
    try:
        conn = mysql_conn.getConn()
        cursor = mysql_conn.getCursor()
        # 使用 execute()  方法执行 SQL 查询
        exe_res = cursor.execute(sql, (username, password))
        # 使用 fetchall() 方法获取所有数据, 返回元组
        fet_res = cursor.fetchall()
        # 提交修改 (事务机制)
        conn.commit()
    except AttributeError as e:
        print('AttributeError: ', e)
        # 发生错误时回滚
        conn.rollback()
    except Exception as e:
        print(e)
        # print(e.args)
        # print(str(e))
        print(repr(e))
        conn.rollback()


def genDelSql(table_name, fields, values):
    return "delete from " + table_name + ' where ' + tuple_str2(fields, values)
def deleteUsers(sql):
    result = True
    mysql_conn = MySQLConnection()
    conn = None
    try:
        conn = mysql_conn.getConn()
        cursor = mysql_conn.getCursor()
        exe_res = cursor.execute(sql)
        fet_res = cursor.fetchall()
        # 提交修改 (事务机制)
        conn.commit()
    except AttributeError as e:
        result = False
        print('AttributeError: ', e)
        conn.rollback()
    except Exception as e:
        result = False
        print(repr(e))
        conn.rollback()
    return result

def genQuerySql(table_name, fields, values):
    return "select * from " + table_name + ' where ' + tuple_str2(fields, values)
def queryUsers(sql) -> List[tuple]:
    userlist = []
    mysql_conn = MySQLConnection()
    try:
        cursor = mysql_conn.getCursor()
        exe_res = cursor.execute(sql)
        fet_res = cursor.fetchall()
        userlist = list(items for items in fet_res)
    except AttributeError as e:
        print('AttributeError: ', e)
    except Exception as e:
       print(repr(e))
    return userlist

def genUpdSql(table_name, fields, values, fields2, values2):
    return "update " + table_name + \
           ' set ' + tuple_str2(fields, values) + \
           ' where ' + tuple_str2(fields2, values2)
def updateUser(sql) -> bool:
    result = True
    mysql_conn = MySQLConnection()
    conn = None
    try:
        conn = mysql_conn.getConn()
        print('*', conn.autocommit_mode, conn.get_autocommit())
        cursor = mysql_conn.getCursor()
        exe_res = cursor.execute(sql)
        fet_res = cursor.fetchall()
        # 提交修改 (事务机制)
        conn.commit()
    except AttributeError as e:
        print('AttributeError: ', e)
        conn.rollback()
    except Exception as e:
        print(repr(e))
        conn.rollback()
    return result


# 测试功能
if __name__ == '__main__':
    # 删除用户
    sql = genDelSql('users', ('username', 'password'), ('wemz2', 'wemz2'))
    res = deleteUsers(sql)
    print('delete: ', res)

    # 新增用户
    user = Users.Users(0, 'wemz2', 'wemz2')
    sql = genInsSql('users', ('username', 'password', 'email', 'phonenumber', 'nickname', 'sex'), user.getAttrs())
    print(sql)
    insertUsers(sql)

    # 查询用户
    sql = genQuerySql('users', ('username', 'password'), ('wemz', 'wemz'))
    print(sql)
    res = queryUsers(sql)
    print('query: ', res)
    new_user = Users.Users.genUsers(res[0])
    print("new_users: ", new_user)

    # 更新用户信息
    upd_sql = genUpdSql('users', ('password',), ('zs4',), ('username', 'password'), ('zs', 'zs3'))
    print(upd_sql)
    upd_res = updateUser(upd_sql)
    print('upd_res: ', upd_res)

    print(get_now_time())

    a = ('123', 'abc', r'z12%')
    print(a.__str__(), tuple_str(a))
    print(tuple_str2(a, a))

    print(genInsSql('users', ('username', 'password'), ('\b123', '\t234')))
    print(genDelSql('users', ('username', 'password'), ('\b123%', '\t234')))
    print(genQuerySql('users', ('username', 'password'), ('\b123%', '\t234')))
    print(genUpdSql('users', ('password',), ('\tzs4',), ('username', 'password'), ('\azs', 'zs3')))
