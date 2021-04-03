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
    , font, StringVar, IntVar, Checkbutton, Menu, Radiobutton
from tkinter import filedialog, simpledialog, scrolledtext
from tkinter import W, E, N, S, END, BOTTOM, TOP, BOTH, X, Y
from tkinter import ttk
import fileinput
import os
from PIL import Image, ImageTk
import pickle
import time

from src.model import Users, Goods
from src import utilMysql, loginFrame
from src.conf_win import *
from src.spiders import taobao

class ecSpider(Tk):
    def __init__(self):
        super().__init__()
        self.rt = self
        self.rt.title("基于爬虫的电商比价系统")
        self.change_src_size(800)
        self.login_frame = loginFrame.LoginFrame(self.rt)
        self.login_frame.pack()
        self.pf_all, self.pf_tb, self.pf_jd, self.pf_tmcs, self.pf_wph = IntVar(value=0), IntVar(value=1), IntVar(value=1), IntVar(value=0), IntVar(value=0)
        # 排序方式
        self.sort_var = tk.IntVar()
        self.goodsinfo = []
        self.main_frame = Frame(self.rt, width=1200, height=800)
        self.create_main_page()
        self.show_main_window()

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
            print('id: ', self.usr_info['login_userid'])
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
        self.label_font = font.Font(family='微软雅黑', size=10)
        self.menubar = Menu(self.rt, tearoff=0)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='更新电商信息', menu=self.filemenu)
        self.filemenu.add_command(label='淘宝', command=lambda: self.update_platform_info(1))
        self.filemenu.add_command(label='京东', command=lambda: self.update_platform_info(2))
        self.filemenu.add_command(label='天猫超市', command=lambda: self.update_platform_info(3))
        self.filemenu.add_command(label='唯品会', command=lambda: self.update_platform_info(4))

        self.promenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='个人中心', menu=self.promenu)
        self.promenu.add_command(label='我的资料', command=self.show_profile)
        self.promenu.add_command(label='我的词云', command=self.show_word_cloud)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='帮助')
        self.helpmenu.add_command(label='操作说明', command=self.description)
        self.helpmenu.add_command(label='关于',  command=self.software_about)

        self.menubar.add_command(label='返回登录', command=self.goto_login)

        self.search_frame = Frame(self.main_frame, width=1200, bg='green')
        self.search_frame.pack(side='top', fill=BOTH, expand='yes')
        self.pt_frame = Frame(self.main_frame, width=1200, bg='blue')
        self.pt_frame.pack(side='top', fill=BOTH, expand='yes')
        self.goodslist_frame = Frame(self.main_frame, width=1200, bg='pink', height=700)
        self.goodslist_frame.pack(side='bottom', fill=BOTH, expand='yes')

        self.key_word = StringVar()
        self.crawl_num = IntVar(value=10)
        self.list_id = StringVar(value='（多个序号请用空格隔开）')
        Label(self.search_frame, text='搜索关键词：', width=20, bg='red', font=self.label_font).\
            grid(row=0, column=0, sticky=W, padx=50, pady=10)
        Entry(self.search_frame, width=88, font=self.label_font, textvariable=self.key_word).\
            grid(row=0, column=1, sticky=W, padx=40, pady=10, ipady=5, columnspan=4)
        Button(self.search_frame, text='search', command=self.search, font=self.label_font, width=10).\
            grid(row=0, column=5, sticky=E, padx=15)

        Label(self.pt_frame, text='平台选择：', width=15, bg='red').\
            grid(row=1, column=0, sticky=W, padx=30, pady=10)
        Checkbutton(self.pt_frame, text='全选', variable=self.pf_all, onvalue=1, offvalue=0, command=lambda: (self.pf_tb.set(1), self.pf_jd.set(1), self.pf_tmcs.set(1), self.pf_wph.set(1))).\
            grid(row=1, column=1)
        Checkbutton(self.pt_frame, text='淘宝', variable=self.pf_tb, onvalue=1, offvalue=0).\
            grid(row=1, column=2, padx=2)
        Checkbutton(self.pt_frame, text='京东', variable=self.pf_jd, onvalue=1, offvalue=0). \
            grid(row=1, column=3, padx=4)
        Checkbutton(self.pt_frame, text='天猫超市', variable=self.pf_tmcs, onvalue=1, offvalue=0). \
            grid(row=1, column=4, padx=8)
        Checkbutton(self.pt_frame, text='唯品会', variable=self.pf_wph, onvalue=1, offvalue=0). \
            grid(row=1, column=5, padx=4)
        Label(self.pt_frame, text='排序方式：', width=15, bg='red'). \
            grid(row=1, column=6, sticky=W, padx=20, pady=10)
        Radiobutton(self.pt_frame, text='默认排序', variable=self.sort_var, value=1).\
            grid(row=1, column=7, padx=3)
        Radiobutton(self.pt_frame, text='价格升序', variable=self.sort_var, value=2).\
            grid(row=1, column=8, padx=3)
        Radiobutton(self.pt_frame, text='价格倒序', variable=self.sort_var, value=3).\
            grid(row=1, column=9, padx=3)
        Label(self.pt_frame, text='爬取数量：', width=15, bg='red'). \
            grid(row=1, column=10, sticky=W, padx=30, pady=10)
        Entry(self.pt_frame, width=5, font=self.label_font, textvariable=self.crawl_num). \
            grid(row=1, column=11, sticky=W)

        Button(self.pt_frame, text='推荐结果', command=self.watchlist). \
            grid(row=2, column=0, sticky=W+E, padx=15)
        Button(self.pt_frame, text='关注列表', command=self.watchlist, width=15). \
            grid(row=2, column=1, sticky=W + E, padx=14, columnspan=2)
        Button(self.pt_frame, text='更新关注列表价格', command=self.upd_watchlist, width=15). \
            grid(row=2, column=3, sticky=W + E, padx=15, columnspan=2)
        Label(self.pt_frame, text='请输入序号：', width=15, bg='red'). \
            grid(row=2, column=6, sticky=W, padx=15)
        Entry(self.pt_frame, width=35, textvariable=self.list_id). \
            grid(row=2, column=7, sticky=W, columnspan=3)
        Button(self.pt_frame, text='加入关注列表', command=self.add_watchlist, width=10, bg='red'). \
            grid(row=2, column=10, sticky=W, padx=50, pady=10)

        s = ttk.Style()
        s.configure('Treeview', rowheight=80)
        # 表格
        self.tree = ttk.Treeview(self.goodslist_frame, columns=['1', '2', '3', '4', '5', '6', '7', '8'],
                                 height=7)
        # 表格滚动条
        self.VScroll1 = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.column('#0', width=100, anchor='w')
        self.tree.heading('#0', text='图片')
        self.tree.column('1', width=25, anchor='w')
        self.tree.heading('1', text='序')
        self.tree.column('2', width=115, anchor='w')
        self.tree.heading('2', text='ID')
        self.tree.column('3', width=80, anchor='w')
        self.tree.heading('3', text='平台')
        self.tree.column('4', width=400-40, anchor='w')
        self.tree.heading('4', text='标题')
        self.tree.column('5', width=50, anchor='w')
        self.tree.heading('5', text='价格')
        self.tree.column('6', width=50, anchor='w')
        self.tree.heading('6', text='月销量')
        self.tree.column('7', width=100, anchor='w')
        self.tree.heading('7', text='商铺')
        self.tree.column('8', width=300, anchor='w')
        self.tree.heading('8', text='链接')
        self.VScroll1.place(relx=0.979, rely=0, relwidth=0.020, relheight=1)
        self.tree.configure(yscrollcommand=self.VScroll1.set)
        self.tree.place(x=5, y=30)
        self.tree.bind('<ButtonRelease-1>', self.treeviewClick)

    def search(self):
        start = time.perf_counter()
        self.key_word.set(self.key_word.get().strip())
        print(self.key_word.get())
        rec_que_res = utilMysql.query(utilMysql.genQuerySql('records', (USERID,), (self.usr_info['login_userid'], )))
        if rec_que_res:
            new_sec = rec_que_res[0][1] + " " + self.key_word.get()
            sql = utilMysql.genUpdSql('records', (SEARCHTERM, ), (new_sec, ), (USERID, ), (self.usr_info['login_userid'], ))
            utilMysql.update(sql)
        else:
            sql = utilMysql.genInsSql('records', (USERID, SEARCHTERM, WORDCLOUD, WCPATH, TAGS), (self.usr_info['login_userid'], self.key_word.get(), '', '', ''))
            utilMysql.insert(sql)
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not isinstance(self.crawl_num.get(), int):
            self.crawl_num.set(10)

        self.goodsinfo = []
        rec_que_res = utilMysql.query(utilMysql.genQuerySql('records', (SEARCHTERM,), ("%" + self.key_word.get() + "%",)))
        if rec_que_res:
            gds_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (TITLE,), ("%" + self.key_word.get() + "%",)))
            print('gds: ', gds_que_res)
            for gd in gds_que_res:
                self.goodsinfo.append(gd)
        else:
            if self.pf_tb.get() == 1:
                self.search_tb()

        if not self.goodsinfo:
            tk.messagebox.showinfo(title='提示', message='当前无商品信息')
            return
        else:
            num = 1
            self.gdsimgs = []
            for goods in self.goodsinfo:
                good = Goods.Goods.genGoods(goods)
                goodslist = [num, *good.showItem()]
                self.gdsimg = Image.open(DATA_ROOT_PATH + good.picpath)
                self.gdsimg = self.gdsimg.resize((80, 80))
                self.gdsimg = ImageTk.PhotoImage(self.gdsimg)
                self.gdsimgs.append(self.gdsimg)
                self.tree.insert('', 'end', image=self.gdsimgs[num - 1], values=goodslist)
                num = num + 1

        end = time.perf_counter()
        print('Running time: %s Seconds' % (end - start))

    def search_tb(self, platform='淘宝'):
        res_info = taobao.getTaobaoProd(self.key_word.get(), self.crawl_num.get())
        for x in res_info:
            res_good = (x[0], platform, x[3], x[1], x[5], x[4], x[2], taobao.downPic('https:'+x[6]), self.key_word.get())
            sql = utilMysql.genInsSql('goods', (GOODID, PLATFORM, TITLE, PRICE, MSALES, SHOPNAME, HREF, PICPATH, TAGS),
                                  res_good)
            utilMysql.insert(sql)
            self.goodsinfo.append(res_good)


    def treeviewClick(self, event):
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            print(item_text)

    def watchlist(self):
        pass
    def add_watchlist(self):
        print('list_id: ', self.list_id.get())
        for item_id in self.list_id.get().split():
            try:
                sql = utilMysql.genInsSql('watchlist', )
            except:
                continue
    def upd_watchlist(self):
        pass
    def description(self):
        pass
    def software_about(self):
        pass
    def show_word_cloud(self):
        pass


if __name__ == "__main__":
    ecs = ecSpider()
    root = ecs.rt
    root.mainloop()
