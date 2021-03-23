# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: LoginFrm
@date: 2021-03-22 21:27
@desc:
"""
import utilMysql
from conf_win import *
from tkinter import Tk, Frame, Button, Label, LabelFrame, Text, PhotoImage, Entry, messagebox, font, StringVar, IntVar, Checkbutton
from tkinter import W, E, N, S, END, BOTTOM, TOP, BOTH, X, Y
import pickle
from src.model import Users


class LoginFrame(Frame):
    def __init__(self, master, **kw):
        self.kw = kw
        self.temp = dict()
        for key, value in self.kw.items():
            self.temp[key] = value
        Frame.__init__(self, master, self.temp)

        print(id(self.master), id(master))
        self.login_page = Frame(self)
        self.reg_page = Frame(self)
        self.username = StringVar()
        self.password = StringVar()
        self.re_un = IntVar(value=0)
        self.re_pw = IntVar(value=0)

        self.repassword = StringVar()
        self.email = StringVar()
        self.phonenumber = StringVar()
        self.nickname = StringVar()
        self.sex = StringVar(value='男')

        self.login_photo, self.login_frame = None, None
        self.create_page()
        self.create_reg_page()

    def create_page(self):
        try:
            with open('data\\info.pickle', 'rb') as f:
                usr_info = pickle.load(f)
                self.re_un.set(usr_info['login_re_un'])
                self.re_pw.set(usr_info['login_re_pw'])
                self.username.set("")
                self.password.set("")
                if self.re_un.get() == 1:
                    self.username.set(usr_info['login_username'])
                if self.re_pw.get() == 1:
                    self.password.set(usr_info['login_password'])
        except:
            pass
        self.login_photo = PhotoImage(file="data\\img_hds.gif")
        logo = Label(self.login_page, image=self.login_photo, text="^.^ 欢迎来到电商比价系统", compound=BOTTOM,
                     font=('微软雅黑', 25), fg='pink', height=400)  # compound位置关系
        logo.grid(row=0, column=0, columnspan=2, padx=130, pady=0)

        self.login_frame = LabelFrame(self.login_page, text="登录框", width=540, height=200)

        Label(self.login_frame, text='用户名:', font=('微软雅黑', 12)).grid(row=0, stick=W, padx=90, pady=10)
        Entry(self.login_frame, textvariable=self.username, width=25, font=(12)).grid(row=0, column=1, stick=W, ipady=6)

        Label(self.login_frame, text='密码:', font=('微软雅黑', 12)).grid(row=1, stick=W, padx=90, pady=10)
        login_frame_ep = Entry(self.login_frame, textvariable=self.password, show='*', width=25, font=(12))
        login_frame_ep.grid(row=1, stick=W, column=1, ipady=6)

        Checkbutton(self.login_frame, text='记住账号', variable=self.re_un).grid(row=2, padx=90)
        Checkbutton(self.login_frame, text='记住密码', variable=self.re_pw).grid(row=2, column=1, padx=60, stick=W)

        Button(self.login_frame, text='注册', command=self.show_register, font=('微软雅黑', 12)).grid(row=3, stick=W, padx=90, pady=10)
        login_frame_bl = Button(self.login_frame, text='登录', command=self.login, font=('微软雅黑', 12))
        login_frame_bl.grid(row=3, stick=W + E, column=1)

        self.login_frame.grid(row=1, stick=W+E, padx=130)
        self.login_frame.grid_propagate(0)
        login_frame_ep.bind('<KeyRelease-Return>', self.login)

        self.login_page.pack()

    def login(self, event=None):
        if event:
            print(event, event.char, event.keysym, event.keycode)
        un = self.username.get().strip()
        pw = self.password.get().strip()
        print(un, pw)
        invalid_symbols = ['\\', '/', ',', '<', '>', '?', ':', ';', '\'', '\"', '[', ']', '{', '}', '|', ' ', '\n', '\r']
        errorno = 0
        if min(len(un), len(pw)) < 2:
            errorno = -2
        for c in un + pw:
            if c in invalid_symbols:
                errorno = -1
        if errorno == 0:
            query_sql = utilMysql.genQuerySql('users', (USERNAME, ), (un, ))
            query_res = utilMysql.queryUsers(query_sql)
            if query_res:
                query_sql = utilMysql.genQuerySql('users', (USERNAME, PASSWORD), (un, pw))
                query_res = utilMysql.queryUsers(query_sql)
                if query_res:
                    with open('data\\info.pickle', 'wb') as f:
                        usr_info = {'login_userid': query_res[0][0],
                                    'login_username': query_res[0][1],
                                    'login_password': query_res[0][2],
                                    'login_re_un': self.re_un.get(),
                                    'login_re_pw': self.re_pw.get()
                        }
                        pickle.dump(usr_info, f)
                    self.master.show_main_window()
                else:
                    errorno = -4
            else:
                errorno = -3
            pass
        error_mes = ['', '用户名或密码包含非法字符', '用户名或密码长度不得少于5位', '不存在此用户', '密码错误']
        if errorno != 0:
            messagebox.showerror(title='错误提示！', message=error_mes[-errorno])

    def show_register(self):
        self.username.set("")
        self.password.set("")
        self.repassword.set("")
        self.email.set("")
        self.phonenumber.set("")
        self.nickname.set("")

        self.login_page.pack_forget()
        self.reg_page.pack()

    def re_login(self):
        try:
            with open('data\\info.pickle', 'rb') as f:
                usr_info = pickle.load(f)
                self.re_un.set(usr_info['login_re_un'])
                self.re_pw.set(usr_info['login_re_pw'])
                self.username.set("")
                self.password.set("")
                if self.re_un == 1:
                    self.username.set(usr_info['login_username'])
                if self.re_pw == 1:
                    self.password.set(usr_info['login_password'])
        except:
            pass
        self.repassword.set("")
        self.email.set("")
        self.phonenumber.set("")
        self.nickname.set("")

        self.reg_page.pack_forget()
        self.login_page.pack()

    def create_reg_page(self):
        label_font = font.Font(family='微软雅黑', size=16)
        label_font2 = font.Font(family='微软雅黑', size=18)
        entry_font = font.Font(family='微软雅黑', size=14)
        Label(self.reg_page, text="注册页面", font=label_font2).grid(row=0, sticky=E, pady=15)

        Label(self.reg_page, text="账号*:", font=label_font, width=10).grid(row=1, sticky=E, pady=10, padx=150)
        Entry(self.reg_page, textvariable=self.username, font=entry_font, width=20).grid(row=1, column=1, stick=W, columnspan=3, ipady=5, pady=12)
        Label(self.reg_page, text="密码*:", font=label_font, width=10).grid(row=2, stick=E, pady=10, padx=150)
        Entry(self.reg_page, textvariable=self.password, show='*', font=entry_font, width=20).grid(row=2, column=1, stick=W, columnspan=3, ipady=5, pady=12)
        Label(self.reg_page, text="重复密码*:", font=label_font, width=10).grid(row=3, stick=E, pady=10, padx=150)
        Entry(self.reg_page, textvariable=self.repassword, show='*', font=entry_font, width=20).grid(row=3, column=1, stick=W, columnspan=3, ipady=5, pady=12)
        Label(self.reg_page, text="邮箱:", font=label_font, width=10).grid(row=4, stick=E, pady=10, padx=150)
        Entry(self.reg_page, textvariable=self.email, font=entry_font, width=20).grid(row=4, column=1, stick=W, columnspan=3, ipady=5, pady=12)
        Label(self.reg_page, text="电话号码:", font=label_font, width=10).grid(row=5, stick=E, pady=10, padx=150)
        Entry(self.reg_page, textvariable=self.phonenumber, font=entry_font, width=20).grid(row=5, column=1, stick=W, columnspan=3, ipady=5, pady=12)
        Label(self.reg_page, text="昵称:", font=label_font, width=10).grid(row=6, stick=E, pady=10, padx=150)
        Entry(self.reg_page, textvariable=self.nickname, font=entry_font, width=20).grid(row=6, column=1, stick=W, columnspan=2, ipady=5, pady=12)
        Label(self.reg_page, text="性别:", font=label_font, width=10).grid(row=7, stick=E, pady=10, padx=150)
        Checkbutton(self.reg_page, text='男', variable=self.sex, onvalue='男', offvalue='女', font=entry_font,
                    width=6).grid(row=7, column=1, stick=W, pady=12)
        Checkbutton(self.reg_page, text='女', variable=self.sex, onvalue='女', offvalue='男', font=entry_font,
                    width=8).grid(row=7, column=2, stick=W, pady=12)
        Button(self.reg_page, text="返回", command=self.re_login, font=entry_font, width=5).grid(row=8, pady=10)
        Button(self.reg_page, text="注册", command=self.register, font=entry_font, width=5).grid(row=8, column=1,
                                                                                               columnspan=2)

    def register(self):
        un = self.username.get().strip()
        pw = self.password.get().strip()
        repw = self.repassword.get().strip()
        print(un, pw)
        re_user = Users.Users(0, self.username.get().strip(), self.password.get().strip(), self.email.get().strip(), self.phonenumber.get().strip(),
                              self.nickname.get().strip(), self.sex.get().strip())
        check_res = re_user.self_check()
        if pw != repw:
            check_res = -4
        print(check_res)
        error_mes = ['注册成功！请登录吧~', '用户名或密码包含非法字符', '用户名或密码长度不得少于5位', '邮箱或电话号码格式不正确', '两次密码输入不相同', '已存在此用户名', '系统出错，请重试！']
        if check_res == 0:
            query_sql = utilMysql.genQuerySql('users', (USERNAME,), (un,))
            query_res = utilMysql.queryUsers(query_sql)
            if not query_res:
                ins_sql = utilMysql.genInsSql('users', (USERNAME, PASSWORD, EMAIL, PHONENUMBER, NICKNAME, SEX), re_user.getAttrs())
                ins_res = utilMysql.insertUsers(ins_sql)
                if ins_res:
                    self.username.set(re_user.username)
                    self.password.set("")
                else:
                    check_res = -6
            else:
                check_res = -5
        if check_res != 0:
            messagebox.showerror(title='错误提示！', message=error_mes[-check_res])
        else:
            messagebox.showinfo(title='温馨提示！', message=error_mes[0])
            self.reg_page.pack_forget()
            self.login_page.pack()