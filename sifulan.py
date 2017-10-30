#! /Library/Framework/Python.framework/Versions/2.7/bin/python2.7
# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def send_request(url):
    # proxy = {"http": "http://616353084:j57da14r@43.226.164.60:16816"}
    header = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}
    try:
        print "抓取....."
        response = requests.get(url, headers=header)  # , proxies=proxy)
    except:
        print "[INFO]: 抓取失败....."

    return response.content


def get_page(face_html):
    soup = BeautifulSoup(face_html, "lxml")
    print "抓取面部护理--商品li....."
    goods_list = soup.select('ul[class="mb64 clearFix"] li')

    for node in goods_list:
        item = {}
        item[u'proPic'] = node.select('div[class=proPic] img')[0].get("data-original")
        item[u'proTit'] = node.select('div[class=proTit] a')[0].get_text()
        item[u'proPrice'] = node.select('div[class=proPrice] span')[0].get_text()

        gd_list.append(item)

    now_page = soup.select('div[class="pageList"] em[class="cur"]')[0].get_text()
    print "[INFO]--当前页码:", now_page
    page_all = soup.select('div[class="pageList"] b')[0].get_text()
    print "[INFO]--总页码:", page_all

    if now_page == page_all:
        return False

    if now_page == '1':
        next_link = soup.select('div[class="pageList"] span a')[0].get('href')
        return next_link
    else:
        next_link = soup.select('div[class="pageList"] span')[1].find('a').get('href')
        return next_link


def get_link(html):
    soup = BeautifulSoup(html, "lxml")
    print "[INFO]:抓护肤首页...."
    a_list = soup.select("div[class='categoryNav categoryNavMob'] a[title='面部护理']")
    print len(a_list), "[INFO]:护肤首页获得"
    # a_list = soup.select("div[class='categoryNav categoryNavMob'] a")
    # for item in a_list:
    #     url_list.append({item.get("title"): item.get("href")}) 这里url_list列表里会装完 "护肤" 分类下的所有细分链接--面部护理、眼部护理....

    face = a_list[0].get('title')
    dict_gd = {face: a_list[0].get('href')}

    face_link = dict_gd[face]  # 分类中的面部护理链接

    return face_link


def manage():
    url = "http://www.sephora.cn/category/60001/"  # 护肤首页
    # 请求护肤链接，返回抓取的护肤页面
    html = send_request(url)
    # 页面交给get_link()，拿到分类链接
    face_link = get_link(html)

    while True:
        time.sleep(1)
        # 面部护理链接交给request，返回面部护理分类的页面
        face_html = send_request(face_link)
        # 去页面获取数据，并返回下一页的链接
        face_link = get_page(face_html)

        if not face_link:
            break

    content = json.dumps(gd_list, ensure_ascii=False)
    with open("sephora.json", "w") as f:
        f.write(content)


if __name__ == "__main__":
    url_list = []
    gd_list = []
    manage()
