# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: tmcs
@date: 2021-04-14 10:33
@desc:
"""
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
import json
import csv
import datetime
import time
import random
from src.conf_win import *


# %BE%C6%B7%E8%C0%C7lp
tmcs_cookie = r'dnk=\u9152\u75AF\u72FClp; tracknick=\u9152\u75AF\u72FClp; lid=%BE%C6%B7%E8%C0%C7lp; lgc=\u9152\u75AF\u72FClp; cookie2=17b54f4e7e5b3a136597c2c5d57e44c0; t=5b9661cda0b5e825c49d562bbebfb7f1; enc=4IcYQAEf6n8oYeYZDLKpWuyuMMQld6/11EcD6gmhQrw/ybZmwqhhOo45tTuOpZMXQNYfj/hoIHrzvTvg+5UuTA==; _tb_token_=57b73e781399b; cna=ghItGJbpnRQCAd73JQuwqdcQ; uc1=cookie16=V32FPkk/xXMk5UvIbNtImtMfJQ==&existShop=false&cookie14=Uoe1gBpZqGHGQg==&cookie15=VFC/uZ9ayeYq2g==&cookie21=WqG3DMC9FxUx&pas=0; uc3=lg2=U+GCWk/75gdr5Q==&id2=UU6nRCwmzNLA9Q==&nk2=3Rj2a800wpk=&vt3=F8dCuAbxCoj4v7atgv8=; uc4=nk4=0@35PWOqVA3il14dduk5b4ZJJJiw==&id4=0@U2xqIFo4BlQVQlqi37AO9HXTIQFc; sgcookie=E100WCK/GES0f1rWEWqgef+IoX8ChYTi9mK5iueuasqbLeyLH5lWoq4meqqwtyvqCrbG7oFJsFY0G0sWYP2HEwZQHA==; csg=d97e4d29; sm4=430100; _m_h5_tk=96442ef8a65eae8c60d10b85ae5099b4_{}; _m_h5_tk_enc=30999bc0c642402eb7f9e7701dfcf9e2; xlly_s=1; _med=dw:1228.8&dh:691.2&pw:1536&ph:864&ist:0; cq=ccp=1; _uab_collina=161836826412845621368136; csa=0_0_0.0; x5sec=7b22746d616c6c7365617263683b32223a223838316139386365643035363236333064336538396135313430393931313033434e6e3532594d47454e4b793034547a7037623270414561444449324e6a55354f5445324e5445374d54446a316f536d2b662f2f2f2f3842227d; res=scroll:1442*5354-client:1442*762-offset:1442*5354-screen:1536*864; pnm_cku822=098#E1hvxpvUvbpvUvCkvvvvvjiWPLLWzjnmPFMWzjthPmP9Aj3PPLqWgjtRPszw1jtUi9hvCvvvpZpvvpvVvUCvpvvvuvhvmvvvpLyq4spgkvhvC9hvpyP9gb9Cvm9vvhCvvvvvEQvvBNwvvvHYvvCVB9vv9LvvvhczvvmCWvvvBNwvvUhQmvhvLUmNQWvag8TJ+ulgE4AUKfu1h7QEfJmK5d8rJm7+kbwshBODN+3l5d8rjC6sswh0r2IZOymy+b8re4tYVVzUd3wt+FXLAw0AHEp7EcgRvpvhvv2MMs9CvvpvvhCv; tfstk=cc7RBFDZJ-2urJRA_gEmOGoRE9QRZZcJKb9KJ7UEL6JjkL3di27GWGtgVBkJkSC..; l=eBOiGEpqjNZKySXoBOfZnurza77TsIRAguPzaNbMiOCPO25e5bSVW6arsjTwCnGVhsgMR3zWDma6BeYBqID6rVmstBALuzkmn; isg=BMvLGoeDL-Q0KHNRowLQiXJdWm-1YN_iUeGtwD3IrYphXOu-xTJvMvj-Mlyy_Dfa'


def downPic(url = "https://g-search3.alicdn.com/img/bao/uploaded/i4/i1/3063905773/O1CN01qXLQ231sW59J818ds_!!0-item_pic.jpg"):
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
                "referer": "https://list.tmall.com/",
                'cookie': tmcs_cookie
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


#UA池，更多UA头部可参考 http://www.useragentstring.com/pages/useragentstring.php
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 ",
      "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
      "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 ",
      "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 ",
      "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 ",
      "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 ",
      "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 ",
      "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
      "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 ",
      "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 ",
      "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 ",
      "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 ",
      "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]

def getTMCSHTMLText(url, dSearch, ip=0):
    # 获取当前时间
    d1 = datetime.datetime.now()
    # 时间计算 加2小时05分钟
    d3 = d1 + datetime.timedelta(hours=2, minutes=5)
    # 转字符串
    a = d3.strftime("%Y-%m-%d %H:%M:%S")
    # 转数组
    b = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    # 转时间戳
    time2 = int(time.mktime(b) * 1000)
    print('时间戳 ', time2)
    host = ["list.tmall.com", 'detail.tmall.com']
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "user-agent": user_agent_list[0],
            #random.choice(user_agent_list),
        "Host": host[ip],
        "referer": "https://list.tmall.com/",
        'upgrade-insecure-requests': '1',
        'cookie': tmcs_cookie.format(time2)
    }
    cookie_dict = {
        'cookie': tmcs_cookie.format(time2)
    }
    try:
        reqS = requests.Session()
        # reqS.cookies.update(cookie_dict)
        cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
        reqS.cookies = cookies
        # print(cookies)
        if ip == 0:
            r = reqS.get(url, timeout=1, headers=headers, params=dSearch, allow_redirects=False)
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
        print("获取URL页面失败")
        return "获取URL页面失败"


def parsePage(ilt, html, cnt):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        nameInfo = soup.find_all('p', attrs={'class': 'productTitle'})
        priceInfo = soup.find_all('p', attrs={'class': 'productPrice'})
        shopInfo = soup.find_all('div', attrs={'class': 'productShop'})
        imgInfo = soup.find_all('a', attrs={'class': 'productImg'})
        for i in range(len(nameInfo)):
            glink = nameInfo[i].find('a')['href'].split('&')[0][2:]
            titlelst = nameInfo[i].find('a').text.split()
            name = ""
            for j in range(len(titlelst)):  # 此处要注意循环变量不能混淆，与JS不同
                # 注意！！！此处之前是选择了截取长度，但是截取长度导致了后几个页面有些数据丢失，不知道为什么 :TODO
                name = name + titlelst[j]
                if len(name) >= 68:
                    break
                if j != len(titlelst) - 1:
                    name += " "
            price = priceInfo[i].find('em').text[1:]
            if (not price):  # 特殊情况，特殊处理
                price = priceInfo[i].find('em')['title']
            shop_name = shopInfo[i].find('a').text
            picpath = imgInfo[i].find('img')['src'][2:]
            itemId = re.search(r'id\=(\d+)', glink).group(1)
            itemId = 'TM' + itemId
            ilt.append(
                [itemId, name.strip(), price.strip(), str(random.randint(1, 1000)), shop_name.strip(), glink.strip(),
                 picpath.strip()])
            if len(ilt) >= cnt:
                break
    except:
        print("解析HTML内容失败")


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


def getTMCSProd(qName='手机', cnt=3):
    use_old = 0
    print('qName, cnt: ', qName, cnt)
    url = "https://list.tmall.com/search_product.htm"
    dSearch = {'q': qName, 's': '0'}
    infoList = []
    for i in range(1):
        time.sleep(1)
        dSearch['s'] = str(60 * i)
        html = None
        try:
            if use_old == 1:
                with open(DATA_ROOT_PATH+"iTmcsSJ.html", "r", encoding='utf-8') as f:
                    html = f.read()
            else:
                html = getTMCSHTMLText(url, dSearch)
                if i == 0:
                    with open(DATA_ROOT_PATH+"iTmcsSJ.html", "w", encoding='utf-8') as f:
                        f.write(html)
            parsePage(infoList, html, cnt)
            if len(infoList) >= cnt:
                break
        except:
            print("获取商品产生异常")
    printGoodsList(infoList)
    return infoList


def getNewPrice(url, op):
    """
    HTTPSConnectionPool(host='detail.tmall.com', port=443): Read timed out. (read timeout=5)
    :param url:
    :param op:
    :return:
    """
    html = getTMCSHTMLText(url+'&sku_properties=5919063:6536025;122216431:27772', None, 1)
    plt = re.findall(r'\"price\"\:\"[\d\.]*\"', html)
    ans = 1000000000.0
    try:
        for pli in plt:
            min_val = float(eval(pli.split(":")[1]))
            ans = min(ans, min_val)
        return ans
    except:
        return min(ans, op)


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
    getTMCSProd()


if __name__ == '__main__':
    my_test()
    x = getNewPrice('https://detail.tmall.com/item.htm?id=639142927098', 12.3)
    print(x)
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
        "referer": "https://chaoshi.detail.tmall.com/item.htm",
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'cookie': tmcs_cookie
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
    except Exception as e:
        print(e)
        print("获取tmcs评论出现bug2")
    return result

def getTMCSProdComments(url):
    time.sleep(1)
    ilist = []
    with open(DATA_ROOT_PATH+'tmcsCommentData.csv', 'a+', newline='', encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerow(("用户昵称", "商品型号", "评论时间", "评论内容"))
        ilist = reqProdComments(url, writer)
    printComments(ilist)
    return ilist