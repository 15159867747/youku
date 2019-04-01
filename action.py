# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import youku20190327,mongotv20190329
import datetime
import threading
reload(sys)
sys.setdefaultencoding('utf-8')
class Action(object):
    def __init__(self):
        self.youku=youku20190327.Youku()
        self.mongotv=mongotv20190329.MongoTV()
    def timeAction(self):
        begin=datetime.datetime.now()
        print '当前时间：',begin
        self.timer("00:00:00")#明天0点开始爬取
        endtime=datetime.datetime.now()
        print '结束时间',endtime

        timer = threading.Timer(86400,self.timeAction)#d
        timer.start()
    def timer(self,time):
        # 获取现在时间
        now_time = datetime.datetime.now()
        # 获取明天时间
        next_time = now_time + datetime.timedelta(days=+1)
        next_year = next_time.date().year
        next_month = next_time.date().month
        next_day = next_time.date().day
        # 获取明天3点时间
        next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" "+str(time), "%Y-%m-%d %H:%M:%S")
        #   # 获取昨天时间
        # last_time = now_time + datetime.timedelta(days=-1)

        # 获取距离明天3点时间，单位为秒
        timer_start_time = (next_time - now_time).total_seconds()
        print(timer_start_time)
        # 54186.75975


        #定时器,参数为(多少时间后执行，单位为秒，执行的方法)
        timer = threading.Timer(timer_start_time, self.mongotv.action)
        timer.start()

if __name__ == "__main__":
    action=Action()
    action.timeAction()











