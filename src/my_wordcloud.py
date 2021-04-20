# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: wordcloud
@date: 2021-04-05 22:34
@desc:
"""
import re
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from src.conf_win import *

# 词云形状图片
WC_MASK_IMG = DATA_ROOT_PATH + "wawa.jpg"
# 词云图片
WC_IMG = DATA_ROOT_PATH + 'wawa1.jpg'
# 词云字体
WC_FONT_PATH = 'C:\\Windows\\Fonts\\' + 'simsun.ttc'


def get_word_list(comment_path='D:\ACM_Code_Lib\other\爬虫\jd_comment.txt'):
    wordlist = None
    with open(comment_path, 'r', encoding='utf-8') as file :
        comment_txt = file.read()
        wordlist = jieba.lcut(comment_txt, cut_all=True)
    return wordlist


def get_cut_word(wordlist):
    new_word_list = []
    for word in wordlist:
        word = word.replace('的', '')
        word = word.replace('了', '')
        word = word.replace('也', '')
        if word not in ['：', '，', '；', '。', '？', '??', '?'] :
            new_word_list.append(word)
    wl = " ".join(new_word_list)
    print(wl)
    return wl


def create_word_cloud(my_words=None):
    # https://pig66.blog.csdn.net/article/details/95198791
    # 设置词云形状图片
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    wc = WordCloud(background_color="white", max_words=2000, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, font_path=WC_FONT_PATH)
    # 生成词云
    word_cloud = wc.generate(get_cut_word(my_words))
    # word_cloud.to_file(WC_IMG)
    # 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    # plt.figure()
    plt.show()


if __name__ == '__main__':
    print('hello')
    my_words = get_word_list()
    create_word_cloud(my_words)
