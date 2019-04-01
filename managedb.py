# coding=utf-8
import sys
import pymongo
from pyExcelerator import *
import urllib2
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')

class ManageDB(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost')
        db = client['TY']
        self.youkuCol=db.youku

    def findtvshowyouku(self,data):
        if data is  None:
            print '数据为空'
            return
        updatetime = data['update']
        name=data['name']
        print name
        if name:
            doc =self.youkuCol.find_one({'name':name})
            if doc:
                if str(doc['update']) == str(updatetime):
                    print '该剧目前没有更新XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                else:
                    self.youkuCol.update({'update': doc['update'], 'name': name}, {"$set": {'update': updatetime}})
                    print '该剧有更新√√√√√√更新√√√√√√'
            else:
                urllib.urlretrieve(data['picurl'], data['pic'])
                self.youkuCol.insert(data)
                print '录入新数据************新节目*************'
    def findtvshowmongotv(self,data):
        if data is  None:
            print '数据为空'
            return
        updatetime = data['update']
        print updatetime
        name=data['name']
        print name
        if name:
            doc =self.youkuCol.find_one({'name':name})

            if doc:
                if str(doc['update']) == str(updatetime):
                    print '该剧目前没有更新XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                else:
                    self.youkuCol.update({'update': doc['update'], 'name': name}, {"$set": {'update': updatetime}})
                    print '该剧有更新√√√√√√√更新√√√√√√√'
            else:
                urllib.urlretrieve(data['picurl'],r'C:/Users/Administrator/Desktop/pic/mongotv/' + unicode(name) + '.jpg')
                self.youkuCol.insert(data)
                print '录入新数据************* 新节目***************'

