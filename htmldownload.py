# coding=utf-8
import urllib2
from time import sleep
import cookielib
import random
import winsound
import requests
from requests.exceptions import ConnectionError
class HtmlDownload(object):
    def getHTMLText(self,url):
        # headers = {
        #
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        # }
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)

        except :
            return ""
        if response.getcode() == 200:
            return response.read()
        else:
            print '网页错误'
            return ""

