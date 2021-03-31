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
import tkinter as tk
from tkinter import Tk, Frame, Button, Label, LabelFrame, Text, PhotoImage, Entry, messagebox\
    , font, StringVar, IntVar, Checkbutton, Menu
from tkinter import filedialog, simpledialog, scrolledtext
from tkinter import W, E, N, S, END, BOTTOM, TOP, BOTH, X, Y
import fileinput
import os
import pickle
import loginFrame

from src.model import Users


class ecSpider(Tk):
    def __init__(self):
        super().__init__()
        self.rt = self
        self.rt.title("基于爬虫的电商比价系统")
        self.change_src_size(800)
        self.login_frame = loginFrame.LoginFrame(self.rt)
        self.login_frame.pack()
        self.pf_all, self.pf_tb, self.pf_jd, self.tmcs, self.wph = IntVar(value=0), IntVar(value=1), IntVar(value=1), IntVar(value=0), IntVar(value=0)
        self.main_frame = Frame(self.rt, width=1200, height=800)
        self.create_main_page()

    def change_src_size(self, width=1200, height=800):
        screenwidth = self.rt.winfo_screenwidth()
        screenheight = self.rt.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.rt.geometry(size)

    def goto_login(self):
        self.rt.config(menu=Menu())
        self.main_frame.pack_forget()
        self.change_src_size(800)
        self.login_frame.pack()

    def show_main_window(self):
        print('hello, main window')
        self.rt.config(menu=self.menubar)
        try:
            with open('data\\info.pickle', 'rb') as f:
                self.usr_info = pickle.load(f)
                print(self.usr_info)
            self.rt.title("基于爬虫的电商比价系统^.^   欢迎 " + self.usr_info['login_username'])
            self.login_frame.pack_forget()
            self.change_src_size()
            self.main_frame.pack(fill=BOTH)
        except FileNotFoundError:
            messagebox.showerror(title='错误提示！', message='系统出错，请重新登录！')
            self.goto_login()

    def update_platform_info(self, pf_id):
        print(pf_id)

    def show_profile(self):
        pass

    def create_main_page(self):
        self.menu_font = font.Font(family='微软雅黑', size=16)
        self.menubar = Menu(self.rt, tearoff=0)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='更新电商信息', menu=self.filemenu)
        self.filemenu.add_command(label='淘宝', command=lambda: self.update_platform_info(1))
        self.filemenu.add_command(label='京东', command=lambda: self.update_platform_info(2))
        self.filemenu.add_command(label='天猫超市', command=lambda: self.update_platform_info(3))
        self.filemenu.add_command(label='唯品会', command=lambda: self.update_platform_info(4))

        self.menubar.add_command(label='个人中心', command=self.show_profile)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='帮助')
        self.helpmenu.add_command(label='操作说明', command=self.description)
        self.helpmenu.add_command(label='关于',  command=self.software_about)

        self.search_frame = Frame(self.main_frame, width=1200, height=300, bg='blue')
        self.search_frame.pack(side='top', fill=BOTH, expand='yes')

        Label(self.search_frame, text='搜索关键词：', width=20, bg='red').grid(row=0, column=0, sticky=W, padx=50, pady=10)
        Entry(self.search_frame, width=100).grid(row=0, column=1, sticky=W, padx=50, pady=10, ipady=5)
        Button(self.search_frame, text='search', command=self.goto_login).grid(row=0, column=2, sticky=E, padx=15)
        Button(self.search_frame, text='hello', command=self.goto_login).grid(row=10, column=1)

    def description(self):
        pass
    def software_about(self):
        pass


if __name__ == "__main__":
    ecs = ecSpider()
    root = ecs.rt
    root.mainloop()
