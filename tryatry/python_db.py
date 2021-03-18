# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: python_db
@date: 2021-02-09 16:01
@desc:

"""
# 导入pymysql模块
import pymysql

# 连接database
conn = pymysql.connect(host='localhost', port=3306, user ='root', password = 'ua123', database = 'uslib', charset = 'utf8')
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
# 得到一个可以执行SQL语句并且将结果作为字典返回的游标
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# SQL语句
sql = "SELECT * FROM users WHERE id > %d" % (1) + " and name like 'cwo%'"

# sql = 'update users set sex = "女" where id = 3'

try:
    x = cursor.execute(sql)
    res = cursor.fetchall()
    print(res)
    print("cursor, x: ", cursor, x)
    # 提交修改 (事务机制)
    conn.commit()
except:
   print ("Error: unable to?")
   conn.rollback()


# 关闭光标对象
cursor.close()

# 关闭数据库连接
conn.close()

try:
     s = None
     if s is None:
         print("s 是空对象")
         raise NameError('参数1', '参数2')     #如果引发NameError异常，后面的代码将不能执行
     print(len(s))  #这句不会执行，但是后面的except还是会走到
except TypeError:
     print("TypeError 空对象没有长度")
except NameError as e:
    print("NameError", e)
finally:
    print("this is final part!")

