# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import redis
reload(sys)
sys.setdefaultencoding('utf-8')
class RedisManage(object):
    def __init__(self):

        self.pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
        self.rdb = redis.Redis(connection_pool=self.pool)
        # client = pymongo.MongoClient('localhost')
        # db = client['TY']
        # self.youkuCol=db.youku
    def action(self):
        dict={''}
        self.rdb.set('gender', 'male')     # key是"gender" value是"male" 将键值对存入redis缓存
        print(self.rdb.get('gender'))      # gender 取出键male对应的值

if __name__ == "__main__":
    mongotv=RedisManage()
    mongotv.action()