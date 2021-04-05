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
import fileinput
import tkinter as tk
from tkinter import Tk, Frame, Button, Label, LabelFrame, Text, PhotoImage, Entry, messagebox\
    , font, StringVar, IntVar, Checkbutton, Menu, Radiobutton
from tkinter import filedialog, simpledialog, scrolledtext
from tkinter import W, E, N, S, END, BOTTOM, TOP, BOTH, X, Y
from tkinter import ttk
from PIL import Image, ImageTk
import pickle
import time
from functools import wraps

from src.model import Users, Goods, Watchlist
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
        self.sort_var = tk.IntVar(value=1)
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
        self.watchlist_frame = Frame(self.main_frame, width=1200, bg='yellow', height=700)
        # self.watchlist_frame.pack(side='bottom', fill=BOTH, expand='yes')


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
        Radiobutton(self.pt_frame, text='默认排序', variable=self.sort_var, value=1, command=self.show_search).\
            grid(row=1, column=7, padx=3)
        Radiobutton(self.pt_frame, text='价格升序', variable=self.sort_var, value=2, command=self.show_search).\
            grid(row=1, column=8, padx=3)
        Radiobutton(self.pt_frame, text='价格倒序', variable=self.sort_var, value=3, command=self.show_search).\
            grid(row=1, column=9, padx=3)
        Label(self.pt_frame, text='爬取数量：', width=15, bg='red'). \
            grid(row=1, column=10, sticky=W, padx=30, pady=10)
        Entry(self.pt_frame, width=5, font=self.label_font, textvariable=self.crawl_num). \
            grid(row=1, column=11, sticky=W)

        Button(self.pt_frame, text='推荐结果', command=self.recommend_result).grid(row=2, column=0, sticky=W+E, padx=15)
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

        self.which_tree = 1
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
        self.tree2.column('3', width=80, anchor='w')
        self.tree2.heading('3', text='平台')
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
        self.tree2.place(x=170, y=30)
        cnt = 1
        for col in self.tree2_column:  # 给所有标题加（循环上边的“手工”）
            self.tree2.heading(str(cnt), text=col,
                              command=lambda _col=str(cnt): self.treeview2_sort_column(self.tree2, _col, False))
            cnt += 1

    def a_new_decorator(a_func):
        @wraps(a_func)
        def wrapTheFunction(*args, **kwargs):
            start = time.perf_counter()
            a_func(*args, **kwargs)
            end = time.perf_counter()
            print('Decorator: Running time: %s Seconds' % (end - start))

        return wrapTheFunction

    def delTreeView(self, tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def treeview_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        if col == '5' or col == '6':
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

    def search(self):
        start = time.perf_counter()
        self.goodslist_frame.pack(side='bottom', fill=BOTH, expand='yes')
        self.watchlist_frame.pack_forget()
        self.key_word.set(self.key_word.get().strip())
        print(self.key_word.get())
        if not isinstance(self.crawl_num.get(), int):
            self.crawl_num.set(10)

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.goodsinfo = []
        rec_que_res = utilMysql.query(utilMysql.genQuerySql('records', (SEARCHTERM,), ("%" + self.key_word.get() + "%",)))
        print('rec_que_res: ', rec_que_res)
        if rec_que_res:
            gds_que_res = utilMysql.query(
                utilMysql.genQuerySql('goods', (TITLE,), ("%" + self.key_word.get() + "%",)))
            print('gds: ', gds_que_res)
            for gd in gds_que_res:
                self.goodsinfo.append(gd)
        else:
            if self.pf_tb.get() == 1:
                self.search_tb()

        self.goodsinfo_bkb = self.goodsinfo
        self.show_search()

        if self.goodsinfo:
            rec_que_res = utilMysql.query(utilMysql.genQuerySql('records', (USERID,), (self.usr_info['login_userid'],)))
            print('rec_que_res: ', rec_que_res)
            if rec_que_res:
                new_sec = rec_que_res[0][1] + " " + self.key_word.get()
                print(new_sec)
                sql = utilMysql.genUpdSql('records', (SEARCHTERM,), (new_sec,), (USERID,), (self.usr_info['login_userid'],))
                utilMysql.update(sql)
            else:
                sql = utilMysql.genInsSql('records', (USERID, SEARCHTERM, WORDCLOUD, WCPATH, TAGS),
                                          (self.usr_info['login_userid'], self.key_word.get(), '', '', ''))
                utilMysql.insert(sql)
        end = time.perf_counter()
        print('Running time: %s Seconds' % (end - start))

    def show_search(self):
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
                goodslist = [num, *good.showItem()]
                self.gdsimg = Image.open(DATA_ROOT_PATH + good.picpath)
                self.gdsimg = self.gdsimg.resize((80, 80))
                self.gdsimg = ImageTk.PhotoImage(self.gdsimg)
                self.gdsimgs.append(self.gdsimg)
                self.tree.insert('', 'end', image=self.gdsimgs[num - 1], values=goodslist)
                num = num + 1

    @a_new_decorator
    def search_tb(self, platform='淘宝'):
        print(self.key_word.get(), self.crawl_num.get())
        res_info = taobao.getTaobaoProd(self.key_word.get(), self.crawl_num.get())
        start = time.perf_counter()
        for x in res_info:
            res_good = (x[0], platform, x[3], x[1], x[5], x[4], x[2], taobao.downPic('https:'+x[6]), self.key_word.get())
            sql = utilMysql.genInsSql('goods', (GOODID, PLATFORM, TITLE, PRICE, MSALES, SHOPNAME, HREF, PICPATH, TAGS),
                                  res_good)
            utilMysql.insert(sql)
            self.goodsinfo.append(res_good)
        end = time.perf_counter()
        print('Downloading: Running time: %s Seconds' % (end - start))

    def treeviewClick(self, event):
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            print(item_text)
            self.rt.clipboard_clear()
            self.rt.clipboard_append("https:" + item_text[7])

    def watchlist(self):
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
                wlslist = [*wl.showItem()]
                print(wlslist)
                self.gdsimg = Image.open(DATA_ROOT_PATH + wl.picpath)
                self.gdsimg = self.gdsimg.resize((80, 80))
                self.gdsimg = ImageTk.PhotoImage(self.gdsimg)
                self.gdsimgs.append(self.gdsimg)
                self.tree2.insert('', 'end', image=self.gdsimgs[num - 1], values=wlslist)
                num = num + 1

    def add_watchlist(self):
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
        pass
    def software_about(self):
        pass
    def show_word_cloud(self):
        pass
    def recommend_result(self):
        self.show_search()


if __name__ == "__main__":
    ecs = ecSpider()
    root = ecs.rt
    root.mainloop()
