# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: taobao
@date: 2021-03-17 22:00
@desc:
"""
from functools import wraps
import requests
import os
import re
from bs4 import BeautifulSoup
import time
import json
import csv
import random
from src.conf_win import *


tb_cookie = r'cookie2=17b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; _tb_token_=57b73e781399b; _samesite_flag_=true; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; thw=cn; hng=GLOBAL|zh-CN|USD|999; alitrackid=www.taobao.com; cna=ghItGJbpnRQCAd73JQuwqdcQ; dnk=\u9152\u75AF\u72FClp; tracknick=\u9152\u75AF\u72FClp; _cc_=WqG3DMC9EA==; _uab_collina=161768533207166644258734; _m_h5_tk=3b919bf24789a06013f058698392078f_1619435602621; _m_h5_tk_enc=f1fc0ae1227bbd5664ee4b62a1995df6; xlly_s=1; sgcookie=E100p5Ci4wiEDo0AaBvjLO3gOnvOiSwtqawP6sKWQPZOTGGrEYI93WxxIhvw5UR8PXKFtwrE9dZb6tkNHQfHTdFSyg==; unb=2665991651; uc3=nk2=3Rj2a800wpk=&lg2=WqG3DMC9VAQiUQ==&id2=UU6nRCwmzNLA9Q==&vt3=F8dCuwlHfpGnFA8EOl0=; csg=686e847f; lgc=\u9152\u75AF\u72FClp; cookie17=UU6nRCwmzNLA9Q==; skt=6a618d9371376c20; existShop=MTYxOTQyODgxMw==; uc4=id4=0@U2xqIFo4BlQVQlqi37AF6RfgnbLU&nk4=0@35PWOqVA3il14ddumIOz6n16uQ==; _l_g_=Ug==; sg=p17; _nk_=\u9152\u75AF\u72FClp; cookie1=U7HwN3kxiXT7IEAcQ8eG3KkqRoGDI3P9LO+TJyuRgyU=; JSESSIONID=63E8CFB3B1B653044EBF3B5A34E8A7D6; lastalitrackid=login.taobao.com; mt=ci=24_1; uc1=pas=0&cookie21=WqG3DMC9FxUx&existShop=false&cookie16=U+GCWk/74Mx5tgzv3dWpnhjPaQ==&cookie14=Uoe1i6vj5YWaGw==&cookie15=UIHiLt3xD8xYTw==; isg=BJSUR7yliMEv0CMnbCB8BaZdZdIG7bjX8oRCTS50GZ-iGTZjVv5zZwLbHRGB5vAv; l=eBaGSPBgOnge47DtBO5ahurza77tyIObz1PzaNbMiInca6Od1FgBpNCCaj2pRdtjgtfAYetzPnnb5RhJ7Mzdg2HvCbKrCyCk6xJ6-; tfstk=co-1BAmuG5V_-Su4bdMU7dgvNaSRZghCKV19CUEIES5LPtJ1itqPN9yMoWqdy91..'
tb_cm_cookie = r'dnk=\u9152\u75AF\u72FClp; tracknick=\u9152\u75AF\u72FClp; lid=%BE%C6%B7%E8%C0%C7lp; lgc=\u9152\u75AF\u72FClp; cookie2=17b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; _tb_token_=57b73e781399b; cna=ghItGJbpnRQCAd73JQuwqdcQ; uc1=cookie16=V32FPkk/xXMk5UvIbNtImtMfJQ==&existShop=false&cookie14=Uoe1gBpZqGHGQg==&cookie15=VFC/uZ9ayeYq2g==&cookie21=WqG3DMC9FxUx&pas=0; uc3=lg2=U+GCWk/75gdr5Q==&id2=UU6nRCwmzNLA9Q==&nk2=3Rj2a800wpk=&vt3=F8dCuAbxCoj4v7atgv8=; uc4=nk4=0@35PWOqVA3il14dduk5b4ZJJJiw==&id4=0@U2xqIFo4BlQVQlqi37AO9HXTIQFc; sgcookie=E100WCK/GES0f1rWEWqgef+IoX8ChYTi9mK5iueuasqbLeyLH5lWoq4meqqwtyvqCrbG7oFJsFY0G0sWYP2HEwZQHA==; csg=d97e4d29; sm4=430100; csa=0_0_0.0; xlly_s=1; x5sec=7b22726174656d616e616765723b32223a226438613930393335306131323635326164313638356164666630663834393564434a36716d6f5147454b66542f645443317676464b44447475662f632f762f2f2f2f3842227d; l=eBOiGEpqjNZKyomwBO5alurza77TCIOb81PzaNbMiInca661aE_84NCCaxv9udtjgtCbpeKzPnnb5RHH8wzdgZqhuJ1REpZabxvO.; isg=BBMTSWtRd7zE2Tt5O5oYUXqlopc9yKeKacnl6MUxBjJ4RDLmTJnX2inSerQqY_-C; tfstk=cfdlBPgTyLW7LOXDCb1Wysq4zgKhZCHPVBR2gBWZdBvAFMRViwe4QYa-ogKk9J1..'

def downPic(url="https://g-search3.alicdn.com/img/bao/uploaded/i4/i1/3063905773/O1CN01qXLQ231sW59J818ds_!!0-item_pic.jpg"):
    """
    爬取图片
    :param url:
    :return:
    """
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
                'cookie': tb_cookie
            }
            r = requests.get(url, headers=headers, timeout=0.7)
            with open(path, 'wb') as f:
                # 保存为二进制格式
                f.write(r.content)
                f.close()
                print("文件保存成功")
        else:
            print("文件已经存在")
    except:
        print("爬取失败")
    print(path.split('\\')[-1])
    return path.split('\\')[-1]


def getTBHTMLText(url, dSearch, ip=0):
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        "referer": "https://s.taobao.com/",
        'cookie': tb_cookie
    }
    cookie_dict = {
        'cookie': tb_cookie
    }
    try:
        reqS = requests.Session()
        # reqS.cookies.update(cookie_dict)

        cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
        reqS.cookies = cookies
        print(cookies)
        '''
        <RequestsCookieJar[<Cookie cookie=7b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; _tb_token_=57b73e781399b; _samesite_flag_=true; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; thw=cn; hng=GLOBAL|zh-CN|USD|999; alitrackid=www.taobao.com; xlly_s=1; lastalitrackid=www.taobao.com; mt=ci=0_0; cna=ghItGJbpnRQCAd73JQuwqdcQ; _m_h5_tk=258f615938a9fffd610ad420c8b6c038_1612187188554; _m_h5_tk_enc=adf4cac53165bdf2f886f6d44e09196f; JSESSIONID=CE1405197D4F86041BF290FE23160A41; l=eBaGSPBgOnge41TyBOfZhurza77TGIRfguPzaNbMiOCPOa1p5LY5W6MkobT9CnGVH62MR38KdX68B4TWsydVtSQ5uM80AC1Z3dC..; isg=BHR0od8YqLBu6QNHDIAcZcY9RTLmTZg3W5DG-A7Vc_-LeRXDNlkixwc7-bGhgdCP; tfstk=cKDPBufYZLpyLFyB68wFPQULnSPRZqa35traZXUZ4qH2xlPlik7Lmn_L0kz9n7f..; sgcookie=E1005JQj9/1cnplokvGtldOlk/RurBNfOYmf7En3q+qG0/3ENfVuDTUmdPd6ErRlZLt677g5UqtOmRtO/K7M1YbXjw==; unb=2665991651; uc1=cookie21=W5iHLLyFe3xm&cookie14=Uoe1gBpbBvXwQw==&pas=0&cookie16=W5iHLLyFPlMGbLDwA+dvAGZqLg==&existShop=false&cookie15=W5iHLLyFOGW7aA==; uc3=lg2=V32FPkk/w0dUvg==&nk2=3Rj2a800wpk=&vt3=F8dCuAbxCWMMXsmH758=&id2=UU6nRCwmzNLA9Q==; csg=339090b8; lgc=\u9152\u75AF\u72FClp; cookie17=UU6nRCwmzNLA9Q==; dnk=\u9152\u75AF\u72FClp; skt=3937ef62536f1fb6; existShop=MTYxMjE3ODU2OQ==; uc4=nk4=0@35PWOqVA3il14dduk5b6A0kRbw==&id4=0@U2xqIFo4BlQVQlqi37AO9HfxSNjE; tracknick=\u9152\u75AF\u72FClp; _cc_=VFC/uZ9ajQ==; _l_g_=Ug==; sg=p17; _nk_=\u9152\u75AF\u72FClp; cookie1=U7HwN3kxiXT7IEAcQ8eG3KkqRoGDI3P9LO+TJyuRgyU= for />]>
        '''
        if ip == 0:
            r = reqS.get(url, timeout=0.7, headers=headers, params=dSearch)
        else:
            r = reqS.get(url, timeout=1, headers=headers)
        print(r.status_code, r.encoding, r.apparent_encoding)
        print(r.request.url)
        r.raise_for_status()  # 如果状态不是200 引发http error异常
        r.encoding = r.apparent_encoding
        print(r.request.headers)
        print(r.headers)
        # print(r.request.headers['cookie'])
        return r.text
    except Exception as e:
        print(e)
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
            urlLink = urlLink.split('&')[0][2:]
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
            ilt.append([itemId, title, price, msales, shop_name, urlLink, pic_url])
            if len(ilt) >= cnt:
                break
    except:
        print("解析淘宝HTML内容失败")


def printGoodsList(ilt, num=5):
    tplt = "{:4}\t{:8}\t{:8}\t{:16}\t{:16}\t{:16}\t{:8}\t{:16}"
    print(tplt.format("序号", "goodID", "商品名称", "价格", "月销量", "店铺", "链接", "图片url"))
    count = 0
    for g in ilt:
        count = count+1
        print(tplt.format(count, g[0], g[1], g[2], g[3], g[4], g[5], g[6]))
        if count == num:
            break
    print("")


def getTaobaoProd(qName = '手机', cnt = 1):
    use_old = 0
    print('qName, cnt: ', qName, cnt)
    url = "https://s.taobao.com/search"
    dSearch = {'q': qName, 's': '0',
    'imgfile':'',
    'commend':'all','ssid':'s5-e','search_type':'item','sourceId':'tb.index','spm':'a21bo.2017.201856-taobao-item.1','ie':'utf8','initiative_id':'tbindexz_20170306'}
    infoList = []
    for i in range(1):
        time.sleep(1)
        dSearch['s'] = str(44 * i)
        html = None
        try:
            if use_old == 1:
                with open(DATA_ROOT_PATH+"iTaobaoSJ.html", "r", encoding='utf-8') as f:
                    html = f.read()
            else:
                html = getTBHTMLText(url, dSearch)
                if i == 0:
                    with open(DATA_ROOT_PATH+"iTaobaoSJ.html", "w", encoding='utf-8') as f:
                        f.write(html)
            parsePage(infoList, html, cnt)
            if len(infoList) >= cnt:
                break
        except:
            print("获取淘宝商品产生异常")
    printGoodsList(infoList)
    return infoList


def getNewPrice(url, op):
    html = getTBHTMLText(url, None, 1)
    plt = re.findall(r'\"price\"\:\"[\d\.]*\"', html)
    try:
        return float(eval(plt[0].split(":")[1]))
    except:
        return op


def test_dec(a_func):
    @wraps(a_func)
    def wrapTheFunction(*args, **kwargs):
        start = time.perf_counter()
        a_func(*args, **kwargs)
        end = time.perf_counter()
        print('Decorator: Running time: %s Seconds' % (end - start))

    return wrapTheFunction


@test_dec
def my_test():
    getTaobaoProd()


if __name__ == '__main__':
    my_test()
    pass


def printComments(ilist):
    cnt = 0
    for x in ilist:
        print(cnt, x[0], x[1], x[2], x[3])
        cnt += 1
    print("")


# https://rate.tmall.com/list_detail_rate.htm?itemId=629748003807&spuId=1846540591&sellerId=268451883&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvl9vnvPOvUpCkvvvvvjiWPLqZ1jEHRLFhAjthPmPhsjYbPLF9ljn2n2SOQjiRROvCvCLwjUYJDrMwznAa9lS5FMsJzVD448QCvvyvmCQmFgGvbvTVvpvhvvpvv29Cvvpvvvvv29hvCvvvMMGvvpvVvvpvvhCvKvhv8vvvvvCvpvvtvvmm7ZCvmR%2BvvvWvphvW9pvv9DDvpvACvvmm7ZCv2UVUvpvVmvvC9j3vuvhvmvvv9b%2B1eAw0mvhvLvCrpQvjn%2BkQ0f06WeCpqU0HsfUpwyjIAXcBKFyK2ixrQj7JVVQHYnFhAEI7nDeDyO2vSdtIjbmYSW94P5CXqU5EDfmlJ1kHsX7veEkevpvhvvmv9uQCvvyvmH9mKdIv8EQgvpvhvvvvvv%3D%3D&needFold=0&_ksTS=1612519758221_703&callback=jsonp704
def reqProdComments(url, csv_writer, num=5):
    if num > 20: num = 20
    if num <= 0: num = 10
    result = []
    head = {
        "referer": "https://detail.tmall.com/item.htm",
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'cookie': tb_cookie
    }
    itemId = re.search(r'id\=(\d+)', url).group(1)
    print("itemId:", itemId)
    sellerId = "268451883"
    try:
        r = requests.get(url, timeout=1, headers=head)
        r.raise_for_status()
        sellerId = re.search(r'sellerId\:\"(\d+)\"', r.text).group(1)
        print("sellerId: ", sellerId)
    except:
        print("获取淘宝评论出现bug1")
        return result
    dSearch = {
        "itemId": itemId,
        "sellerId": sellerId,
        "currentPage": "1",
        "callback": "jsonp704"
    }
    url = 'https://rate.tmall.com/list_detail_rate.htm'
    attris = ["displayUserNick", "auctionSku", "rateDate", "rateContent"]
    head['cookie'] = tb_cm_cookie
    try:
        while len(result) < num:
            r = requests.get(url, timeout=1, headers=head, params=dSearch)
            r.raise_for_status()
            print(r.url)
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
    except Exception as e:
        print(e)
        print("获取淘宝评论出现bug2")
    return result


def getTBProdComments(url):
    time.sleep(1)
    ilist = []
    with open(DATA_ROOT_PATH + 'tbCommentData.csv', 'a+', newline='', encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerow(("用户昵称", "商品型号", "评论时间", "评论内容"))
        ilist = reqProdComments(url, writer)
    # printComments(ilist)
    return ilist