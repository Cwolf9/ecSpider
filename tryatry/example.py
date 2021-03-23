# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: example.py
@date: 2021-02-14 16:55
@desc:
"""
import _thread
import time

# 为线程定义一个函数
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# 创建两个线程
try:
   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print ("Error: 无法启动线程")

while 1:
   pass


def reverseWords(input):
   # 通过空格将字符串分隔符，把各个单词分隔为列表
   inputWords = input.split(" ")

   # 翻转字符串
   # 假设列表 list = [1,2,3,4],
   # list[0]=1, list[1]=2 ，而 -1 表示最后一个元素 list[-1]=4 ( 与 list[3]=4 一样)
   # inputWords[-1::-1] 有三个参数
   # 第一个参数 -1 表示最后一个元素
   # 第二个参数为空，表示移动到列表末尾
   # 第三个参数为步长，-1 表示逆向
   inputWords = inputWords[-1::-1]

   # 重新组合字符串
   output = ' '.join(inputWords)

   return output


sites = {'Google', 'Taobao', 'Runoob', 'Facebook', 'Zhihu', 'Baidu', 2, 10.1}

print(sites)  # 输出集合，重复的元素被自动去掉

# 成员测试
if 10.1 in sites:
   print('Runoob 在集合中')
else:
   print('Runoob 不在集合中')

dict = {}
dict['one'] = "1 - 菜鸟教程"
dict[2] = "2 - 菜鸟工具"

tinydict = {'name': 'runoob', 'code': 1, 'site': 'www.runoob.com'}

print(dict['one'])  # 输出键为 'one' 的值
print(dict[2])  # 输出键为 2 的值
print(tinydict)  # 输出完整的字典
print(tinydict.keys())  # 输出所有键
print(tinydict.values())  # 输出所有值

str = "runoob"
print(str[5:-5:-1])

print("55".join("list"))