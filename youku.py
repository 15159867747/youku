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


# 该函数用来收集每页的数据的信息（这里收集的是名字）
def parsePage(namelist, html):
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find_all('li', class_='title')

    for i in lis:
        namelist.append(i.a.string)
        url = 'https:' + i.a['href']
        show=i.a['href']
        str2 = "list"
        html = getHTMLText(url)


        if html == "":
            continue
        if url[8:12] == str2:
            data=parsetvinfo(html, i.a.string,show)  # 解析url中信息，主持人、地区、类型
            findtvshow(data)

        else:
            url = parsetv(html)  # 获取简介的url
            if url:
                html = getHTMLText('https:' + url)
                data = parsetvinfo(html, i.a.string,show)  # 解析url中信息，主持人、地区、类型
                findtvshow(data)



def findtvshow(data):

    if data is  None:
        print '数据为空'
        return

    updatetime = data['update']
    name=data['name']

    if name:
        doc =db.youku.find_one({'update':updatetime,'name':name})

        if doc:
            if str(doc['update']) == str(updatetime):
                print '该剧目前没有更新*********************************************'
            else:
                db.youku.update({'update': doc['update'], 'name': name}, {"$set": {'update': updatetime}})
                print '该剧有更新*****************************************************'
        else:
            db.youku.insert(data)
            urllib.urlretrieve(data['picurl'], data['pic'])
            print '录入新数据'

# def findpicexit(name):
#     doc =db.youku.find_one({'name':name})
#     if doc:
#         return '0'
#     else:
#         return '1'






# parsetvinfo(url)
# parsetv(getHTMLText(i.a['href']))
# print(i.a.string)
# print i.a['href']
# print(len(lis))
# print("this is parsePage")

def parsetv(html):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    if soup.find('div', class_='tvinfo'):
        lis = soup.find('div', class_='tvinfo')
        # print lis.a['href']
        return lis.a['href']
    # //list.youku.com/show/id_z8a031cd4f8cc11e2b8b7.html


def parsetvinfo(html, name,show):

    res_data = {}
    actor = []
    areadict = []
    allfromtvdict = []
    alltypedict = []
    if html=='':
        return res_data

    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    info = soup.find('div', class_='p-base')
    imginfo = soup.find('div', class_="p-thumb")
    ul = info.find('ul')
    # 播放按钮
    res_data['btn']=show
    # print '播放地址',res_data['btn']
    # 地区
    if re.search('<li>地区：(.*?)</li>', str(ul), re.S):
        allarea = re.search('<li>地区：(.*?)</li>', str(ul), re.S)
        area = re.findall('<a .*?>(.*?)</a>', str(allarea.group(0)), re.S)
        for i in area:
            areadict.append(i)
        res_data['area'] = areadict
    else:
        res_data['area'] =''
    # 播出
    if re.search('<li>播出：(.*?)</li>', str(ul), re.S):
        allfromtv = re.search('<li>播出：(.*?)</li>', str(ul), re.S)
        fromtv = re.findall('<a .*?>(.*?)</a>', str(allfromtv.group(0)), re.S)
        for i in fromtv:
            allfromtvdict.append(i)
        res_data['fromtv']=allfromtvdict
    else:
        res_data['fromtv']=''
    # 类型
    if re.search('<li>类型：(.*?)</li>', str(ul), re.S):
        alltype = re.search('<li>类型：(.*?)</li>', str(ul), re.S)
        type = re.findall('<a .*?>(.*?)</a>', str(alltype.group(0)), re.S)
        for i in type:
            alltypedict.append(i)
        res_data['type']=alltypedict
    else:
        res_data['type']=''
    # 图片
    if re.search('src="(.*?)"', str(imginfo)):
        pic = re.search('src="(.*?)"', str(imginfo))
        # <img alt="鲁豫有约 2017" src="http://r1.ykimg.com/051600005A5D752E859B5D05D90E0AB4"/>
        #print str(pic.group(1))
        res_data['pic'] = 'C:/Users/Administrator/Desktop/pic/youku/' + name + '.jpg'
        res_data['picurl']=str(pic.group(1))
    res_data['name']=name
    print res_data['name']
    if info.find('li', class_='p-row p-intro').text:
        res_data['content'] = info.find('li', class_='p-row p-intro').text  # 简介
    else:
        res_data['content'] ='null'
    if info.find('li', class_='p-row p-renew').get_text().strip():
        res_data['update'] = info.find('li', class_='p-row p-renew').get_text().strip()  # 最近更新时间
    else:
        res_data['update']='null'

    # actor=ac.find('li',class_='p-row ')
    if info.find('ul').find('li', class_='p-row '):
        all_href = info.find('ul').find('li', class_='p-row ').find_all('a')
        for link in all_href:
            actor.append(link.get_text())
        res_data['actor']=actor
    return res_data
    # save_to_mongo(name,areadict,actor,content,update,'C:/Users/Administrator/Desktop/pic/youku/'+name+'.jpg',allfromtvdict)


