# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: textEdit
@date: 2021-03-22 20:49
@desc:
"""
'''
im = Image.open(path)
im.show()
'''
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import colorchooser
from tkinter import font
import tkinter as tk
import tkinter.scrolledtext as tkst
import fileinput
import os
# import win32clipboard
import tkinter.filedialog

t1 = []
root = None

def die(event=None):
    root.destroy()

def about():
    messagebox.showinfo(title="当前版本为1.0,欢迎使用", message="**作者:\n**状态:继续努力ing")

class editor():
    def __init__(self, rt):
        if rt == None:
            self.t = tk.Tk()
        else:
            self.t = tk.Toplevel(rt)

        self.t.title("文本编辑器%d" % (len(t1) + 1))

        self.frm_file = tk.Frame(self.t)
        self.frm_file.grid(row=0, column=0, padx=0, sticky=W)
        self.btn_open = Button(self.frm_file, text="打开", relief=GROOVE, command=self.openfile)
        self.btn_open.pack(side=LEFT, padx=5, fill=BOTH, expand=1)
        self.btn_new = Button(self.frm_file, text="新建", relief=GROOVE, command=self.neweditor)
        self.btn_new.pack(side=LEFT, padx=5, fill=BOTH)
        self.btn_save = Button(self.frm_file, text="保存", relief=GROOVE, command=self.savefile)
        self.btn_save.pack(side=LEFT, padx=5, fill=BOTH)
        self.btn_saveas = Button(self.frm_file, text="另存为", relief=GROOVE, command=self.saveasfile)
        self.btn_saveas.pack(side=LEFT, padx=5, fill=BOTH)
        self.btn_exit = Button(self.frm_file, text="退出", relief=GROOVE, command=self.close)
        self.btn_exit.pack(side=RIGHT, padx=5, fill=BOTH)

        print(self.frm_file, self.btn_open)

        self.frm_edit = tk.Frame(self.t)
        self.frm_edit.grid(row=0, column=1, padx=1, sticky=W)
        self.btn_copy = Button(self.frm_edit, text="复制")
        self.btn_copy.pack(side=LEFT, padx=5, fill=BOTH, expand=1)
        self.btn_cut = Button(self.frm_edit, text="剪切")
        self.btn_cut.pack(side=LEFT, padx=5, fill=BOTH, expand=1)
        self.btn_paste = Button(self.frm_edit, text="黏贴")
        self.btn_paste.pack(side=LEFT, padx=5, fill=BOTH, expand=1)
        self.btn_find = Button(self.frm_edit, text="查询")
        self.btn_find.pack(side=LEFT, padx=5, fill=BOTH, expand=1)
        self.btn_allselect = Button(self.frm_edit, text="全选")
        self.btn_allselect.pack(side=LEFT, padx=5, fill=BOTH, expand=1)
        self.btn_font = Button(self.frm_edit, text="字体样式")
        self.btn_font.pack(side=LEFT, padx=5, fill=BOTH, expand=1)
        self.btn_color = Button(self.frm_edit, text="字体颜色")
        self.btn_color.pack(side=LEFT, padx=5, fill=BOTH, expand=1)

        self.bar = tk.Menu(self.t)

        self.filem = tk.Menu(self.bar, tearoff = 0)
        self.filem.add_separator()
        self.filem.add_command(label="新建", command=self.neweditor, accelerator="     Ctr +N")
        self.filem.bind_all("<Control-n>", self.neweditor)
        self.filem.add_separator()
        self.filem.add_command(label="打开", command=self.openfile, accelerator="     Ctr + O")
        self.filem.bind_all("<Control-o>", self.openfile)
        self.filem.add_separator()
        self.filem.add_command(label="保存", command=self.savefile, accelerator="     Ctr +S ")
        self.filem.bind_all("<Control-s>", self.savefile)
        self.filem.add_separator()
        self.filem.add_command(label="另存为", command=self.saveasfile, accelerator="     Ctr + D ")
        self.filem.bind_all("<Control-d>", self.saveasfile)

        self.filem.add_command(label="关闭", command=self.close, accelerator="     F4")
        self.filem.bind_all("<F4>", self.close)
        self.filem.add_separator()
        self.filem.add_command(label="退出", command=die, accelerator="     ESC")
        self.filem.bind_all("<Escape>", die)

        self.editm = tk.Menu(self.bar)
        self.editm.add_separator()
        self.editm.add_command(label="复制", command=self.copy, accelerator=" " * 10 + "Ctr + C")
        self.editm.bind_all("<Control-c>", self.copy)
        self.editm.add_separator()
        self.editm.add_command(label="黏贴", command=self.paste, accelerator=" " * 10 + "Ctr + V")
        self.editm.bind_all("<Control-v>", self.paste)
        self.editm.add_separator()
        self.editm.add_command(label="剪切", command=self.cut, accelerator=" " * 10 + "Ctr + X")
        self.editm.bind_all("<Control-x>", self.cut)
        self.editm.add_separator()
        self.editm.add_command(label="删除", command=self.delete_text, accelerator=" " * 10 + "Delete")
        self.editm.bind_all("<Delete>", self.delete_text)
        self.editm.add_separator()
        self.editm.add_command(label="查找", command=self.find_char, accelerator=" " * 10 + "Ctr +F")
        self.editm.bind_all("<Control-f>", self.find_char)
        self.editm.add_separator()
        self.editm.add_command(label="全选", command=self.select_char_all, accelerator=" " * 10 + "Ctr + A")
        self.editm.bind_all("<Control-a>", self.select_char_all)

        self.formm = tk.Menu(self.bar)
        self.formm.add_command(label="字体颜色", command=self.color_it, accelerator=" " * 10 + "Alt + C")
        self.formm.bind_all("<Alt-f>", self.color_it)
        self.formm.add_separator()
        self.formm.add_command(label="字体格式", command=self.font_it, accelerator=" " * 10 + "Alt + F")
        self.formm.bind_all("<Alt-f>", self.font_it)

        self.helpm = tk.Menu(self.bar)
        self.helpm.add_command(label="关于", command=about)

        self.bar.add_cascade(label="文件", menu=self.filem)
        self.bar.add_cascade(label="编辑", menu=self.editm)
        self.bar.add_cascade(label="格式", menu=self.formm)
        self.bar.add_cascade(label="帮助", menu=self.helpm)

        self.t.config(menu=self.bar)

        # self.f = tk.Frame(self.t, width = 512)
        # self.f.grid(row = 1, column=0, columnspan=3, pady=3)

        self.st = tkst.ScrolledText(self.t)
        self.st.grid(row = 2, column=0, columnspan=3, pady=3)

    def close(self, event=None):
        self.t.destroy()

    def neweditor(self, event=None):
        global root
        print(id(root), root)
        t1.append(editor(root))

    def openfile(self, event=None):
        oname = tkinter.filedialog.askopenfilename(filetypes=[("打开文件", "*.txt")])
        if oname:
            print('oname: ', oname)
            self.st.delete("1.0", tk.END)
            for line in fileinput.input(oname, openhook=fileinput.hook_encoded("utf-8")):
                self.st.insert(tk.END, line)
            self.t.title(oname)

    def savefile(self, event=None):
        print(self.t.title(), type(self.t.title()))
        if os.path.isfile(self.t.title()):
            opf = open(self.t.title(), "w", encoding='utf-8')
            opf.write(self.st.get(1.0, tk.END))
            opf.flush()
            opf.close()
        else:
            sname = tkinter.filedialog.asksaveasfilename(title="保存好你的宝宝哟", filetypes=[("保存文件", "*.txt")],
                                                       defaultextension=".txt")
            if sname:
                ofp = open(sname, "w", encoding='utf-8')
                ofp.write(self.st.get(1.0, tk.END))
                ofp.flush()
                ofp.close()
            self.t.title(sname)

    def saveasfile(self, event=None):
        sname = tkinter.filedialog.asksaveasfilename(title="保存好你的宝宝哟", filetypes=[("保存文件", "*.txt")],
                                                   defaultextension=".txt")
        if sname:
            ofp = open(sname, "w", encoding='utf-8')
            ofp.write(self.st.get(1.0, tk.END))
            ofp.flush()
            ofp.close()
            self.t.title(sname)

    def copy(self, event=None):
        print(self.st.index(tk.SEL_FIRST), self.st.index(tk.SEL_LAST))
        text = self.st.get(tk.SEL_FIRST, tk.SEL_LAST)
        print(text)
        self.st.clipboard_clear()
        self.st.clipboard_append(text)

    def paste(self, event=None):
        try:
            text = self.st.selection_get(selection="CLIPBOARD")
            self.st.insert(tk.INSERT, text)
            self.st.clipboard_clear()
        except tk.TclError:
            pass

    def cut(self, event=None):
        text = self.st.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.st.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.st.clipboard_clear()
        self.st.clipboard_append(text)

    def delete_text(self):
        self.st.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def find_char(self, event=None):
        target = simpledialog.askstring("简易文本编辑器", "寻找字符串")
        # wraplength or width
        print(self.st["width"])
        if target:
            end = self.st.index(tk.END)
            print("st.index(tk.END): ", end)
            endindex = end.split(".")
            end_line = int(endindex[0])
            end_column = int(endindex[1])
            pos_line = 1
            pos_column = 0
            length = len(target)
            while pos_line <= end_line:
                pos = str(pos_line) + "." + str(pos_column)
                where = self.st.search(target, pos, tk.END)
                if where:
                    print(where)
                    next_find_col = str(int(where.split(".")[1]) + length)
                    next_find_pos = where.split(".")[0] + "." + next_find_col
                    self.st.tag_add(tk.SEL, where, next_find_pos)
                    self.st.mark_set(tk.INSERT, next_find_pos)
                    self.st.see(tk.INSERT)
                    self.st.focus()

                    again = messagebox.askokcancel(title="继续查询么", message=where)
                    if again:
                        pos_line = int(next_find_pos.split(".")[0])
                        pos_column = int(next_find_pos.split(".")[1])
                    else:
                        aa = messagebox.showinfo(title="你终于还是放弃了我", message="你放弃了我--!")
                        print("aa: ", aa)
                        break
                else:
                    break

    def select_char_all(self, event=None):
        self.st.tag_add(tk.SEL, 1.0, tk.END)
        self.st.see(tk.INSERT)
        self.st.focus()

    def color_it(self, event=None):
        color = colorchooser.askcolor()
        print(color)
        self.st["foreground"] = color[1]

    def font_it(self, event=None):
        self.t_font = tk.Toplevel()
        self.t_font.title("字体选择面板")
        self.label_size = Label(self.t_font, text="字体大小")
        self.label_font = Label(self.t_font, text="字体类型")
        self.label_shape = Label(self.t_font, text="字体形状")
        self.label_weight = Label(self.t_font, text="字体粗细")
        self.label_size.grid(row=0, column=0, padx=30)
        self.label_font.grid(row=0, column=2, padx=30)
        self.label_shape.grid(row=0, column=4, padx=30)
        self.label_weight.grid(row=0, column=6, padx=30)

        self.scroll_size = Scrollbar(self.t_font)
        self.scroll_size.grid(row=1, column=1, stick=NS)
        self.scroll_font = Scrollbar(self.t_font)
        self.scroll_font.grid(row=1, column=3, stick=NS)
        self.scroll_shape = Scrollbar(self.t_font)
        self.scroll_shape.grid(row=1, column=5, stick=NS)
        self.scroll_weight = Scrollbar(self.t_font)
        self.scroll_weight.grid(row=1, column=7, stick=NS)

        list_var_size = StringVar()
        list_var_font = StringVar()
        list_var_shape = StringVar()
        list_var_weight = StringVar()

        self.list_size = Listbox(self.t_font, selectmode=BROWSE, listvariable=list_var_size, exportselection=0)
        self.list_size.grid(row=1, column=0, padx=4)
        list_size_item = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        for item in list_size_item:
            self.list_size.insert(0, item)
        self.list_size.bind("<ButtonRelease-1>", self.change_size)

        self.list_font = Listbox(self.t_font, selectmode=BROWSE, listvariable=list_var_font, exportselection=0)
        self.list_font.grid(row=1, column=2, padx=4)
        list_font_item = ["\"Arial\"", "\"Arial Baltic\"", "\"Arial Black\"", "\"Arial CE\"", "\"Arial CYR\"",
                          "\"Arial Greek\"", "\"Arial Narrow\"",
                          "\"Arial TUR\"", "\"Baiduan Number\"", "\"Batang,BatangChe\""]
        for item in list_font_item:
            self.list_font.insert(0, item)
        self.list_font.bind("<ButtonRelease-1>", self.change_font)

        self.list_shape = Listbox(self.t_font, selectmode=BROWSE, listvariable=list_var_shape, exportselection=0)
        self.list_shape.grid(row=1, column=4, padx=4)
        list_shape_item = ["italic", "roman"]
        for item in list_shape_item:
            self.list_shape.insert(0, item)
        self.list_shape.bind("<ButtonRelease-1>", self.change_shape)

        self.list_weight = Listbox(self.t_font, selectmode=BROWSE, listvariable=list_var_weight, exportselection=0)
        self.list_weight.grid(row=1, column=6, padx=4)
        list_weight_item = ["bold", "normal"]
        for item in list_weight_item:
            self.list_weight.insert(0, item)
        self.list_weight.bind("<ButtonRelease-1>", self.change_weight)

        self.labFra_display = LabelFrame(self.t_font, text="字体样式演示区域")
        self.labFra_display.grid(row=2, column=0, pady=4)
        self.lab_display = Label(self.labFra_display, text="我在这里", font = "TkDefaultFont")
        self.lab_display.pack()
        print(tk.font.Font(font = 'TkDefaultFont').configure())

        self.btn_ok = Button(self.t_font, text="确定", width=10, height=2, command=self.change)
        self.btn_ok.grid(row=2, column=2, pady=4)
        self.btn_cancel = Button(self.t_font, width=10, height=2, text="取消", command=self.exit_subwindow)
        self.btn_cancel.grid(row=2, column=4, pady=4)

    def change_size(self, event):
        tk.customFont = font.Font(family="Helvetica", size=12, weight="normal", slant="roman", underline=0)
        size = tk.customFont["size"]
        tk.customFont.configure(size=self.list_size.get(self.list_size.curselection()))
        self.st.config(font=tk.customFont)
        self.size_count = 1
        pass

    def change_font(self, event):
        tk.customFont = font.Font(family="Helvetica", size=12, weight="normal", slant="roman", underline=0)
        family = tk.customFont["family"]
        tk.customFont.configure(family=self.list_font.get(self.list_font.curselection()))
        self.st.config(font=tk.customFont)
        self.font_count = 1
        pass

    def change_shape(self, event):
        tk.customFont = font.Font(family="Helvetica", size=12, weight="normal", slant="roman", underline=0)
        slant = tk.customFont["slant"]
        tk.customFont.configure(slant=self.list_shape.get(self.list_shape.curselection()))
        self.st.config(font=tk.customFont)
        self.shape_count = 1
        pass

    def change_weight(self, event):
        tk.customFont = font.Font(family="Helvetica", size=12, weight="normal", slant="roman", underline=0)
        weight = tk.customFont["weight"]
        tk.customFont.configure(weight=self.list_weight.get(self.list_weight.curselection()))
        self.st.config(font=tk.customFont)
        self.shape_count = 1

    def change(self, event=None):
        ld_font = tk.font.Font(font=self.lab_display["font"]).configure()
        lsize = ld_font['size']
        lfont = ld_font['family']
        lweight = ld_font['weight']
        lslant = ld_font['slant']
        try:
            lsize, lfont, lslant, lweight = self.list_size.get(self.list_size.curselection()), self.list_font.get(self.list_font.curselection()), self.list_shape.get(self.list_shape.curselection()), self.list_weight.get(self.list_weight.curselection())
            self.testFont = font.Font(family=self.list_font.get(self.list_font.curselection()), size=self.list_size.get(self.list_size.curselection()), weight=self.list_weight.get(self.list_weight.curselection()), slant=self.list_shape.get(self.list_shape.curselection()), underline=0)
            self.lab_display["font"] = self.testFont
            # self.lab_display.config(font = self.testFont)
            print(self.testFont.configure())
            print(ld_font)
            # self.lab_display["font"] = (self.list_size.get(self.list_size.curselection()))
            # self.lab_display["font"] = (self.list_font.get(self.list_font.curselection()))
            # self.lab_display["font"] = (self.list_shape.get(self.list_shape.curselection()))
            # self.lab_display["font"] = (self.list_weight.get(self.list_weight.curselection()))
        except tk._tkinter.TclError as e:
            print(repr(e))
            self.testFont = font.Font(family = lfont, size = lsize, weight = lweight, slant = lslant, underline=0)
            self.lab_display["font"] = self.testFont
            pass

    def exit_subwindow(self):
        self.t_font.destroy()


if __name__ == "__main__":
    root = None
    t1.append(editor(root))
    root = t1[0].t
    print(id(root), root)
    root.mainloop()
