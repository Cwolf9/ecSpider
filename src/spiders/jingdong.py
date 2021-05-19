# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: jingdong
@date: 2021-04-05 22:33
@desc:
"""
# https://blog.csdn.net/CUFEECR/article/details/105467109 ThreadPoolExecutor
# https://blog.csdn.net/aelous_dp/article/details/107461249
import requests
import re
from bs4 import BeautifulSoup
import time
import html
import csv
import json
from src.conf_win import *
import random
import os


jd_cookie = r'__jdu=16117310176871406427129; shshshfpa=dee6d79e-ffb8-a320-e9a3-f4480a9d7fce-1611731020; shshshfpb=w8shDykhS2FrhhTT zWdgyA==; rkv=1.0; qrsc=3; pinId=vFWcniFLl1Uf8axLOC0-K7V9-x-f3wj7; TrackID=1tOYZgdgNPivwxW_dsIJjenFEsWQ7hzLh0jqbNqpqELaDl5k0dbrj43q2k0tkXghULsoCET3-hglvt2Iz20csoP4KFqGkSJ5QRygi3_Y7XX0; __jdv=76161171|direct|-|none|-|1619426867875; areaId=18; ipLoc-djd=18-1482-48939-0; PCSYCityID=CN_430000_430100_0; __jdb=122270672.2.16117310176871406427129|26.1619429071; __jdc=122270672; __jda=122270672.16117310176871406427129.1611731018.1619426868.1619429071.26; shshshfp=9217dafd13ebff4ae5418395e2de5a8c; shshshsID=7fcd14e639c7f8386d3804f73e443cd1_2_1619429076882; 3AB9D23F7A4B3C9B=H4JKAUHLDON5RAUTUQQCCKVZAIOC3QYU6GNCZI65J2ZMPNAMZMU6WUW53EIVIOS573UYQMRSJ7HFGZMSFTGBYLV5DU'


def downPic(url="https://img13.360buyimg.com/n7/jfs/t1/136205/10/7310/56308/5f3dee56E034ab78c/ffc11f69acf791e5.jpg"):
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
                'cookie': jd_cookie
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


def getHTMLText(url, code='utf-8'):
    head = {
        'referer': 'https://search.jd.com/',  # 每个页面的后半部分数据，是通过下拉然后再次请求，会做来源检查。
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'cookie': jd_cookie
    }
    try:
        r = requests.get(url, timeout=1, headers=head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("获取京东URL页面失败")
        return "获取京东URL页面失败"


def parsePage(ilt, html, cnt):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        nameInfo = soup.find_all('div', attrs={'class': 'p-name'})
        priceInfo = soup.find_all('div', attrs={'class': 'p-price'})
        shopInfo = soup.find_all('div', attrs={'class': 'p-shop'})
        imgInfo = soup.find_all('div', attrs={'class': 'p-img'})
        # print(nameInfo)
        # print(priceInfo)
        for i in range(len(nameInfo)):
            glink = nameInfo[i].find('a')['href'][2:]
            titlelst = nameInfo[i].find('em').text.split()
            name = ""
            for j in range(len(titlelst)):  # 此处要注意循环变量不能混淆
                name = name + titlelst[j]
                if len(name) >= 68:
                    break
                if j != len(titlelst) - 1:
                    name += " "
            price = priceInfo[i].find('strong').find('i').text
            if (not price): # 特殊情况，特殊处理
                price = priceInfo[i].find('strong')['data-price']
            shop_name = shopInfo[i].find('a').text
            picpath = imgInfo[i].find('img')['data-lazy-img'][2:]
            itemId = glink.strip().split('/')[-1].split('.')[0]
            itemId = 'JD' + itemId

            ilt.append([itemId, name.strip(), price.strip(), str(random.randint(1, 1000)), shop_name.strip(), glink.strip(), picpath.strip()])
            if len(ilt) >= cnt:
                break
    except:
        print("解析京东HTML内容失败")


def printGoodsList(ilt, num = 20):
    tplt = "{:4}\t{:8}\t{:8}\t{:20}\t{:20}\t{:20}\t{:20}\t{:16}"
    print(tplt.format("序号", 'ID', "商品名称", "价格", '月销量', '店铺', "链接", 'picpath'))
    count = 0
    for g in ilt:
        count = count+1
        print(tplt.format(count, g[0], g[1], g[2], g[3], g[4], g[5], g[6]))
        if count == num:
            break
    print("")


def getJDProd(qName = '手机', cnt = 1):
    use_old = 0
    timeID = '%.5f' % time.time()  # 时间戳保留后五位
    infoList = []
    for i in range(1):
        time.sleep(1)
        html = None
        try:
            if use_old == 1:
                with open(DATA_ROOT_PATH+"iJDSJ.html", "r", encoding='utf-8') as f:
                    html = f.read()
            else:
                url = 'https://search.jd.com/Search?keyword=' + qName + '&enc=utf-8&wq=' + qName + '&page=' + str((i + 1) * 2 - 1) + '&click=0'
                html = getHTMLText(url)
                if i == 0:
                    with open(DATA_ROOT_PATH+"iJDSJ.html", "w", encoding='utf-8') as f:
                        f.write(html)

            parsePage(infoList, html, cnt)
            if len(infoList) >= cnt:
                break
        except:
            print("获取京东商品产生异常")
    printGoodsList(infoList)
    return infoList


def getJsonData(html):
    start = html.index('{')
    end = html.index('})') + 1
    return json.loads(html[start:end])


def getNewPrice(url, op):
    try:
        pid = re.search('/(\w*).html', url).group(1)
        url = f'https://item-soa.jd.com/getWareBusiness?callback=jQuery2423859&skuId={pid}'
        html = getHTMLText(url)
        json_data = getJsonData(html)['price']
        print(json_data)
        return float(json_data['p'])
    except:
        return op


def main():
    time.sleep(1)
    infoList = getJDProd()
    printGoodsList(infoList)


if __name__ == '__main__':
    print('hello')
    # main()
    x = getNewPrice('https://item.jd.com/100014348492.html', 12333.0)
    print(x)
    # getJDProdComments()

jd_comment_path = DATA_ROOT_PATH + 'jd_comment.txt'


def reqProdComments(url, csv_writer, num=5):
    if num > 20: num = 20
    if num <= 0: num = 10
    result = []
    pid = url.split('/')[-1].split('.')[0]
    head = {
        'referer': 'https://search.jd.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'cookie':r'__jdv=76161171|direct|-|none|-|1611731017688; __jdu=16117310176871406427129; user-key=1a59fcf3-fdc0-4a17-9805-d1f856004223; areaId=4; shshshfpa=dee6d79e-ffb8-a320-e9a3-f4480a9d7fce-1611731020; shshshfpb=w8shDykhS2FrhhTT zWdgyA==; ipLoc-djd=4-50951-50965-0; TrackID=1_8mEDXIB1Q7ZUwfJVONM6zD2oq5ZVlZ1md2Kpd2eN2Ko9xYCmZFa7CR2GHjio_G0IPB9qjV0B_rbaPlmM-8Oh7hUcrxroe_D5MApgjx_-5AEfmFy_lMjJMxvx2PP5fOH; pinId=vFWcniFLl1Uf8axLOC0-K7V9-x-f3wj7; pin=jd_71e2e437693da; unick=Cwolf9; ceshi3.com=203; _tp=2DWUiz01VPtXkyXPx03anqCtVg+BiOtslrofe6wlPM0=; _pst=jd_71e2e437693da; __jdc=122270672; shshshfp=0f36980f1d4ef4d9a64edbe653fc0d4a; 3AB9D23F7A4B3C9B=H4JKAUHLDON5RAUTUQQCCKVZAIOC3QYU6GNCZI65J2ZMPNAMZMU6WUW53EIVIOS573UYQMRSJ7HFGZMSFTGBYLV5DU; cn=0; __jda=122270672.16117310176871406427129.1611731018.1612157993.1612322117.13; jwotest_product=99; JSESSIONID=F14A11AAF17621F4A34CA1EA86BD6245.s1; shshshsID=bc1d2b6be48b619180a26b0977c1db88_3_1612323809691; __jdb=122270672.3.16117310176871406427129|13.1612322117'
    }
    reCommentLi = re.compile(r'"guid":".*?"content":"(.*?)".*?"creationTime":"(.*?)",".*?"replyCount":(\d+),"score":(\d+).*?usefulVoteCount":(\d+).*?imageCount":(\d+).*?images":')
    # https://club.jd.com/comment/productCommentSummaries.action?referenceIds=100000499657
    dSearch = {
        "callback": "fetchJSON_comment98",
        "productId": pid,
        "score":"0","sortType":"5",
        "page":"0","pageSize":'10',
        "isShadowSku":"0","fold":"1",
    }
    url = 'https://club.jd.com/comment/productPageComments.action'
    attris = ["creationTime", "score", "replyCount", "usefulVoteCount", "content"]
    try:
        while len(result) < num :
            time.sleep(1)
            r = requests.get(url, timeout=30, headers=head, params=dSearch)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            comment_list = reCommentLi.findall(r.text)
            if r.text == "" or len(comment_list) == 0:
                break
            with open(DATA_ROOT_PATH + "iJingdongPinlun.html", "w", encoding='utf-8') as f:
                f.write(r.text[20:-2])
            rtjs = json.loads(r.text[20:-2])
            comments = rtjs['comments']
            for comment in comments:
                tmp = []
                for attri in attris:
                    if(attri == 'content') :
                        # comment[attri] = html.unescape(comment[attri]).replace(r'\n', ' ')
                        comment[attri] = comment[attri].replace('\n', ' ')
                        with open(jd_comment_path, 'a+', encoding='utf-8') as fjd:
                            fjd.write(comment[attri] + '\n')
                    tmp.append(comment[attri])
                result.append(tmp)
                csv_writer.writerow(tmp)
                if len(result) == num:
                    break
            # for comt in comment_list:
            #     if len(comt) != 6 :
            #         continue
            #     content = html.unescape(comt[0]).replace(r'\n', ' ')#将HTML转义字符如&;等转化成普通字符串
            #     creationTime = comt[1]
            #     replyCount = comt[2]
            #     score = comt[3]
            #     usefulVoteCount = comt[4]
            #     imageCount = comt[5]
            #     csv_writer.writerow((creationTime, score, replyCount, usefulVoteCount, imageCount, content))
            #     nli = [content]
            #     for i in range(1, 6):
            #         nli.append(comt[i].strip())
            #     result.append(nli)
            #     if len(result) == num:
            #         break
            dSearch['page'] = str(int(dSearch['page']) + 1)
    except Exception as e:
        print("获取京东评论出现bug")
        print(repr(e))
    return result


def printComments(ilist):
    cnt = 0
    for x in ilist:
        print(cnt, x[0], x[1], x[2], x[3], x[4])
        cnt += 1
    print("")


def getJDProdComments(good_url='https://item.jd.com/30191153091.html'):
    time.sleep(1)
    ilist = []
    with open('jdData.csv', 'a+', newline='', encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerow(('留言时间', '评分', '回复数', '点赞数', '评论内容'))
        ilist = reqProdComments(good_url, writer)
    printComments(ilist)
    return ilist