# def save_to_mongo(name,area,actor,content,update,pic,fromty,fromtv):
#     try:
#         if db[MONGO_TABLE].insert(result):
#             print('存储到MONGODB成功', result)
#     except Exception:
#         print('存储到MONGODB失败', result)


# 该函数是用来查找每一个类别有多少页
def findpage(html):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    lis = soup.find('ul', class_='yk-pages')
    lilist = []  # 用来装li标签的
    for li in lis:
        lilist.append(li)
    length = lilist[-2].string
    # 因为[-1]是“下一页,所以[-2]是当前最大页，也就是每一个类别到底有多少页”
    # print("页码数："+lilist[-2].string)
    # print("this is findpage")
    return length


# 该函数是用来把所获得的信息按类别以及年份写入.txt
# def printNameList(namelist, show):
#     if not os.path.exists(r'\Users\Administrator\Desktop\优酷爬取信息'):
#         os.mkdir(r'\Users\Administrator\Desktop\优酷爬取信息')
#     # if not os.path.exists(r'\Users\Administrator\Desktop\优酷爬取信息\{0}'.format(show)):
#     #     os.mkdir(r'\Users\Administrator\Desktop\优酷爬取信息\{0}'.format(show))
#     path = r'\Users\Administrator\Desktop\优酷爬取信息\{0}.txt'.format(show)
#     list = open(path, 'w')
#     list.write('优酷全部{0}节目'.format(show) + '\n')
#     for i in range(len(namelist)):
#         list.write(str(i + 1) + ". " + namelist[i] + '\n')
#     list.close()
#     # print("this is printNameList")
#     return ""


def main():
    starttime = datetime.datetime.now()
    print("有以下优酷类别您可以爬取：综艺、音乐、动漫、体育、剧集、电影")
    url1 = 'http://list.youku.com/category/show/c_85_a_'
    url2 = '_r_'
    url3 = '_s_6_d_1_p_'
    url4 = '.html?spm=a2h1n.8251845.0.0'
    area=['中国','中国台湾','中国香港']
    #area = ['中国香港']

    # 下面的三句话都是为了获取每一个类别每一年有多少页码
    namelist = []
    for j in area:
        print j
        turl = url1 + str(j) + url2 + url3 + str(1) + url4
        thtml = getHTMLText(turl)
        length = int(findpage(thtml))
        # print(str(trueyear)+"有"+str(length)+"页")
        for i in range(1, length + 1):
            url = url1 + str(j) + url2 + url3 + str(i) + url4
            # print(url)
            # print("这是{0}年第{1}页的内容".format(trueyear,i))
            html = getHTMLText(url)
            parsePage(namelist, html)
        #printNameList(namelist, j)
        namelist = []

    endtime = datetime.datetime.now()
    print("运行时间为：{}".format(endtime - starttime))


if __name__ == "__main__":

    # html=getHTMLText('https://v.youku.com/v_show/id_XMjY2NTYxODcyOA==.html')
    # url=parsetv(html)
    # parsetvinfo('https:'+url)
    main()  # http//v.youku.com/v_show/id_XMjY2NTYxODcyOA==.html
    # https://v.youku.com/v_show/id_XMjY2NTYxODcyOA==.html
    # https://v.youku.com/v_show/id_XNDEwMDY0MDcwOA==.html?spm=a2h1n.8251845.0.0
    # https://v.youku.com/v_show/id_XNjM3NjkwOTg4.html?spm=a2h1n.8251845.0.0
