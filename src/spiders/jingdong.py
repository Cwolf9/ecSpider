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
def getHTMLText(url, code='utf-8'):
    head = {
        'referer': 'https://search.jd.com/',  # 每个页面的后半部分数据，是通过下拉然后再次请求，会做来源检查。
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': 'dasgfagda'
    }
    try:
        r = requests.get(url, timeout=30, headers=head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("获取京东URL页面失败")
        return "获取京东URL页面失败"

def parsePage(ilt, html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        nameInfo = soup.find_all('div', attrs={'class': 'p-name'})
        priceInfo = soup.find_all('div', attrs={'class': 'p-price'})
        # print(nameInfo)
        # print(priceInfo)
        for i in range(len(nameInfo)):
            glink = nameInfo[i].find('a')['href'][2:]
            titlelst = nameInfo[i].find('em').text.split()
            name = ""
            for j in range(len(titlelst)):  # 此处要注意循环变量不能混淆，与JS不同
                # 注意！！！此处之前是选择了截取长度，但是截取长度导致了后几个页面有些数据丢失，不知道为什么 :TODO
                name = name + titlelst[j]
                if len(name) >= 68:
                    break
                if j != len(titlelst) - 1:
                    name += " "
            price = priceInfo[i].find('strong').text
            if (price == '￥'):  # 特殊情况，特殊处理
                price = '￥' + priceInfo[i].find('strong')['data-price']
            ilt.append([price.strip(), glink.strip(), name.strip()])
    except:
        print("解析京东HTML内容失败")
def printGoodsList(ilt, num = 20):
    tplt = "{:4}\t{:8}\t{:20}\t{:20}"
    print(tplt.format("序号","价格","链接","商品名称"))
    count=0
    for g in ilt:
        count=count+1
        print(tplt.format(count,g[0],g[1],g[2]))
        if count == num:
            break
    print("")
def getJDProd(qName = '手机', depth = 1):
    timeID = '%.5f' % time.time()  # 时间戳保留后五位
    infoList = []
    for i in range(depth):
        try:
            with open("D:/iJDSJ.html", "r", encoding='utf-8') as f:
                html = f.read()
                url = 'https://search.jd.com/Search?keyword=' + qName + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=' + qName + '&cid2=653&cid3=655&page=' + str(
                    (i + 1) * 2 - 1) + '&click=0'  # 此处注意 应该给i加1，注意细节
                # html = getHTMLText(url)
                # if i == 0:
                #     with open("D:/iJDSJ.html", "w", encoding='utf-8') as f:
                #         f.write(html)
                parsePage(infoList, html)
                time.sleep(1)
        except:
            print("获取京东商品产生异常")
    return infoList
jd_comment_path = 'jd_comment.txt'
def reqProdComments(url, csv_writer, num = 10):
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
    attris = ["creationTime", "score", "replyCount", "usefulVoteCount", "imageCount", "content"]
    try:
        while len(result) < num :
            time.sleep(1)
            r = requests.get(url, timeout=30, headers=head, params = dSearch)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            comment_list = reCommentLi.findall(r.text)
            if r.text == "" or len(comment_list) == 0:
                break
            # print(r.text[20:-2])
            rtjs = json.loads(r.text[20:-2])
            comments = rtjs['comments']
            for comment in comments:
                tmp = []
                for attri in attris:
                    if(attri == 'content') :
                        # comment[attri] = html.unescape(comment[attri]).replace(r'\n', ' ')
                        comment[attri] = comment[attri].replace('\n', ' ')
                        with open(jd_comment_path, 'a+', encoding='utf-8') as fjd :
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
    except:
        print("获取京东评论出现bug")
    return result


def printComments(ilist):
    cnt = 0
    for x in ilist:
        print(cnt, x[0], x[1], x[2], x[3], x[4], x[5])
        cnt += 1
    print("")


def getJDProdComments():
    time.sleep(1)
    ilist = []
    with open('jdData.csv', 'a+', newline='', encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerow(('留言时间', '评分', '回复数', '点赞数', '图片数', '评论内容'))
        ilist = reqProdComments('https://item.jd.com/30191153091.html', writer)
    printComments(ilist)

def main():
    time.sleep(1)
    infoList = getJDProd()
    printGoodsList(infoList)

if __name__ == '__main__':
    print('hello')
    main()
    # getJDProdComments()