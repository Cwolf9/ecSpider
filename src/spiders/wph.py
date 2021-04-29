# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: wph
@date: 2021-04-14 13:49
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
import time
import json
import csv
import random
from src.conf_win import *


wph_cookie = r'vip_first_visitor=1; vip_address=%7B%22pid%22%3A%22104103%22%2C%22cid%22%3A%22104103101%22%2C%22pname%22%3A%22%5Cu6e56%5Cu5357%5Cu7701%22%2C%22cname%22%3A%22%5Cu957f%5Cu6c99%5Cu5e02%22%7D; vip_province=104103; vip_province_name=湖南省; vip_city_name=长沙市; vip_city_code=104103101; vip_wh=VIP_HZ; vip_ipver=31; user_class=a; mars_sid=d9ba74d2ab2a708b352299bab1ffe926; PHPSESSID=jp60fjfc21l8989847tc69ui76; mars_pid=0; VIP_QR_FIRST=1; VipUINFO=luc:a|suc:a|bct:c_new|hct:c_new|bdts:0|bcts:0|kfts:0|c10:0|rcabt:0|p2:0|p3:1|p4:0|p5:0|ul:3105; visit_id=A331AA75C7B816A95F8736F13E2E8213; vipshop_passport_src=https://detail.vip.com/; pg_session_no=15; vip_tracker_source_from={"activity_data":"%7B%22common_set%22%3A%7B%22title%22%3A%22%E5%9C%A8%E5%94%AE%E5%95%86%E5%93%81%E5%88%86%E7%B1%BB%E3%80%90%E5%93%81%E7%89%8C%20%E6%AD%A3%E5%93%81%20%E4%BD%8E%E4%BB%B7%E3%80%91_%E5%94%AF%E5%93%81%E4%BC%9A%22%7D%7D","activity_ext":"%7B%22keyword%22%3A%22%E6%89%8B%E6%9C%BA%22%7D","activity_id":"0003","activity_type":"tap"}; mars_cid=1618403676827_7b4c75a702230ee07b1059bc10307c31; vip_access_times={"list":5,"detail":0}'
wph_cookie = strToBytes(wph_cookie)
print(wph_cookie)
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
                "referer": "https://s.taobao.com/",
                'cookie': wph_cookie
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


def getWPHHTMLText(url, dSearch, ip=0):
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        "referer": "https://category.vip.com/",
        'cookie': wph_cookie
    }
    cookie_dict = {
        'cookie': wph_cookie
    }
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
        print("获取URL页面失败")
        return "获取URL页面失败"

def parsePage(ilt, html):
    try:
        start = html.index('{')
        end = html.index('})') + 1
        json_data = json.loads(html[start:end])
        json_data = json_data['data']['products']
        print(json_data)
        data_len = len(json_data)
        for i in range(data_len):
            itemId = 'wph'+json_data[i]['productId']
            brandId = json_data[i]['brandId']
            urlLink = f'detail.vip.com/detail-{brandId}-{itemId}.html'
            title = json_data[i]['title']
            msales = str(random.randint(1, 100))
            price = json_data[i]['price']['salePrice']
            shop_name = json_data[i]['brandShowName']
            pic_url = json_data[i]['smallImage']
            ilt.append([itemId, title, price, msales, shop_name, urlLink, pic_url])
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


