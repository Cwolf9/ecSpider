# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: 225
@date: 2021-01-24 13:13
@desc:
"""
from typing import List
import heapq

import tkinter as tk
import time
import threading

songs = ['爱情买卖', '朋友', '回家过年', '好日子']
films = ['阿凡达', '猩球崛起']


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.createUI()

        # 生成界面


    def createUI(self):
        self.text = tk.Text(self)
        self.text.pack()

        tk.Button(self, text='音乐', command=lambda: self.thread_it(self.music, songs)).pack(expand=True,
                                                                                           side=tk.RIGHT)  # 注意lambda语句的作用！
        tk.Button(self, text='电影', command=lambda: self.thread_it(self.movie, films)).pack(expand=True, side=tk.LEFT)

        # 逻辑：听音乐


    def music(self, songs):
        for x in songs:
            self.text.insert(tk.END, "听歌曲：%s \t-- %s\n" % (x, time.ctime()))
            print("听歌曲：%s \t-- %s" % (x, time.ctime()))
            time.sleep(2)

        # 逻辑：看电影


    def movie(self, films):
        for x in films:
            self.text.insert(tk.END, "看电影：%s \t-- %s\n" % (x, time.ctime()))
            print("看电影：%s \t-- %s" % (x, time.ctime()))
            time.sleep(3)

        # 打包进线程（耗时的操作）


    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)  # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        t.start()  # 启动
        t.join()          # 阻塞--会卡死界面！


app = Application()
app.mainloop()