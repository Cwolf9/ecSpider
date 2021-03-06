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
import os
import re
import fileinput
import tkinter as tk
from tkinter import Tk, Frame, Button, Label, LabelFrame, Text, PhotoImage, Entry, messagebox\
    , font, StringVar, IntVar, Checkbutton, Menu, Radiobutton, Toplevel
from tkinter import filedialog, simpledialog, scrolledtext
from tkinter import W, E, N, S, END, BOTTOM, TOP, BOTH, X, Y
from tkinter import ttk
from PIL import Image, ImageTk
import pickle
import time
import threading
from functools import wraps
from src.model import Users, Goods, Watchlist, Searchinfo, Records, Comments
from src import utilMysql, loginFrame, my_wordcloud, ubcf
from src.conf_win import *
from src.spiders import taobao, jingdong, tmcs, wph


def printGoodsList(ilt, num=5):
    tplt = "{:4}\t{:8}\t{:8}\t{:16}\t{:16}\t{:16}\t{:8}\t{:16}"
    print(tplt.format("序号", "goodID", "商品名称", "价格", "月销量", "店铺", "链接", "图片url"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1], g[2], g[3], g[4], g[5], g[6]))
        if count == num:
            break
    print("")


class ecSpider(Tk):
    def __init__(self):
        super().__init__()
        self.rt = self
        self.rt.title("基于爬虫的电商比价系统")
        self.change_src_size(800, 700)
        self.login_frame = loginFrame.LoginFrame(self.rt)
        self.main_frame = Frame(self.rt, width=1200, height=800)
        self.pf_frame = None
        self.profile_frame = None
        self.comment_frame = Frame(self.rt, width=1200, height=800)
        # 电商平台选择
        self.pf_all, self.pf_tb, self.pf_jd, self.pf_tmcs, self.pf_wph = IntVar(value=0), IntVar(value=1), IntVar(value=1), IntVar(value=0), IntVar(value=0)
        # 排序方式：1 默认排序，2 价格升序，3 价格降序
        self.sort_var = tk.IntVar(value=1)
        # 待显示商品信息
        self.goodsinfo = []
        self.ubcf = ubcf.Ubcf()
        self.create_main_page()
        self.create_comment_page()
        self.login_frame.pack()
        # self.show_main_window()
        # self.test_performance()

    def create_comment_page(self):
        entry_font = font.Font(family='微软雅黑', size=14)
        item_font = font.Font(family='微软雅黑', size=11)

        self.good_comment_frame = Frame(self.comment_frame, width=1200, bg='pink', height=700)
        self.good_photo = PhotoImage(file="data\\img_hds.gif")
        self.good_logo = Label(self.comment_frame, image=self.good_photo, height=300, width=300)
        self.good_logo.grid(row=0, rowspan=3, columnspan=3)
        self.good_title = Label(self.comment_frame, text='text', font=item_font)
        self.good_title.grid(row=0, column=3, columnspan=3)
        self.good_price = Label(self.comment_frame, text='text', font=item_font)
        self.good_price.grid(row=1, column=3)
        self.good_msales = Label(self.comment_frame, text='text', font=item_font)
        self.good_msales.grid(row=1, column=4)
        self.good_shopname = Label(self.comment_frame, text='text', font=item_font)
        self.good_shopname.grid(row=1, column=5)
        Button(self.comment_frame, text="返回", command=self.show_main_window, font=entry_font, width=6).grid(row=2, column=3)
        Button(self.comment_frame, text="查看评论", command=self.show_good_comment, font=entry_font, width=6).grid(row=2, column=4)
        self.good_comment_frame.grid(row=3, columnspan=6)
        self.cm_tree = ttk.Treeview(self.good_comment_frame, columns=['1', '2', '3'], height=5, show='headings')
        self.cm_VScroll = ttk.Scrollbar(self.cm_tree, orient='vertical', command=self.cm_tree.yview)
        self.cm_tree_column = ('序', '时间', '内容')
        self.cm_tree.column('1', width=30, anchor='w')
        self.cm_tree.heading('1', text='序')
        self.cm_tree.column('2', width=150, anchor='w')
        self.cm_tree.heading('2', text='时间')
        self.cm_tree.column('3', width=800, anchor='w', stretch=True)
        self.cm_tree.heading('3', text='内容')
        self.cm_VScroll.place(relx=0.979, rely=0, relwidth=0.020, relheight=1)
        self.cm_tree.configure(yscrollcommand=self.cm_VScroll.set)
        self.cm_tree.place(x=120, y=30)
        ft = tk.font.Font(font='TkDefaultFont')
        # print(ft.configure())
        # print(ft.measure('哈'), 800/12)

    def printComments(self, ilist):
        cnt = 0
        for x in ilist:
            print(cnt, x[0], x[1], x[2], x[3])
            cnt += 1
        print("")

    def show_good_comment(self):
        good_url = self.rt.clipboard_get()
        print(good_url)
        print(self.good_shopname.cget('text'))
        self.comments_list = []
        itemId = ""
        if self.good_shopname.cget('text')[:2] == '淘宝':
            cm_list = taobao.getTBProdComments(good_url)
            for cm in cm_list:
                self.comments_list.append(cm[-2:])
            itemId = re.search(r'id\=(\d+)', good_url).group(1)
            itemId = 'TB' + itemId
        if self.good_shopname.cget('text')[:2] == '京东':
            cm_list = jingdong.getJDProdComments(good_url)
            for cm in cm_list:
                self.comments_list.append([cm[0], cm[-1]])
            itemId = good_url.split('/')[-1].split('.')[0]
            itemId = 'JD' + itemId
        if self.good_shopname.cget('text')[:2] == '天猫':
            cm_list = tmcs.getTMCSProdComments(good_url)
            for cm in cm_list:
                self.comments_list.append(cm[-2:])
            itemId = re.search(r'id\=(\d+)', good_url).group(1)
            itemId = 'TMCS' + itemId

        self.delTreeView(self.cm_tree)
        num = 1
        for cm in self.comments_list:
            cm.insert(0, num)
            cm[2] = changeStrSize(cm[2], 800)
            # print(cm)
            self.cm_tree.insert('', 'end', values=cm)
            num = num + 1
            try:
                Comments.Comments.insert((itemId, cm[1], cm[2]))
            except:
                pass

    def a_new_decorator(a_func):
        """
        计算函数运行时间的装饰器
        :return:
        """
        @wraps(a_func)
        def wrapTheFunction(*args, **kwargs):
            start = time.perf_counter()
            a_func(*args, **kwargs)
            end = time.perf_counter()
            print('Decorator: Running time: %s Seconds' % (end - start))
        return wrapTheFunction

    def change_src_size(self, width=1200, height=800):
        screenwidth = self.rt.winfo_screenwidth()
        screenheight = self.rt.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.rt.geometry(size)

    def goto_login(self):
        self.rt.config(menu=Menu())
        self.main_frame.pack_forget()
        self.comment_frame.pack_forget()
        if self.pf_frame != None:
            self.pf_frame.pack_forget()
        if self.profile_frame != None:
            self.profile_frame.pack_forget()
        self.change_src_size(800, 700)
        self.login_frame.pack()

    def show_main_window(self):
        print('hello, main window')
        self.rt.config(menu=self.menubar)
        try:
            with open('data\\info.pickle', 'rb') as f:
                self.usr_info = pickle.load(f)
                print(self.usr_info)
            self.login_userid = self.usr_info['login_userid']
            self.login_username = self.usr_info['login_username']
            self.rt.title("基于爬虫的电商比价系统^.^   欢迎 " + self.usr_info['login_username'])
            print('id: ', self.usr_info['login_userid'])
            self.login_frame.pack_forget()
            self.comment_frame.pack_forget()
            if self.pf_frame != None:
                self.pf_frame.pack_forget()
            if self.profile_frame != None:
                self.profile_frame.pack_forget()
            self.change_src_size()
            self.main_frame.pack(fill=BOTH)
        except FileNotFoundError:
            messagebox.showerror(title='错误提示！', message='系统出错，请重新登录！')
            self.goto_login()

    def create_main_page(self):
        """
        创建界面主视图
        :return:
        """
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
        self.menubar.add_cascade(label='帮助', menu=self.helpmenu)
        self.helpmenu.add_command(label='操作说明', command=self.description)
        self.helpmenu.add_command(label='关于',  command=self.software_about)

        self.menubar.add_command(label='返回登录', command=self.goto_login)

        self.search_frame = LabelFrame(self.main_frame, width=1200)
        self.search_frame.pack(side='top', fill=BOTH, expand='yes')
        self.pt_frame = LabelFrame(self.main_frame, width=1200)
        self.pt_frame.pack(side='top', fill=BOTH, expand='yes')
        self.goodslist_frame = Frame(self.main_frame, width=1200, bg='pink', height=700)
        self.goodslist_frame.pack(side='bottom', fill=BOTH, expand='yes')
        self.watchlist_frame = Frame(self.main_frame, width=1200, bg='yellow', height=700)
        # self.watchlist_frame.pack(side='bottom', fill=BOTH, expand='yes')

        self.key_word = StringVar(value='')
        self.crawl_num = IntVar(value=3)
        self.list_id = StringVar(value='（多个序号请用空格隔开）')
        Label(self.search_frame, text='搜索关键词：', width=20, font=self.label_font).\
            grid(row=0, column=0, sticky=W, padx=50, pady=10)
        search_ep = Entry(self.search_frame, width=88, font=self.label_font, textvariable=self.key_word)
        search_ep.grid(row=0, column=1, sticky=W, padx=40, pady=10, ipady=5, columnspan=4)
        search_ep.bind('<KeyRelease-Return>', self.search)
        Button(self.search_frame, text='search', command=self.search, font=self.label_font, width=10).\
            grid(row=0, column=5, sticky=E, padx=15)

        Label(self.pt_frame, text='平台选择：', width=15).\
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
        Label(self.pt_frame, text='排序方式：', width=15). \
            grid(row=1, column=6, sticky=W, padx=20, pady=10)
        Radiobutton(self.pt_frame, text='默认排序', variable=self.sort_var, value=1, command=self.change_sort).\
            grid(row=1, column=7, padx=3)
        Radiobutton(self.pt_frame, text='价格升序', variable=self.sort_var, value=2, command=self.change_sort).\
            grid(row=1, column=8, padx=3)
        Radiobutton(self.pt_frame, text='价格倒序', variable=self.sort_var, value=3, command=self.change_sort).\
            grid(row=1, column=9, padx=3)
        Label(self.pt_frame, text='爬取数量：', width=15). \
            grid(row=1, column=10, sticky=W, padx=30, pady=10)
        Entry(self.pt_frame, width=5, font=self.label_font, textvariable=self.crawl_num). \
            grid(row=1, column=11, sticky=W)

        Button(self.pt_frame, text='推荐结果', command=self.recommend_result).grid(row=2, column=0, sticky=W+E, padx=15)
        Button(self.pt_frame, text='关注列表', command=self.watchlist, width=15). \
            grid(row=2, column=1, sticky=W + E, padx=14, columnspan=2)
        Button(self.pt_frame, text='更新关注列表价格', command=self.upd_watchlist, width=15). \
            grid(row=2, column=3, sticky=W + E, padx=15, columnspan=2)
        Label(self.pt_frame, text='请输入序号：', width=15). \
            grid(row=2, column=6, sticky=W, padx=15)
        Entry(self.pt_frame, width=35, textvariable=self.list_id). \
            grid(row=2, column=7, sticky=W, columnspan=3)
        Button(self.pt_frame, text='加入关注列表', command=self.add_watchlist, width=10). \
            grid(row=2, column=10, sticky=W, padx=50, pady=10)

        s = ttk.Style()
        s.configure('Treeview', rowheight=80)

        self.which_tree = 0
        # 表格及表格滚动条
        self.tree = ttk.Treeview(self.goodslist_frame, columns=['1', '2', '3', '4', '5', '6', '7', '8'],
                                 height=7)
        self.VScroll1 = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree_column = ('序', 'ID', '平台', '标题', '价格', '月销量', '商铺', '链接')
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
        self.tree.bind('<Double-Button-1>', self.double_click)
        cnt = 1
        for col in self.tree_column:  # 给所有标题加（循环上边的“手工”）
            self.tree.heading(str(cnt), text=col, command=lambda _col=str(cnt): self.treeview_sort_column(self.tree, _col, False))
            cnt += 1

        self.tree2 = ttk.Treeview(self.watchlist_frame, columns=['1', '2', '3', '4', '5', '6', '7'],
                                 height=7)
        self.VScroll12 = ttk.Scrollbar(self.tree2, orient='vertical', command=self.tree2.yview)
        self.tree2_column = ('USERID', 'GOODID', '平台', '当前价格', '最低价格', '最高价格', '链接')
        self.tree2.column('#0', width=100, anchor='w')
        self.tree2.heading('#0', text='图片')
        self.tree2.column('1', width=60, anchor='w')
        self.tree2.heading('1', text='USERID')
        self.tree2.column('2', width=120, anchor='w')
        self.tree2.heading('2', text='GOODID')
        self.tree2.column('3', width=280, anchor='w')
        self.tree2.heading('3', text='商品信息')
        self.tree2.column('4', width=60, anchor='w')
        self.tree2.heading('4', text='当前价格')
        self.tree2.column('5', width=60, anchor='w')
        self.tree2.heading('5', text='最低价格')
        self.tree2.column('6', width=60, anchor='w')
        self.tree2.heading('6', text='最高价格')
        self.tree2.column('7', width=300, anchor='w')
        self.tree2.heading('7', text='链接')
        self.VScroll12.place(relx=0.979, rely=0, relwidth=0.020, relheight=1)
        self.tree2.configure(yscrollcommand=self.VScroll12.set)
        self.tree2.place(x=70, y=30)
        self.tree2.bind('<ButtonRelease-1>', self.treeviewClick)
        self.tree2.bind('<Double-Button-1>', self.double_click)
        cnt = 1
        for col in self.tree2_column:  # 给所有标题加（循环上边的“手工”）
            self.tree2.heading(str(cnt), text=col,
                              command=lambda _col=str(cnt): self.treeview2_sort_column(self.tree2, _col, False))
            cnt += 1

    def double_click(self, event):
        print('double click')
        self.rt.clipboard_clear()
        good = None
        if self.which_tree == 1:
            for item in self.tree.selection():
                item_text = self.tree.item(item, "values")
                print('double: ', item_text)
                good = Goods.Goods.genGoods((*item_text[1:], ''))
        if self.which_tree == 2:
            for item in self.tree2.selection():
                item_text = self.tree2.item(item, "values")
                print('double: ', item_text)
                good = Goods.Goods.queryWithGoodid(item_text[1])
        print(good)
        self.rt.clipboard_append("https://" + good.href)
        self.good_photo = Image.open(DATA_ROOT_PATH + good.picpath)
        # 修改photo大小以适应界面
        if max(self.good_photo.width, self.good_photo.height) > 300:
            print(self.good_photo.height, self.good_photo.width, max(self.good_photo.height, self.good_photo.width))
            k = 300 / max(self.good_photo.width, self.good_photo.height)
            self.good_photo = self.good_photo.resize((int(self.good_photo.width * k), int(self.good_photo.height * k)))
        self.good_photo = ImageTk.PhotoImage(self.good_photo)
        self.good_logo.configure(image=self.good_photo)
        self.good_title.configure(text=good.title[:60])
        self.good_price.configure(text='价格：'+str(good.price))
        self.good_msales.configure(text='月销量：'+str(good.msales))
        self.good_shopname.configure(text=good.platform+'：'+good.shopname)
        self.main_frame.pack_forget()
        self.comment_frame.pack()

    def delTreeView(self, tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def treeviewClick(self, event):
        """
        点击列表任意一行时复制商品连接
        :param event:
        :return:
        """
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            print(item_text)
            self.rt.clipboard_clear()
            self.rt.clipboard_append("https://" + item_text[7])
        for item in self.tree2.selection():
            item_text = self.tree2.item(item, "values")
            print(item_text)
            self.rt.clipboard_clear()
            self.rt.clipboard_append("https://" + item_text[6])

    def change_sort(self):
        if self.which_tree == 1:
            if self.sort_var.get() == 1:
                self.treeview_sort_column(self.tree, '1', False)
            if self.sort_var.get() == 2:
                self.treeview_sort_column(self.tree, '5', False)
            if self.sort_var.get() == 3:
                self.treeview_sort_column(self.tree, '5', True)
        if self.which_tree == 2:
            if self.sort_var.get() == 1:
                self.treeview2_sort_column(self.tree2, '2', False)
            if self.sort_var.get() == 2:
                self.treeview2_sort_column(self.tree2, '4', False)
            if self.sort_var.get() == 3:
                self.treeview2_sort_column(self.tree2, '4', True)

    def treeview_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        if col == '1' or col == '5' or col == '6':
            l = []
            for k in tv.get_children(''):
                if tv.set(k, col) == '不显示':
                    l.append((0.0, k))
                else:
                    l.append((float(tv.set(k, col)), k))
            # l = [(float(tv.set(k, col)), k) for k in tv.get_children('')]
        else:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
        print(tv.get_children(''), '\n', l)
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def treeview2_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        if col == '4' or col == '5' or col == '6':
            l = [(float(tv.set(k, col)), k) for k in tv.get_children('')]
        else:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
        print(tv.get_children(''))
        print(l)
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
            print(k)
        tv.heading(col, command=lambda: self.treeview2_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def update_platform_info(self, pf_id):
        print(pf_id)
        pf_strs = ['', '淘宝', '京东', '天猫超市', '唯品会']
        self.comment_frame.pack_forget()
        self.main_frame.pack_forget()
        if self.profile_frame: self.profile_frame.pack_forget()
        if self.pf_frame == None:
            self.pf_frame = Frame(self.rt, width=1200, height=800)
            self.pf_ck_e = StringVar()
            self.pf_re_e = StringVar()
            self.pf_label = Label(self.pf_frame, text=pf_strs[pf_id], font=self.menu_font, pady=50)
            self.pf_label.grid(row=0, column=0, columnspan=2)
            Label(self.pf_frame, text='cookie: ', font=self.menu_font, width=10, padx=30).grid(row=1, column=0)
            Entry(self.pf_frame, font=self.menu_font, width=20, textvariable=self.pf_ck_e).grid(row=1, column=1)
            Label(self.pf_frame, text='referer: ', font=self.menu_font, width=10, padx=30).grid(row=2, column=0)
            Entry(self.pf_frame, font=self.menu_font, width=20, textvariable=self.pf_re_e).grid(row=2, column=1)
            Button(self.pf_frame, text='返回', font=self.menu_font, width=10, command=self.show_main_window, padx=30).grid(row=3, column=0, pady=80, padx=30)
            Button(self.pf_frame, text='保存', font=self.menu_font, width=10, command=self.save_pf_info, padx=30).grid(row=3, column=1, pady=80)
        else:
            self.pf_label.configure(text=pf_strs[pf_id])
        self.pf_frame.pack()

    def save_pf_info(self):
        tup = (int(self.login_userid), self.pf_label['text'], self.pf_ck_e.get(), self.pf_re_e.get(), 0)
        Searchinfo.Searchinfo.insert(tup)

    def show_profile(self):
        self.main_frame.pack_forget()
        self.comment_frame.pack_forget()
        if self.pf_frame: self.pf_frame.pack_forget()
        self.cg_username = StringVar(value=self.login_username)
        login_user = Users.Users.queryWithUserid(self.login_userid)
        if self.profile_frame == None:
            self.profile_frame = Frame(self.rt, width=800, height=500)
            self.cg_password = StringVar()
            self.cg_repassword = StringVar()
            self.cg_email = StringVar(value=login_user.email)
            self.cg_phonenumber = StringVar(value=login_user.phonenumber)
            self.cg_nickname = StringVar(value=login_user.nickname)
            self.cg_sex = StringVar(value=login_user.sex)
            self.pf_label = Label(self.profile_frame, text='欢迎用户：' + self.login_username, font=self.menu_font, pady=50)
            self.pf_label.grid(row=0, column=0, columnspan=2)
            label_font = self.label_font
            entry_font = font.Font(family='微软雅黑', size=14)
            Label(self.profile_frame, text="账号*:", font=label_font, width=10).grid(row=1, sticky=E, pady=10, padx=150)
            Entry(self.profile_frame, textvariable=self.cg_username, font=entry_font, width=20).grid(row=1, column=1, stick=W,
                                                                                             columnspan=3, ipady=5,
                                                                                             pady=12)
            Label(self.profile_frame, text="密码*:", font=label_font, width=10).grid(row=2, stick=E, pady=10, padx=150)
            Entry(self.profile_frame, textvariable=self.cg_password, show='*', font=entry_font, width=20).grid(row=2, column=1,
                                                                                                       stick=W,
                                                                                                       columnspan=3,
                                                                                                       ipady=5, pady=12)
            Label(self.profile_frame, text=" 确认密码*:", font=label_font, width=10).grid(row=3, stick=E, pady=10, padx=150)
            Entry(self.profile_frame, textvariable=self.cg_repassword, show='*', font=entry_font, width=20).grid(row=3,
                                                                                                         column=1,
                                                                                                         stick=W,
                                                                                                         columnspan=3,
                                                                                                         ipady=5,
                                                                                                         pady=12)
            Label(self.profile_frame, text="邮箱:", font=label_font, width=10).grid(row=4, stick=E, pady=10, padx=150)
            Entry(self.profile_frame, textvariable=self.cg_email, font=entry_font, width=20).grid(row=4, column=1, stick=W,
                                                                                          columnspan=3, ipady=5,
                                                                                          pady=12)
            Label(self.profile_frame, text="电话号码:", font=label_font, width=10).grid(row=5, stick=E, pady=10, padx=150)
            Entry(self.profile_frame, textvariable=self.cg_phonenumber, font=entry_font, width=20).grid(row=5, column=1,
                                                                                                stick=W, columnspan=3,
                                                                                                ipady=5, pady=12)
            Label(self.profile_frame, text="昵称:", font=label_font, width=10).grid(row=6, stick=E, pady=10, padx=150)
            Entry(self.profile_frame, textvariable=self.cg_nickname, font=entry_font, width=20).grid(row=6, column=1, stick=W,
                                                                                             columnspan=2, ipady=5,
                                                                                             pady=12)
            Label(self.profile_frame, text="性别:", font=label_font, width=10).grid(row=7, stick=E, pady=10, padx=150)
            Checkbutton(self.profile_frame, text='男', variable=self.cg_sex, onvalue='男', offvalue='女', font=entry_font,
                        width=6).grid(row=7, column=1, stick=W, pady=12)
            Checkbutton(self.profile_frame, text='女', variable=self.cg_sex, onvalue='女', offvalue='男', font=entry_font,
                        width=8).grid(row=7, column=2, stick=W, pady=12)
            Button(self.profile_frame, text="返回", command=self.show_main_window, font=entry_font, width=6).grid(row=8, pady=10)
            Button(self.profile_frame, text="确认修改", command=self.save_profile, font=entry_font, width=6).grid(row=8, column=1,
                                                                                                   columnspan=2)
        else:
            self.cg_email.set(login_user.email)
            self.cg_phonenumber.set(login_user.phonenumber)
            self.cg_nickname.set(login_user.nickname)
            self.cg_sex.set(login_user.sex)
        self.profile_frame.pack()

    def save_profile(self):
        print(Users.Users.genUsers((self.login_userid, self.cg_username.get(), self.cg_password.get(), self.cg_email.get(), self.cg_phonenumber.get(), self.cg_nickname.get(), self.cg_sex.get())))
        if self.cg_password.get() != self.cg_repassword.get():
            messagebox.showerror(title='提示', message='两次密码输入不一致')
            return
        if Users.Users.genUsers((self.login_userid, self.cg_username.get(), self.cg_password.get(), self.cg_email.get(), self.cg_phonenumber.get(), self.cg_nickname.get(), self.cg_sex.get())).self_check() < 0:
            messagebox.showerror(title='提示', message='请检查输入信息是否合法')
            return
        f1 = (USERNAME, PASSWORD, EMAIL, PHONENUMBER, NICKNAME, SEX)
        v1 = (self.cg_username.get(), self.cg_password.get(), self.cg_email.get(), self.cg_phonenumber.get(), self.cg_nickname.get(), self.cg_sex.get())
        f2 = (USERID, )
        v2 = (self.login_userid, )
        Users.Users.updateUsers1(f1, v1, f2, v2)


    def search(self, event=None):
        """
        统计搜索+显示总用时
        :param event:
        :return:
        """
        start = time.perf_counter()
        self.which_tree = 1
        self.goodslist_frame.pack(side='bottom', fill=BOTH, expand='yes')
        self.watchlist_frame.pack_forget()
        self.key_word.set(self.key_word.get().strip())
        print(self.key_word.get())
        if not self.key_word.get():
            tk.messagebox.showinfo(title='提示', message='请输入搜索关键词')
            return
        if not isinstance(self.crawl_num.get(), int):
            self.crawl_num.set(10)

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.goodsinfo = []
        if self.pf_tb.get() == 1:
            rec_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('淘宝', "%" + self.key_word.get() + "%")))
            if not rec_que_res:
                self.search_tb()
        if self.pf_jd.get() == 1:
            rec_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('京东', "%" + self.key_word.get() + "%")))
            if not rec_que_res:
                self.search_jd()
        if self.pf_tmcs.get() == 1:
            rec_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('天猫超市', "%" + self.key_word.get() + "%")))
            if not rec_que_res:
                self.search_tmcs()
        if self.pf_wph.get() == 1:
            rec_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('唯品会', "%" + self.key_word.get() + "%")))
            if not rec_que_res:
                self.search_wph()
        # 获取商品待显示列表
        gds_que_res = []
        if self.pf_tb.get() == 1:
            rec_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('淘宝', "%" + self.key_word.get() + "%")))
            gds_que_res.extend(rec_que_res)
        if self.pf_jd.get() == 1:
            rec_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('京东', "%" + self.key_word.get() + "%")))
            gds_que_res.extend(rec_que_res)
        if self.pf_tmcs.get() == 1:
            rec_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('天猫超市', "%" + self.key_word.get() + "%")))
            gds_que_res.extend(rec_que_res)
        if self.pf_wph.get() == 1:
            rec_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('唯品会', "%" + self.key_word.get() + "%")))
            gds_que_res.extend(rec_que_res)

        for gd in gds_que_res:
            self.goodsinfo.append(gd)

        self.goodsinfo_bkb = self.goodsinfo
        self.show_search()
        # 如果成功搜索到数据，将key word添入搜索记录
        if self.goodsinfo:
            rec_que_res = utilMysql.query(utilMysql.genQuerySql('records', (USERID,), (self.usr_info['login_userid'],)))
            if rec_que_res:
                new_sec = rec_que_res[0][1] + " " + self.key_word.get()
                sql = utilMysql.genUpdSql('records', (SEARCHTERM,), (new_sec,), (USERID,), (self.usr_info['login_userid'],))
                utilMysql.update(sql)
            else:
                sql = utilMysql.genInsSql('records', (USERID, SEARCHTERM, WORDCLOUD, WCPATH, TAGS),
                                          (self.usr_info['login_userid'], self.key_word.get(), '', '', ''))
                utilMysql.insert(sql)
        end = time.perf_counter()
        print('Search+show Running time: %s Seconds' % (end - start))

    def show_search(self):
        """
        显示搜索结果
        :return:
        """
        if self.sort_var.get() == 1:
            self.goodsinfo = self.goodsinfo_bkb
        if self.sort_var.get() == 2:
            self.goodsinfo = sorted(self.goodsinfo_bkb, key=lambda elm: elm[3])
        if self.sort_var.get() == 3:
            self.goodsinfo = sorted(self.goodsinfo_bkb, key=lambda elm: elm[3], reverse=True)

        if not self.goodsinfo:
            tk.messagebox.showinfo(title='提示', message='当前无商品信息')
            return
        else:
            self.delTreeView(self.tree)
            num = 1
            self.gdsimgs = []
            for goods in self.goodsinfo:
                good = Goods.Goods.genGoods(goods)
                goodslist = [num, *good.showItem(), good.picpath]
                if goodslist[5] == 0:
                    goodslist[5] = '不显示'
                self.gdsimg = Image.open(DATA_ROOT_PATH + good.picpath)
                self.gdsimg = self.gdsimg.resize((80, 80))
                self.gdsimg = ImageTk.PhotoImage(self.gdsimg)
                self.gdsimgs.append(self.gdsimg)
                self.tree.insert('', 'end', image=self.gdsimgs[num - 1], values=goodslist)
                num = num + 1

    def my_single_down(self, platform, x, key_word):
        """
        将爬取到的结果存入数据库和商品待显示列表
        根据picpath获取商品缩略图
        TODO：爬取图片效率有待提高
        :param platform:
        :param x:
        :param key_word:
        :return:
        """
        picpath = 'img_huaban.gif'
        # if platform == '淘宝':
        #     picpath = taobao.downPic('https:' + x[6])
        res_good = (x[0], platform, x[1], x[2], x[3], x[4], x[5], picpath, key_word)
        sql = utilMysql.genInsSql('goods', (GOODID, PLATFORM, TITLE, PRICE, MSALES, SHOPNAME, HREF, PICPATH, TAGS),
                                  res_good)
        utilMysql.insert(sql)
        # self.goodsinfo.append(res_good)

    @a_new_decorator
    def mysql_tb(self):
        rec_que_res = utilMysql.query(
            utilMysql.genQuerySql('goods', (PLATFORM, TAGS), ('淘宝', "%" + self.key_word.get() + "%")))
        printGoodsList(rec_que_res)
        return rec_que_res

    @a_new_decorator
    def search_tb(self, platform='淘宝'):
        # 注意res_info的排列
        res_info = taobao.getTaobaoProd(self.key_word.get(), self.crawl_num.get())
        # self.printGoodsList(res_info)
        start = time.perf_counter()
        # 多线程异步存取商品（下载缩略图）
        t = None
        for x in res_info:
            t = threading.Thread(target=self.my_single_down, args=(platform, x, self.key_word.get()))
            t.start()
            t.join()
        end = time.perf_counter()
        print('tb Downloading: Running time: %s Seconds' % (end - start))

    @a_new_decorator
    def search_jd(self, platform='京东'):
        # 注意res_info的排列
        res_info = jingdong.getJDProd(self.key_word.get(), self.crawl_num.get())
        start = time.perf_counter()
        # 多线程异步存取商品（下载缩略图）
        t = None
        for x in res_info:
            t = threading.Thread(target=self.my_single_down, args=(platform, x, self.key_word.get()))
            t.start()
            t.join()
        end = time.perf_counter()
        print('jd Downloading: Running time: %s Seconds' % (end - start))

    @a_new_decorator
    def search_tmcs(self, platform='天猫超市'):
        # 注意res_info的排列
        res_info = tmcs.getTMCSProd(self.key_word.get(), self.crawl_num.get())
        start = time.perf_counter()
        # 多线程异步存取商品（下载缩略图）
        t = None
        for x in res_info:
            t = threading.Thread(target=self.my_single_down, args=(platform, x, self.key_word.get()))
            t.start()
            t.join()
        end = time.perf_counter()
        print('tmcs Downloading: Running time: %s Seconds' % (end - start))

    @a_new_decorator
    def search_wph(self, platform='唯品会'):
        # 注意res_info的排列
        res_info = wph.getWPHProd(self.key_word.get(), self.crawl_num.get())
        start = time.perf_counter()
        # 多线程异步存取商品（下载缩略图）
        t = None
        for x in res_info:
            t = threading.Thread(target=self.my_single_down, args=(platform, x, self.key_word.get()))
            t.start()
            t.join()
        end = time.perf_counter()
        print('wph Downloading: Running time: %s Seconds' % (end - start))

    def watchlist(self):
        """
        显示关注列表
        :return:
        """
        self.which_tree = 2
        self.goodslist_frame.pack_forget()
        self.watchlist_frame.pack(side='bottom', fill=BOTH, expand='yes')
        sql = utilMysql.genQuerySql('watchlist', (USERID, ), (self.usr_info['login_userid'], ))
        wl_res = utilMysql.query(sql)
        print(wl_res)
        if not wl_res:
            tk.messagebox.showinfo(title='提示', message='当前无商品信息')
            return
        else:
            self.delTreeView(self.tree2)
            num = 1
            self.gdsimgs = []
            for iwl in wl_res:
                wl = Watchlist.Watchlist.genWatchlist(iwl)
                print(wl)
                wlslist = [*wl.showItem(), wl.picpath]
                print(wlslist)
                self.gdsimg = Image.open(DATA_ROOT_PATH + wl.picpath)
                self.gdsimg = self.gdsimg.resize((80, 80))
                self.gdsimg = ImageTk.PhotoImage(self.gdsimg)
                self.gdsimgs.append(self.gdsimg)
                self.tree2.insert('', 'end', image=self.gdsimgs[num - 1], values=wlslist)
                num = num + 1

    def add_watchlist(self):
        """
        添加搜索到的某些商品进入关注列表，同时更新商品的历史最低最高价格
        :return:
        """
        print('list_id: ', self.list_id.get())
        for item_id in self.list_id.get().split():
            try:
                sql = utilMysql.genQuerySql('watchlist', (USERID, GOODID), (self.usr_info['login_userid'], self.goodsinfo[int(item_id)-1][0]))
                wl_res = utilMysql.query(sql)
                if wl_res:
                    print('wl_res: ', wl_res)
                    print(self.goodsinfo[int(item_id) - 1])
                    flag = 0
                    if float(self.goodsinfo[int(item_id) - 1][3]) < float(wl_res[0][4]):
                        sql = utilMysql.genUpdSql('watchlist', (LOWPRICE, NOWPRICE), (self.goodsinfo[int(item_id) - 1][3], self.goodsinfo[int(item_id) - 1][3]),
                                                  (USERID, GOODID), (self.usr_info['login_userid'], self.goodsinfo[int(item_id)-1][0]))
                        utilMysql.update(sql)
                        flag = 1
                    if float(self.goodsinfo[int(item_id) - 1][3]) > float(wl_res[0][5]):
                        sql = utilMysql.genUpdSql('watchlist', (HIGHPRICE, NOWPRICE), (self.goodsinfo[int(item_id) - 1][3], self.goodsinfo[int(item_id) - 1][3]),
                                                  (USERID, GOODID), (self.usr_info['login_userid'], self.goodsinfo[int(item_id)-1][0]))
                        utilMysql.update(sql)
                        flag = 1
                    if flag == 0:
                        sql = utilMysql.genUpdSql('watchlist', (NOWPRICE, ), (self.goodsinfo[int(item_id) - 1][3], ),
                                          (USERID, GOODID),
                                          (self.usr_info['login_userid'], self.goodsinfo[int(item_id)-1][0]))
                        utilMysql.update(sql)
                else:
                    sql = utilMysql.genInsSql('watchlist', (USERID, GOODID, PLATFORM, NOWPRICE, LOWPRICE, HIGHPRICE, HREF, PICPATH),
                                                (self.usr_info['login_userid'], self.goodsinfo[int(item_id) - 1][0], self.goodsinfo[int(item_id) - 1][1] + ' ' + self.goodsinfo[int(item_id) - 1][2], self.goodsinfo[int(item_id) - 1][3], self.goodsinfo[int(item_id) - 1][3], self.goodsinfo[int(item_id) - 1][3], self.goodsinfo[int(item_id) - 1][6], self.goodsinfo[int(item_id) - 1][7]))
                    utilMysql.insert(sql)
            except:
                continue

    def upd_watchlist(self):
        """
        更新关注列表历史最低最高价格
        :return:
        """
        sql = utilMysql.genQuerySql('watchlist', (USERID,), (self.usr_info['login_userid'],))
        wl_res = utilMysql.query(sql)
        for iwl in wl_res:
            new_p = taobao.getNewPrice('https:' + iwl[6], float(iwl[3]))
            flag = 0
            if new_p < float(iwl[4]):
                sql = utilMysql.genUpdSql('watchlist', (LOWPRICE, NOWPRICE),
                                          (new_p, new_p),
                                          (USERID, GOODID),
                                          (self.usr_info['login_userid'], iwl[1]))
                utilMysql.update(sql)
                flag = 1
            if new_p > float(iwl[5]):
                sql = utilMysql.genUpdSql('watchlist', (HIGHPRICE, NOWPRICE),
                                          (new_p, new_p),
                                          (USERID, GOODID),
                                          (self.usr_info['login_userid'], iwl[1]))
                utilMysql.update(sql)
                flag = 1
            if flag == 0 and new_p != float(iwl[3]):
                sql = utilMysql.genUpdSql('watchlist', (NOWPRICE, ), (new_p, ),
                                          (USERID, GOODID),
                                          (self.usr_info['login_userid'], iwl[1]))
                utilMysql.update(sql)
        self.watchlist()

    def description(self):
        """
        软件使用简介
        :return:
        """
        tl = Toplevel()
        screenwidth = self.rt.winfo_screenwidth()
        screenheight = self.rt.winfo_screenheight()
        size = '%dx%d+%d+%d' % (400, 300, (screenwidth - 400) / 2, (screenheight - 300) / 2)
        tl.geometry(size)
        tl.title('ecSpider1.0')
        Label(tl, text='    在搜索框输入待搜索的关键词即可在您选定的电商平台中搜索相关信息.\n'
                       '    默认按综合评价来排序，可选按价格排序。\n'
                       '    支持的电商平台有淘宝，京东，天猫超市，唯品会。\n'
                       '    对于您感兴趣的商品，可以添加到您的关注列表中，并可以随时更新关注列表中商品的价格。', font=self.label_font, wraplength=300, justify='left', padx=60).pack()
        Label(tl, text='    在个人中心中可以查看您的专属词云哦~\n'
                       '    为了方便您的使用，建议不定期更新您的电商信息，如：cookie等。', font=self.label_font, wraplength=300,
              justify='left', padx=10).pack()

    def software_about(self):
        """
        关于系统
        :return:
        """
        tl = Toplevel()
        screenwidth = self.rt.winfo_screenwidth()
        screenheight = self.rt.winfo_screenheight()
        size = '%dx%d+%d+%d' % (400, 300, (screenwidth - 400) / 2, (screenheight - 300) / 2)
        tl.geometry(size)
        tl.title('ecSpider 1.0')
        Label(tl, text='基于Python爬虫的电商比价系统\n'
                       'python3.6版本，数据库使用MySQL8，爬虫基于requests库定制。', font=self.label_font, wraplength=280,
              justify='left', padx=60).pack()

    def show_word_cloud(self):
        """
        显示用户专属词云
        :return:
        """
        record = Records.Records.getRecords(self.login_userid)
        if record:
            my_words_list = [record[0][1]]
        for goods in self.goodsinfo:
            goodid = goods[0]
            comments = Comments.Comments.getComments(goodid)
            for comment in comments:
                my_words_list.append(comment[1])
        try:
            my_wordcloud.create_word_cloud(my_words_list)
        except Exception as e:
            print(e)
            pass

    def recommend_result(self):
        """
        展示推荐结果，算法为基于用户的协同过滤推荐算法，需要一定的历史数据量结果才准确
        TODO: 推荐
        :return:
        """
        self.which_tree = 1
        self.goodslist_frame.pack(side='bottom', fill=BOTH, expand='yes')
        self.watchlist_frame.pack_forget()
        try:
            goodId_list = self.ubcf.get_recommend(self.login_userid)
            self.delTreeView(self.tree)
            num = 1
            self.gdsimgs = []
            for goodId in goodId_list:
                good = Goods.Goods.queryWithGoodid(goodId)
                goodslist = [num, *good.showItem(), good.picpath]
                if goodslist[5] == 0:
                    goodslist[5] = '不显示'
                self.gdsimg = Image.open(DATA_ROOT_PATH + good.picpath)
                self.gdsimg = self.gdsimg.resize((80, 80))
                self.gdsimg = ImageTk.PhotoImage(self.gdsimg)
                self.gdsimgs.append(self.gdsimg)
                self.tree.insert('', 'end', image=self.gdsimgs[num - 1], values=goodslist)
                num = num + 1
        except Exception as e:
            print(e)

    def count_running_time(a_func):
        @wraps(a_func)
        def wrapTheFunction(*args, **kwargs):
            start = time.perf_counter()
            a_func(*args, **kwargs)
            end = time.perf_counter()
            print('\nTotal running time: %s Seconds' % (end - start))
        return wrapTheFunction

    @count_running_time
    def test_performance(self):
        print('淘宝 查询关键字, 搜索项目数: ', self.key_word.get(), self.crawl_num.get())
        print('即时爬取法：')
        self.search_tb()
        print('\n数据库法：')
        self.mysql_tb()




if __name__ == "__main__":
    ecs = ecSpider()
    root = ecs.rt
    root.mainloop()