def getWPHProd(qName='手机', cnt=3):
    use_old = 0
    print('qName, cnt: ', qName, cnt)
    offset = 0
    infoList = []
    for idp in range(1):
        time.sleep(1)
        url = f'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank?callback=getMerchandiseIds&app_name=shop_pc&app_version=4.0&warehouse=VIP_HZ&fdc_area_id=104103101&client=pc&mobile_platform=1&province_id=104103&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1618403676827_7b4c75a702230ee07b1059bc10307c31&wap_consumer=a&standby_id=nature&keyword={qName}&lv3CatIds=&lv2CatIds=&lv1CatIds=&brandStoreSns=&props=&priceMin=&priceMax=&vipService=&sort=0&pageOffset=0&pageOffset={offset}&channelId=1&gPlatform=PC&batchSize=120&_=1618410683071'
        offset += 120
        html = None
        try:
            if use_old == 1:
                with open(DATA_ROOT_PATH+"iWphRkSJ.html", "r", encoding='utf-8') as f:
                    html = f.read()
            else:
                html = getWPHHTMLText(url, None, 1)
                if idp == 0:
                    with open(DATA_ROOT_PATH+"iWphRkSJ.html", "w", encoding='utf-8') as f:
                        f.write(html)
            start = html.index('{')
            end = html.index('})') + 1
            json_data = json.loads(html[start:end])
            json_data = json_data['data']['products']
            rk_len = min(cnt, len(json_data))
            cnt -= rk_len
            pid_str = ""
            for i in range(rk_len):
                pid_str += json_data[i]['pid'] + ','
            url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2?callback=getMerchandiseDroplets1&app_name=shop_pc&app_version=4.0&warehouse=VIP_HZ&fdc_area_id=104103101&client=pc&mobile_platform=1&province_id=104103&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1618403676827_7b4c75a702230ee07b1059bc10307c31&wap_consumer=a&productIds={}' \
                  '&scene=search&standby_id=nature&extParams=%7B%22stdSizeVids%22%3A%22%22%2C%22preheatTipsVer%22%3A%223%22%2C%22couponVer%22%3A%22v2%22%2C%22exclusivePrice%22%3A%221%22%2C%22iconSpec%22%3A%222x%22%2C%22ic2label%22%3A1%7D&context=&_=1618472405301'.format(pid_str)
            print(url)
            if use_old == 1:
                with open(DATA_ROOT_PATH+"iWphSJ.html", "r", encoding='utf-8') as f:
                    html = f.read()
            else:
                html = getWPHHTMLText(url, None, 1)
                if idp == 0:
                    with open(DATA_ROOT_PATH+"iWphSJ.html", "w", encoding='utf-8') as f:
                        f.write(html)
            parsePage(infoList, html)
            if cnt <= 0:
                break
        except:
            print("获取商品产生异常")
    printGoodsList(infoList)
    return infoList


def getJsonData(html):
    start = html.index('{')
    end = html.index('})') + 1
    return json.loads(html[start:end])


def getNewPrice(url, op):
    try:
        pid = url.split('-')[-1].split('.')[0]
        url = f'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/detail/v5?callback=detailInfoCB&app_name=shop_pc&app_version=4.0&warehouse=VIP_HZ&fdc_area_id=104103101&client=pc&mobile_platform=1&province_id=104103&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1618403676827_7b4c75a702230ee07b1059bc10307c31&wap_consumer=a&productId={pid}&functions=brand_store_info%2CnewBrandLogo%2ChideOnlySize%2CextraDetailImages%2Csku_price%2Cui_settings&kfVersion=1&highlightBgImgVer=1&is_get_TUV=1&commitmentVer=2&haitao_description_fields=text&supportSquare=1&longTitleVer=2&propsVer=1'
        html = getWPHHTMLText(url, None, 1)
        return float(getJsonData(html)['data']['product']['min_vipshop_price'])
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
    getWPHProd()

if __name__ == '__main__':
    my_test()
    x = getNewPrice('https://detail.vip.com/detail-1710613295-6919031768266477647.html', 13989.0)
    print(x)
    pass





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
        'cookie': wph_cookie
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
        print("获取评论出现bug1")
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
        print("获取评论出现bug2")
    return result

def getTBProdComments(url):
    time.sleep(1)
    ilist = []
    with open(DATA_ROOT_PATH + 'wphCommentData.csv', 'a+', newline='', encoding='gb18030') as f:
        writer = csv.writer(f)
        writer.writerow(("用户昵称", "商品型号", "评论时间", "评论内容"))
        ilist = reqProdComments(url, writer)
    printComments(ilist)
'''
[{'productId': '6918663538697742531', 'brandId': '1710615683', 'brandStoreSn': '10010712', 'categoryId': '1082', 'spuId': '1454739529706520576', 'skuId': '371905269467332612', 'status': '0', 'title': '畅享10S全网通4G手机', 'brandShowName': '华为', 'smallImage': 'http://h2.appsimg.com/a.appsimg.com/upload/merchandise/pdcvis/612272/2019/1214/134/0043dfc7-c9bb-4289-a329-ef22414aee1c_420_531.jpg', 'squareImage': 'http://h2.appsimg.com/a.appsimg.com/upload/merchandise/pdcvis/612272/2019/1214/50/1e627f0f-5a61-4369-a15c-c4f10a7e2c9e.jpg', 'logo': 'http://a.vpimg3.com/upload/brandcool/0/b5db46e8bfbf444b985b1708e6cf0ca6/10010712/primary.png', 'price': {'priceType': 'special', 'priceLabelType': 'text', 'priceLabel': '特卖价', 'salePrice': '1728', 'salePriceSuff': '', 'saleDiscount': '', 'marketPrice': '1729'}, 'attrs': [{'name': '屏幕尺寸', 'value': '6.3英寸'}, {'name': '机身内存', 'value': '64G/128G'}, {'name': '运行内存', 'value': '4G/6G/8G'}, {'name': '首销日期', 'value': '2019-12-05'}], 'flags': 52}]
'''