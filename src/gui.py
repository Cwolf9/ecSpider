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
from tkinter import Tk, Frame, Button, Label, LabelFrame, Text, StringVar, PhotoImage, Entry, messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import font
from tkinter import scrolledtext
import fileinput
import os
import pickle
import loginFrame


class ecSpider(Tk):
    def __init__(self):
        super().__init__()
        self.rt = self
        self.rt.title("基于爬虫的电商比价系统")
        self.change_src_size(800)
        self.login_frame = loginFrame.LoginFrame(self.rt)
        self.login_frame.pack()
        self.main_frame = Frame(self.rt)
        self.create_main_page()

    def change_src_size(self, width=1200, height=800):
        screenwidth = self.rt.winfo_screenwidth()
        screenheight = self.rt.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.rt.geometry(size)

    def goto_login(self):
        self.main_frame.pack_forget()
        self.change_src_size(800)
        self.login_frame.pack()

    def show_main_window(self):
        print('hello, main window')
        try:
            with open('data\\info.pickle', 'rb') as f:
                self.usr_info = pickle.load(f)
                print(self.usr_info)
            self.rt.title("基于爬虫的电商比价系统^.^   欢迎 " + self.usr_info['login_username'])
            self.login_frame.pack_forget()
            self.change_src_size()
            self.main_frame.pack()
        except FileNotFoundError:
            messagebox.showerror(title='错误提示！', message='系统出错，请重新登录！')
            self.goto_login()

    def create_main_page(self):
        Label(self.main_frame, text='123', width=20).pack()
        Button(self.main_frame, text='hello', command=self.goto_login).pack()


if __name__ == "__main__":
    ecs = ecSpider()
    root = ecs.rt
    root.mainloop()
