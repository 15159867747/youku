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
import managedb
import htmldownload
reload(sys)
sys.setdefaultencoding("utf-8")
class Youku(object):
    def __init__(self):
        self.managedb=managedb.ManageDB()#数据库操作
        self.htmldown=htmldownload.HtmlDownload()#网页下载器
    def parsePage(self,namelist, html):
        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.find_all('li', class_='title')

        for i in lis:
            namelist.append(i.a.string)
            url = 'https:' + i.a['href']
            show=i.a['href']
            str2 = "list"
            html = self.htmldown.getHTMLText(url)


            if html == "":
                continue
            if url[8:12] == str2:
                data=self.parsetvinfo(html, i.a.string,show)  # 解析url中信息，主持人、地区、类型
                self.managedb.findtvshowyouku(data)

            else:
                url = self.parsetv(html)  # 获取简介的url
                if url:
                    html = self.htmldown.getHTMLText('https:' + url)
                    data = self.parsetvinfo(html, i.a.string,show)  # 解析url中信息，主持人、地区、类型
                    self.managedb.findtvshowyouku(data)
    def parsetvinfo(self,html, name,show):

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
    # 该函数是用来查找每一个类别有多少页
    def findpage(self,html):
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
    def parsetv(self,html):
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        if soup.find('div', class_='tvinfo'):
            lis = soup.find('div', class_='tvinfo')
            # print lis.a['href']
            return lis.a['href']
    # //list.youku.com/show/id_z8a031cd4f8cc11e2b8b7.html


    def action(self):
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
            thtml = self.htmldown.getHTMLText(turl)
            length = int(self.findpage(thtml))
            # print(str(trueyear)+"有"+str(length)+"页")
            for i in range(1, length + 1):
                url = url1 + str(j) + url2 + url3 + str(i) + url4
                #   print(url)
                # print("这是{0}年第{1}页的内容".format(trueyear,i))
                html = self.htmldown.getHTMLText(url)
                self.parsePage(namelist, html)
            #printNameList(namelist, j)
            namelist = []

        endtime = datetime.datetime.now()
        print("运行时间为：{}".format(endtime - starttime))
if __name__ == "__main__":
    youku=Youku()
    youku.action()
