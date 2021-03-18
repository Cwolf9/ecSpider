# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: exercise
@date: 2021-01-23 12:49
@desc:
"""
from typing import List


class people:
    # 定义基本属性
    name = ''
    age = 0
    # 定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0

    # 定义构造方法
    def __init__(self, n, a, w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %d 岁。 %d." % (self.name, self.age, self.__weight))


# 实例化类
p = people('runoob', 10, 50)
p.speak()


import random
s = []
for i in range(4) :
    s.append((random.randint(0, 5), random.randint(0, 5), str(random.randint(0, 5))))
print(s)
print(sorted(s))


