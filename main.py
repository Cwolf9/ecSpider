# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

'''
https://www.runoob.com/python3/python3-add-number.html
https://www.bilibili.com/video/BV1mi4y1s7s2#reply3079374962
https://blog.csdn.net/smxjant/article/details/93614544
https://www.cnblogs.com/Tommy-Yu/p/3988893.html
'''

import sys
print(sys.path[0])
x = sys.path[0] + '\\leetcode'
print(x)
sys.path.append(x)
import exercise
'''
要导入上级目录，可以借助 sys.path，把上级目录加到 sys.path 里。
sys.path 作用：当使用import语句导入模块时，解释器会搜索当前模块所在目录以及sys.path指定的路径去找
需要import的模块。
'''