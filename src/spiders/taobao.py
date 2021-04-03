# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: taobao
@date: 2021-03-17 22:00
@desc:
"""

import requests
import os
import re
from bs4 import BeautifulSoup
import time
import json
import csv
import hashlib
import codecs

from src.conf_win import *
def getMD5(s) :
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()
def bytesToStr(bs) :
    # s = "%E7%AC%94%E8%AE%B0%E6%9C%AC" #笔记本
    # s = s.replace('%', '\\x')
    # '\xE7\xAC\x94\xE8\xAE\xB0\xE6\x9C\xAC'
    # ss = codecs.escape_decode(s, 'hex-escape')[0]
    # print(ss.decode('utf-8'))
    bs = bs.replace('%', '\\x')
    bss = codecs.escape_decode(bs, 'hex-escape')[0]
    bss = bss.decode('utf-8')
    return bss
# 爬取图片
def downPic(url = "https://g-search3.alicdn.com/img/bao/uploaded/i4/i1/3063905773/O1CN01qXLQ231sW59J818ds_!!0-item_pic.jpg"):
    root = DATA_ROOT_PATH
    path = root + url.split('/')[-1]  # 新建文件名为root路径之后加上地址最后以“/”分割的部分
    path = path.replace('jpg', 'png')
    try:
        if not os.path.exists(root):  # 判断括号里的文件是否存在的意思，括号内的可以是文件路径
            os.mkdir(root)  # 不存在则创建目录
        if not os.path.exists(path):  # 文件不存在则开始爬取保存
            headers = {
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                "referer": "https://s.taobao.com/",
                'cookie': r'cookie2=17b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; _tb_token_=57b73e781399b; _samesite_flag_=true; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; thw=cn; hng=GLOBAL|zh-CN|USD|999; alitrackid=www.taobao.com; cna=ghItGJbpnRQCAd73JQuwqdcQ; sgcookie=E100NOFdbUuG0giKiCqGPLgbiPtWrrW/OFH3Z9DCpT97yY5fs/u8mDnDG+D89/SoRX1DpyqxtIWGfmWRUoM1Ls8Sxw==; uc3=nk2=3Rj2a800wpk=&vt3=F8dCuASkA7t1hb70TZk=&lg2=VT5L2FSpMGV7TQ==&id2=UU6nRCwmzNLA9Q==; csg=b906308a; lgc=\u9152\u75AF\u72FClp; dnk=\u9152\u75AF\u72FClp; skt=2ebe208bc2b09887; existShop=MTYxMzgwMTMyNQ==; uc4=nk4=0@35PWOqVA3il14ddukkZfRtNILw==&id4=0@U2xqIFo4BlQVQlqi37APKGI6gPxX; tracknick=\u9152\u75AF\u72FClp; _cc_=WqG3DMC9EA==; lastalitrackid=login.taobao.com; mt=ci=-1_0; xlly_s=1; JSESSIONID=9E44C71750433AA69BF8FD5932CC3D97; uc1=cookie16=U+GCWk/74Mx5tgzv3dWpnhjPaQ==&cookie14=Uoe1hgKdxnFfYQ==&cookie21=VT5L2FSpczFp&pas=0&existShop=false; tfstk=cnrhBbXvpyuIjWuglMiQ3I9kczbOZxbEOurablptB1lj72qNi4Lwuw9dIXF32U1..; l=eBaGSPBgOnge4bd2BOfZnurza77TIIRAguPzaNbMiOCPOF1p5bBOW6gi3m89CnGVh6yeR3zWDma_BeYBqCvan5U62j-la6Hmn; isg=BCMjF3-LRzHIczSS9_XDuB2QsmfNGLda-Tn12FWAcwL5lEO23eiRqiDOimSaNA9S'
            }
            r = requests.get(url, headers=headers)
            with open(path, 'wb') as f:
                f.write(r.content)#保存为二进制格式
                f.close()
                print("文件保存成功")
        else:
            print("文件已经存在")
    except:
        print("爬取失败")
    print(path.split('\\')[-1])
    return path.split('\\')[-1]


def getTBHTMLText(url, dSearch, ip = 0):
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        "referer": "https://s.taobao.com/",
        'cookie': r'cookie2=17b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; _tb_token_=57b73e781399b; _samesite_flag_=true; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; thw=cn; hng=GLOBAL|zh-CN|USD|999; alitrackid=www.taobao.com; cna=ghItGJbpnRQCAd73JQuwqdcQ; sgcookie=E100NOFdbUuG0giKiCqGPLgbiPtWrrW/OFH3Z9DCpT97yY5fs/u8mDnDG+D89/SoRX1DpyqxtIWGfmWRUoM1Ls8Sxw==; uc3=nk2=3Rj2a800wpk=&vt3=F8dCuASkA7t1hb70TZk=&lg2=VT5L2FSpMGV7TQ==&id2=UU6nRCwmzNLA9Q==; csg=b906308a; lgc=\u9152\u75AF\u72FClp; dnk=\u9152\u75AF\u72FClp; skt=2ebe208bc2b09887; existShop=MTYxMzgwMTMyNQ==; uc4=nk4=0@35PWOqVA3il14ddukkZfRtNILw==&id4=0@U2xqIFo4BlQVQlqi37APKGI6gPxX; tracknick=\u9152\u75AF\u72FClp; _cc_=WqG3DMC9EA==; lastalitrackid=login.taobao.com; mt=ci=-1_0; xlly_s=1; JSESSIONID=9E44C71750433AA69BF8FD5932CC3D97; uc1=cookie16=U+GCWk/74Mx5tgzv3dWpnhjPaQ==&cookie14=Uoe1hgKdxnFfYQ==&cookie21=VT5L2FSpczFp&pas=0&existShop=false; tfstk=cnrhBbXvpyuIjWuglMiQ3I9kczbOZxbEOurablptB1lj72qNi4Lwuw9dIXF32U1..; l=eBaGSPBgOnge4bd2BOfZnurza77TIIRAguPzaNbMiOCPOF1p5bBOW6gi3m89CnGVh6yeR3zWDma_BeYBqCvan5U62j-la6Hmn; isg=BCMjF3-LRzHIczSS9_XDuB2QsmfNGLda-Tn12FWAcwL5lEO23eiRqiDOimSaNA9S'
        }
    cookie_dict = {
        'cookie': r'cookie2=17b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; _tb_token_=57b73e781399b; _samesite_flag_=true; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; thw=cn; hng=GLOBAL|zh-CN|USD|999; alitrackid=www.taobao.com; xlly_s=1; lastalitrackid=www.taobao.com; mt=ci=0_0; cna=ghItGJbpnRQCAd73JQuwqdcQ; _m_h5_tk=258f615938a9fffd610ad420c8b6c038_1612187188554; _m_h5_tk_enc=adf4cac53165bdf2f886f6d44e09196f; JSESSIONID=CE1405197D4F86041BF290FE23160A41; l=eBaGSPBgOnge41TyBOfZhurza77TGIRfguPzaNbMiOCPOa1p5LY5W6MkobT9CnGVH62MR38KdX68B4TWsydVtSQ5uM80AC1Z3dC..; isg=BHR0od8YqLBu6QNHDIAcZcY9RTLmTZg3W5DG-A7Vc_-LeRXDNlkixwc7-bGhgdCP; tfstk=cKDPBufYZLpyLFyB68wFPQULnSPRZqa35traZXUZ4qH2xlPlik7Lmn_L0kz9n7f..; sgcookie=E1005JQj9/1cnplokvGtldOlk/RurBNfOYmf7En3q+qG0/3ENfVuDTUmdPd6ErRlZLt677g5UqtOmRtO/K7M1YbXjw==; unb=2665991651; uc1=cookie21=W5iHLLyFe3xm&cookie14=Uoe1gBpbBvXwQw==&pas=0&cookie16=W5iHLLyFPlMGbLDwA+dvAGZqLg==&existShop=false&cookie15=W5iHLLyFOGW7aA==; uc3=lg2=V32FPkk/w0dUvg==&nk2=3Rj2a800wpk=&vt3=F8dCuAbxCWMMXsmH758=&id2=UU6nRCwmzNLA9Q==; csg=339090b8; lgc=\u9152\u75AF\u72FClp; cookie17=UU6nRCwmzNLA9Q==; dnk=\u9152\u75AF\u72FClp; skt=3937ef62536f1fb6; existShop=MTYxMjE3ODU2OQ==; uc4=nk4=0@35PWOqVA3il14dduk5b6A0kRbw==&id4=0@U2xqIFo4BlQVQlqi37AO9HfxSNjE; tracknick=\u9152\u75AF\u72FClp; _cc_=VFC/uZ9ajQ==; _l_g_=Ug==; sg=p17; _nk_=\u9152\u75AF\u72FClp; cookie1=U7HwN3kxiXT7IEAcQ8eG3KkqRoGDI3P9LO+TJyuRgyU='}
    try:
        reqS = requests.Session()
        # reqS.cookies.update(cookie_dict)

        cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
        reqS.cookies = cookies
        print(cookies)
        '''
        <RequestsCookieJar[<Cookie cookie=cookie2=17b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; _tb_token_=57b73e781399b; _samesite_flag_=true; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; thw=cn; hng=GLOBAL|zh-CN|USD|999; alitrackid=www.taobao.com; xlly_s=1; lastalitrackid=www.taobao.com; mt=ci=0_0; cna=ghItGJbpnRQCAd73JQuwqdcQ; _m_h5_tk=258f615938a9fffd610ad420c8b6c038_1612187188554; _m_h5_tk_enc=adf4cac53165bdf2f886f6d44e09196f; JSESSIONID=CE1405197D4F86041BF290FE23160A41; l=eBaGSPBgOnge41TyBOfZhurza77TGIRfguPzaNbMiOCPOa1p5LY5W6MkobT9CnGVH62MR38KdX68B4TWsydVtSQ5uM80AC1Z3dC..; isg=BHR0od8YqLBu6QNHDIAcZcY9RTLmTZg3W5DG-A7Vc_-LeRXDNlkixwc7-bGhgdCP; tfstk=cKDPBufYZLpyLFyB68wFPQULnSPRZqa35traZXUZ4qH2xlPlik7Lmn_L0kz9n7f..; sgcookie=E1005JQj9/1cnplokvGtldOlk/RurBNfOYmf7En3q+qG0/3ENfVuDTUmdPd6ErRlZLt677g5UqtOmRtO/K7M1YbXjw==; unb=2665991651; uc1=cookie21=W5iHLLyFe3xm&cookie14=Uoe1gBpbBvXwQw==&pas=0&cookie16=W5iHLLyFPlMGbLDwA+dvAGZqLg==&existShop=false&cookie15=W5iHLLyFOGW7aA==; uc3=lg2=V32FPkk/w0dUvg==&nk2=3Rj2a800wpk=&vt3=F8dCuAbxCWMMXsmH758=&id2=UU6nRCwmzNLA9Q==; csg=339090b8; lgc=\u9152\u75AF\u72FClp; cookie17=UU6nRCwmzNLA9Q==; dnk=\u9152\u75AF\u72FClp; skt=3937ef62536f1fb6; existShop=MTYxMjE3ODU2OQ==; uc4=nk4=0@35PWOqVA3il14dduk5b6A0kRbw==&id4=0@U2xqIFo4BlQVQlqi37AO9HfxSNjE; tracknick=\u9152\u75AF\u72FClp; _cc_=VFC/uZ9ajQ==; _l_g_=Ug==; sg=p17; _nk_=\u9152\u75AF\u72FClp; cookie1=U7HwN3kxiXT7IEAcQ8eG3KkqRoGDI3P9LO+TJyuRgyU= for />]>
        '''
        if ip == 0:
            r = reqS.get(url, timeout=3, headers=headers, params=dSearch)
        else:
            r = reqS.get(url, timeout=3, headers=headers)
        print(r.status_code, r.encoding, r.apparent_encoding)
        print(r.request.url)
        r.raise_for_status()  # 如果状态不是200 引发http error异常
        r.encoding = r.apparent_encoding
        print(r.request.headers)
        print(r.headers)
        # print(r.request.headers['cookie'])
        return r.text
    except:
        print("获取淘宝URL页面失败")
        return "获取淘宝URL页面失败"

def parsePage(ilt, html, cnt):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        urllt = re.findall(r'\"detail_url\"\:\".*?\"', html)
        shoplt = re.findall(r'\"nick\"\:\".*?\"', html)
        msaleslt = re.findall(r'\"view_sales\"\:\".*?\"', html)
        pic_urllt = re.findall(r'\"pic_url\"\:\".*?\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(":")[1])
            title = eval(tlt[i].split(":")[1])
            urllt[i] = re.sub(r'https:', "", urllt[i])
            urlLink = eval(urllt[i].split(":")[1])
            urlLink = urlLink.encode('utf-8').decode('utf-8')
            if len(urlLink) > 120 or urlLink[2] != 'd':
                continue
            urlLink = urlLink.split('&')[0]
            shop_name = eval(shoplt[i].split(":")[1])
            pic_url = eval(pic_urllt[i].split(":")[1])

            def py_to_num(s):
                if s[-1] == '+':
                    s = s[:-1]
                if s[-1] == '万':
                    return int(float(s[:-1]) * 10000)
                else:
                    return int(s)

            msales = msaleslt[i].split(":")[1].strip()[1:-4]
            msales = py_to_num(msales)
            itemId = re.search(r'id\=(\d+)', urlLink).group(1)
            itemId = 'TB' + itemId
            # print("itemId:", itemId)
            ilt.append([itemId, price, urlLink, title, shop_name, msales, pic_url])
            if len(ilt) >= cnt:
                break
    except:
        print("解析淘宝HTML内容失败")

def printGoodsList(ilt, num = 20):
    tplt = "{:4}\t{:8}\t{:8}\t{:16}\t{:16}\t{:16}\t{:8}\t{:16}"
    print(tplt.format("序号","goodID","价格","链接","商品名称", "店铺", "月销量", "图片url"))
    count = 0
    for g in ilt:
        count = count+1
        print(tplt.format(count, g[0], g[1], g[2], g[3], g[4], g[5], g[6]))
        if count == num:
            break
    print("")
def getTaobaoProd(qName = '手机', cnt = 1):
    url = "https://s.taobao.com/search"
    dSearch = {'q': qName, 's': '0',
    'imgfile':'',
    'commend':'all','ssid':'s5-e','search_type':'item','sourceId':'tb.index','spm':'a21bo.2017.201856-taobao-item.1','ie':'utf8','initiative_id':'tbindexz_20170306'}
    infoList = []
    for i in range(2):
        time.sleep(1)
        dSearch['s'] = str(44 * i)
        try:
            with open("D:/iTaobaoSJ.html", "r", encoding='utf-8') as f:
                html = f.read()
                # html = getTBHTMLText(url, dSearch)
                parsePage(infoList, html, cnt)
                # if i == 0:
                #     with open("D:/iTaobaoSJ.html", "w", encoding='utf-8') as f:
                #         f.write(html)
            if len(infoList) >= cnt:
                break
        except:
            print("获取淘宝商品产生异常")
    return infoList

def getNewPrice(url, op):
    html = getTBHTMLText(url, None, 1)
    plt = re.findall(r'\"price\"\:\"[\d\.]*\"', html)
    try:
        return float(eval(plt[0].split(":")[1]))
    except:
        return op










def printComments(ilist):
    cnt = 0
    for x in ilist:
        print(cnt, x[0], x[1], x[2], x[3])
        cnt += 1
    print("")
# https://rate.tmall.com/list_detail_rate.htm?itemId=629748003807&spuId=1846540591&sellerId=268451883&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvl9vnvPOvUpCkvvvvvjiWPLqZ1jEHRLFhAjthPmPhsjYbPLF9ljn2n2SOQjiRROvCvCLwjUYJDrMwznAa9lS5FMsJzVD448QCvvyvmCQmFgGvbvTVvpvhvvpvv29Cvvpvvvvv29hvCvvvMMGvvpvVvvpvvhCvKvhv8vvvvvCvpvvtvvmm7ZCvmR%2BvvvWvphvW9pvv9DDvpvACvvmm7ZCv2UVUvpvVmvvC9j3vuvhvmvvv9b%2B1eAw0mvhvLvCrpQvjn%2BkQ0f06WeCpqU0HsfUpwyjIAXcBKFyK2ixrQj7JVVQHYnFhAEI7nDeDyO2vSdtIjbmYSW94P5CXqU5EDfmlJ1kHsX7veEkevpvhvvmv9uQCvvyvmH9mKdIv8EQgvpvhvvvvvv%3D%3D&needFold=0&_ksTS=1612519758221_703&callback=jsonp704
def reqProdComments(url, csv_writer, num = 10):
    if num > 20: num = 20
    if num <= 0: num = 10
    result = []
    head = {
        "referer": "https://detail.tmall.com/item.htm",
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'cookie': r"cookie2=17b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; _tb_token_=57b73e781399b; _samesite_flag_=true; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; thw=cn; hng=GLOBAL|zh-CN|USD|999; alitrackid=www.taobao.com; xlly_s=1; lastalitrackid=www.taobao.com; mt=ci=0_0; cna=ghItGJbpnRQCAd73JQuwqdcQ; _m_h5_tk=258f615938a9fffd610ad420c8b6c038_1612187188554; _m_h5_tk_enc=adf4cac53165bdf2f886f6d44e09196f; JSESSIONID=CE1405197D4F86041BF290FE23160A41; l=eBaGSPBgOnge41TyBOfZhurza77TGIRfguPzaNbMiOCPOa1p5LY5W6MkobT9CnGVH62MR38KdX68B4TWsydVtSQ5uM80AC1Z3dC..; isg=BHR0od8YqLBu6QNHDIAcZcY9RTLmTZg3W5DG-A7Vc_-LeRXDNlkixwc7-bGhgdCP; tfstk=cKDPBufYZLpyLFyB68wFPQULnSPRZqa35traZXUZ4qH2xlPlik7Lmn_L0kz9n7f..; sgcookie=E1005JQj9/1cnplokvGtldOlk/RurBNfOYmf7En3q+qG0/3ENfVuDTUmdPd6ErRlZLt677g5UqtOmRtO/K7M1YbXjw==; unb=2665991651; uc1=cookie21=W5iHLLyFe3xm&cookie14=Uoe1gBpbBvXwQw==&pas=0&cookie16=W5iHLLyFPlMGbLDwA+dvAGZqLg==&existShop=false&cookie15=W5iHLLyFOGW7aA==; uc3=lg2=V32FPkk/w0dUvg==&nk2=3Rj2a800wpk=&vt3=F8dCuAbxCWMMXsmH758=&id2=UU6nRCwmzNLA9Q==; csg=339090b8; lgc=\u9152\u75AF\u72FClp; cookie17=UU6nRCwmzNLA9Q==; dnk=\u9152\u75AF\u72FClp; skt=3937ef62536f1fb6; existShop=MTYxMjE3ODU2OQ==; uc4=nk4=0@35PWOqVA3il14dduk5b6A0kRbw==&id4=0@U2xqIFo4BlQVQlqi37AO9HfxSNjE; tracknick=\u9152\u75AF\u72FClp; _cc_=VFC/uZ9ajQ==; _l_g_=Ug==; sg=p17; _nk_=\u9152\u75AF\u72FClp; cookie1=U7HwN3kxiXT7IEAcQ8eG3KkqRoGDI3P9LO+TJyuRgyU="
    }
    itemId = re.search(r'id\=(\d+)', url).group(1)
    print("itemId:", itemId)
    sellerId = "268451883"
    try:
        url = "https:" + url
        r = requests.get(url, timeout=3, headers=head)
        r.raise_for_status()
        sellerId = re.search(r'sellerId\:\"(\d+)\"', r.text).group(1)
        print("sellerId: ", sellerId)
    except:
        print("获取淘宝评论出现bug1")
        return result
    dSearch = {
        "itemId":itemId,
        "sellerId": "196993935",
        "currentPage":"1",
        "callback": "jsonp704"
    }
    url = 'https://rate.tmall.com/list_detail_rate.htm'
    attris = ["displayUserNick", "auctionSku", "rateDate", "rateContent"]
    try:
        while len(result) < num:
            r = requests.get(url, timeout=3, headers=head, params = dSearch)
            r.raise_for_status()
            if r.text == "":
                break
            rtext = r.text[11:-1]
            # print(rtext)
            rtjs = json.loads(rtext)
            comments = rtjs["rateDetail"]["rateList"]
            for comment in comments:
                tmp = []
                for attri in attris:
                    if(attri == 'rateContent'):
                        # comment[attri] = html.unescape(comment[attri]).replace(r'\n', ' ')
                        comment[attri] = comment[attri].replace('\n', ' ')
                    tmp.append(comment[attri])
                result.append(tmp)
                csv_writer.writerow(tmp)
                if len(result) == num:
                    break
            dSearch['currentPage'] = str(int(dSearch['currentPage']) + 1)
    except:
        print("获取淘宝评论出现bug2")
    return result

def getTBProdComments(url):
    time.sleep(1)
    ilist = []
    with open('tbData.csv', 'a+', newline='', encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerow(("用户昵称", "商品型号", "评论时间", "评论内容"))
        ilist = reqProdComments(url, writer)
    printComments(ilist)