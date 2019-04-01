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
import managedb
import htmldownload
reload(sys)
sys.setdefaultencoding("utf-8")

class MongoTV(object):
    def __init__(self):
        self.managedb=managedb.ManageDB()#数据库操作
        self.htmldown=htmldownload.HtmlDownload()#网页下载器
    def parsePage(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.find_all('li', class_='m-result-list-item')

        for i in lis:
            url = 'https:' + i.a['href']
            imgurl = re.search('img alt.*?src="(.*?)">', str(i), re.S)

            # print i.a['href']
            btn = 'https:' + i.a['href']
            show = i.a['href'][17:]
            # print show[6:7] #327926/5338179.html
            coungtj = 0
            for j in range(0, len(show) - 1):
                if show[j:j + 1] == '/':
                    countj = j
                    break
            urlid = show[0:countj]
            print urlid

            url_detail = 'https://www.mgtv.com/h/' + str(urlid) + '.html?fpa=se'  # 视频页面详情https://www.mgtv.com/h/157.html?fpa=se     搜索
            html = self.htmldown.getHTMLText(url_detail)
            #    print url_detail
            if html == "":
                continue
            # print str(imgurl.group(1))
            data = self.parsetvinfo(html, str(imgurl.group(1)), btn)
            self.managedb.findtvshowmongotv(data)

    def parsetvinfo(self,html, picurl, btn):
        data = {}
        alltypedict = []
        allfrmotvdict = []
        allacctordict = []
        allareadict = []
        soup = BeautifulSoup(html, 'html.parser')
        detail = soup.find('div', class_='v-meta v-meta-album')
        if soup.find('span', class_='status'):
            update = soup.find('span', class_='status')
            data['update'] = update.b.string
            # print '更新时间',update.b.string
        else:
            data['update'] = 'null'

        # 类型
        if re.search('<em class="label">类型</em>(.*?)</p>', str(detail), re.S):
            alltype = re.search('<em.*?类型</em>(.*?)</p>', str(detail), re.S)
            type = re.findall('<a .*?>(.*?)</a>', str(alltype.group(1)), re.S)
            for i in type:
                alltypedict.append(i)
            # print  i
            data['type'] = alltypedict
        else:
            data['type'] = 'null'
        # 播出
        if re.search('<em class="label">播出</em>(.*?)</p>', str(detail), re.S):
            allfromtv = re.search('<em class="label">播出</em>(.*?)</p>', str(detail), re.S)
            fromtv = re.findall('<a .*?>(.*?)</a>', str(allfromtv.group(1)), re.S)
            for i in fromtv:
                allfrmotvdict.append(i)
                # print i
            data['fromty'] = allfrmotvdict
        else:
            data['fromty'] = 'null'
        # 主持
        if re.search('<em class=".*?">主持人</em>(.*?)</p>', str(detail), re.S):
            allactor = re.search('<em class=".*?">主持人</em>(.*?)</p>', str(detail), re.S)
            actor = re.findall('<a .*?>(.*?)</a>', str(allactor.group(1)), re.S)
            for i in actor:
                allacctordict.append(i)
                # print i
            data['actor'] = allacctordict
        else:
            data['actor'] = 'null'
        # 地区
        if re.search('<em class=".*?">地区</em>(.*?)</p>', str(detail), re.S):
            allarea = re.search('<em class=".*?">地区</em>(.*?)</p>', str(detail), re.S)
            area = re.findall('<a .*?>(.*?)</a>', str(allarea.group(1)), re.S)
            for i in area:
                allareadict.append(i)
                # print i
            data['area'] = allareadict
        else:
            data['area'] = 'null'
        # 内容
        if re.search('<em class=".*?">简介</em>.*?<span>(.*?)</span>.*?</p>', str(detail), re.S):
            content = re.search('<em class=".*?">简介</em>.*?<span>(.*?)</span>.*?</p>', str(detail), re.S)
            # print content.group(1)
            data['content'] = '简介：' + content.group(1)
        else:
            data['content'] = 'null'
        # 片名
        if re.search('<h1 class="title"><span>(.*?)</span></h1>', str(soup), re.S):
            name = re.search('<h1 class="title".*?<span>(.*?)</span></h1>', str(soup), re.S)
            # print name.group(1)
            data['name'] = name.group(1)
        else:
            data['name'] = 'null'
        #   图片路径
        name = str(data['name'])
        data['pic'] = 'C:/Users/Administrator/Desktop/pic/mongotv/' + name + '.jpg'
        data['picurl'] = 'http:' + picurl
        # 播放地址
        data['btn'] = btn

        return data
    def findpage(self,html):
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        lis = soup.find('div', class_='w-pages w-pages-default ').find('ul')
        lilist = []  # 用来装li标签的
        for li in lis:
            lilist.append(li)
        length = lilist[-2].string
        # 因为[-1]是“下一页,所以[-2]是当前最大页，也就是每一个类别到底有多少页”
        #print("页码数："+lilist[-2].string)
        # print("this is findpage")
        return length
    def action(self):
        starttime = datetime.datetime.now()
        print("爬取芒果tv内王牌综艺、大咖秀场、亲子所有的综艺节目")
        url1='https://list.mgtv.com/1/'
        url2='--------c1-1---.html?channelId=1'
        url3='--------c1-'
        type=['179-a1']#亲子、大咖秀、王牌
        #type=['179-a1','5-a1','4-a1']#亲子、大咖秀、王牌
        for j in type:
            html=url1+str(j)+url2
            #print html
            thtml = self.htmldown.getHTMLText(html)
            length=int(self.findpage(thtml))
            for i in range(1, length + 1):
                #https://list.mgtv.com/1/4-a1--------c1-1---.html?channelId=1
                #https://list.mgtv.com/1/4-a1--------c1-2---.html?channelId=1
                urlpage =url1+str(j)+url3+ str(i) + '---.html?channelId=1'

                thtml = self.htmldown.getHTMLText(urlpage)
                self.parsePage(thtml)

        endtime = datetime.datetime.now()
        print"运行时间为：",(endtime - starttime).total_seconds()
if __name__ == "__main__":
    mongotv=MongoTV()
    mongotv.action()

