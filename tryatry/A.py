# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: A.py
@date: 2020-12-12 16:17
@desc:
"""


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


if __name__ == "__main__":
    input1 = 'I like runoob'
    print(input1)
    rw = reverseWords(input1)
    print(rw)



    # 用户输入数字
    num1 = 1
    num2 = 2

    # 求和
    sum = float(num1) + float(num2)

    # 显示计算结果
    print('数字 {0} 和 {1} 相加结果为： {2}'.format(num1, num2, sum))

sites = {'Google', 'Taobao', 'Runoob', 'Facebook', 'Zhihu', 'Baidu', 2, 10.1}

print(sites)   # 输出集合，重复的元素被自动去掉

# 成员测试
if 10.1 in sites :
    print('Runoob 在集合中')
else :
    print('Runoob 不在集合中')

dict = {}
dict['one'] = "1 - 菜鸟教程"
dict[2]     = "2 - 菜鸟工具"

tinydict = {'name': 'runoob','code':1, 'site': 'www.runoob.com'}


print (dict['one'])       # 输出键为 'one' 的值
print (dict[2])           # 输出键为 2 的值
print (tinydict)          # 输出完整的字典
print (tinydict.keys())   # 输出所有键
print (tinydict.values()) # 输出所有值

str = "runoob"
print(str[5:-5:-1])




print("55".join("list"))