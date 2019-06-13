import time
import requests
import random
import json
from geekCourseDBManager import geekCourseDBManager
from geekCourseFileOperator import geekCourseFileOperator
from geekCourseRecorder import geekCourseRecorder

class geekCourseSeeker:
    def __init__(self):
        self.courseID = ""
        self.referID = ""


    #courseID 与 跳转ID 都需要传进来
    def findCourse(self,courseID):
        if (isinstance(courseID,str) == False) or (courseID is None):
            return
        self.courseID = courseID

        #根据courseID寻找
        courseURL = 'http://time.dev.geekbang.org/serv/v1/column/articles'


        '''
        需要配置 Post JSON 数据
        {
        cid:courseID,
        order:earliest //排列顺序
        
        }
        
        header 可以模拟下浏览器
        {
        Referer:referURL,
        Content-Type:application/json
        User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36
        }
        '''

        headers = {
            'Host': 'time.dev.geekbang.org',
            'Accept':'application/json, text/plain, */*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-cn',
            'Content-Type': 'application/json',
            'Origin':'http://time.dev.geekbang.org',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',

        }

        print(courseURL)
        data = '{"cid":%s,"order":"earliest","size":100}'%self.courseID
        r = requests.post(courseURL, data = data , headers = headers)
        dict = r.json()
        print('课程总数:%s'%len(dict['data']['list']))

        #不是用多线程下载了.以免有不良后果
        fileOperator = geekCourseFileOperator()
        fileOperator.set_courseName(self.courseID)
        dbManager = geekCourseDBManager()
        dbManager.startConfig()
        dbManager.beginCommit()

        # for courseInfo in range(len(dict['data']['list'])-1,-1,-1):
        #     courseInfo = dict['data']['list'][courseInfo]

        for courseInfo in dict['data']['list']:
            if courseInfo['id'] is not None:
                downloader = geekCourseRecorder()
                infoDict = downloader.startDownloadCourse(courseInfo['id'])
                if infoDict is not None:
                    dbManager.startRecord(infoDict)
                    # 抽离出不带下载功能
                    # downloader.saveInfoToDisk(infoDict)


                #随机延时增强现实感
                time.sleep(4)
        dbManager.endCommit()