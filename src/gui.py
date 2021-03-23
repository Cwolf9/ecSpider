# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: gui
@date: 2021-03-17 21:58
@desc:
"""
'''
im = Image.open(path)
im.show()
'''
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import font
from tkinter import scrolledtext
import fileinput
import os
import pickle

import LoginFrm


class ecSpider(Tk):
    def __init__(self):
        super().__init__()
        self.rt = self
        self.rt.title("基于爬虫的电商比价系统")
        self.changeSrcSize(800)
        self.login_Frm = LoginFrm.LoginFrm(self.rt)
        self.login_Frm.grid(row=0, column=0)

    def changeSrcSize(self, width=1200, height=800):
        screenwidth = self.rt.winfo_screenwidth()
        screenheight = self.rt.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.rt.geometry(size)

    def show_main_window(self):
        print('hello, main window')
        try:
            with open('data\\info.pickle', 'rb') as f:
                self.usr_info = pickle.load(f)
                print(self.usr_info)
        except FileNotFoundError:
            messagebox.showerror(title='错误提示！', message='系统出错，请重新登录！')
        self.rt.title("基于爬虫的电商比价系统^.^   欢迎 " + self.usr_info['login_username'])
if __name__ == "__main__":
    ecs = ecSpider()
    root = ecs.rt
    root.mainloop()
