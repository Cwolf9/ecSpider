# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: LoginFrm
@date: 2021-03-22 21:27
@desc:
"""
import utilMysql
from conf_win import *
from tkinter import *
from tkinter import messagebox
import pickle

class LoginFrm(Frame):
    def __init__(self, master, **kw):
        self.kw = kw
        self.temp = dict()
        for key, value in self.kw.items():
            self.temp[key] = value
        Frame.__init__(self, master, self.temp)

        print(id(self.master), id(master))
        self.login_page = Frame(self)
        self.username = StringVar()
        self.password = StringVar()
        self.createpage()

    def createpage(self):
        self.login_photo = PhotoImage(file="data\\img_hds.gif")
        logo = Label(self.login_page, image=self.login_photo, text="^.^ 欢迎来到电商比价系统", compound=BOTTOM,
                     font=('微软雅黑', 25), fg='pink', height=400)  # compound位置关系
        logo.grid(row=0, column=0, columnspan=2, padx=130, pady=0)

        login_lf = LabelFrame(self.login_page, text="登录框", width=540, height=200)
        login_lf.x = 10
        # print(login_lf.x)

        Label(login_lf, text='用户名:', font=('微软雅黑', 12)).grid(row=1, stick=W, padx=90, pady=10)
        Entry(login_lf, textvariable=self.username, width=25, font=(12)).grid(row=1, column=1, stick=E, ipady=6)

        Label(login_lf, text='密码:', font=('微软雅黑', 12)).grid(row=2, stick=W, padx=90, pady=10)
        login_lf_ep = Entry(login_lf, textvariable=self.password, show='*', width=25, font=(12))
        login_lf_ep.focus_set()
        login_lf_ep.bind('<KeyRelease-Return>', self.login())
        login_lf_ep.grid(row=2, stick=E, column=1, ipady=6)

        Button(login_lf, text='注册', command=self.register, font=('微软雅黑', 12)).grid(row=3, stick=W, padx=90, pady=10)
        login_lf_bl = Button(login_lf, text='登录', command=self.login, font=('微软雅黑', 12))
        login_lf_bl.grid(row=3, stick=W + E, column=1)



        login_lf.grid(row=1, stick=W+E, padx=130)
        login_lf.grid_propagate(0)

        self.login_page.pack()

    def login(self, event=None):
        print(event, event.char)
        un = self.username.get()
        pw = self.password.get()
        print(un, pw)
        invalid_symbols = ['\\', '/', ',', '.', '<', '>', '?', ':', ';', '\'', '\"', '[', ']', '{', '}', '|', ' ', '\n', '\r']
        print(invalid_symbols)
        errorno = 0
        if min(len(un), len(pw)) < 2:
            errorno = -2
        for c in un:
            if c in invalid_symbols:
                errorno = -1
        for c in pw:
            if c in invalid_symbols:
                errorno = -1
        if errorno == 0:
            query_sql = utilMysql.genQuerySql('users', (USERNAME, ), (un, ))
            query_res = utilMysql.queryUsers(query_sql)
            if query_res != []:
                query_sql = utilMysql.genQuerySql('users', (USERNAME, PASSWORD), (un, pw))
                query_res = utilMysql.queryUsers(query_sql)
                if query_res != []:
                    with open('data\\info.pickle', 'wb') as f:
                        usr_info = {'login_userid': query_res[0][0],
                                    'login_username': query_res[0][1],
                                    'login_password': query_res[0][2]}
                        pickle.dump(usr_info, f)
                    self.master.show_main_window()
                else:
                    errorno = -4
            else:
                errorno = -3
            pass
        error_mes = ['', '用户名或密码包含非法字符', '用户名或密码长度不得少于6位', '不存在此用户', '密码错误']
        if errorno != 0:
            messagebox.showerror(title='错误提示！', message=error_mes[-errorno])
        pass
    def register(self):
        pass