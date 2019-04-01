# !/usr/bin/python
# -*- coding:utf-8 -*-
import config
import requests
import os
import datetime
from bs4 import BeautifulSoup
import urllib2
import urllib
import sys
import re
import pymongo
from config import *

reload(sys)
sys.setdefaultencoding("utf-8")
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def getHTMLText(url):
    # headers = {
    #
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    # }
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

    except urllib2.URLError, e:
        return ""
    if response.getcode() == 200:
        return response.read()
    else:
        print '网页错误'
        return ""
def parsePage(html):
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find_all('p', class_='site-piclist_info_title')
    for i in lis:
        url = 'https:' + i.a['href']
        show=i.a['href']
        print url
        print i.a.string
        # str2 = "list"
        # html = getHTMLText(url)
        #
        #
        # if html == "":
        #     continue
        # if url[8:12] == str2:
        #     data=parsetvinfo(html, i.a.string,show)  # 解析url中信息，主持人、地区、类型
        #     findtvshow(data)
        #
        # else:
        #     url = parsetv(html)  # 获取简介的url
        #     if url:
        #         html = getHTMLText('https:' + url)
        #         data = parsetvinfo(html, i.a.string,show)  # 解析url中信息，主持人、地区、类型
        #         findtvshow(data)


def main():
    starttime = datetime.datetime.now()
    print("爬取爱奇艺内地所有的综艺节目")
    length=30
    for i in range(1,length+1):
        url='https://list.iqiyi.com/www/6/151-------------11-'+str(i)+'-1-iqiyi--.html'
        thtml= getHTMLText(url)
        parsePage(thtml)

    endtime = datetime.datetime.now()
    print("运行时间为：{}".format(endtime - starttime))
if __name__ == "__main__":
    main()
