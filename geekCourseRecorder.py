import requests
import os
from geekCourseFileOperator import geekCourseFileOperator
from geekCourseInfoModel import geekCourseInfoModel
import html2text
import re
class geekCourseRecorder:
    def __init__(self):
        #每个课程中的子课程
        self.uniqueCourseID = ''
        self.operator = geekCourseFileOperator()
        
    def startDownloadCourse(self,uniqueCourseID):
        if uniqueCourseID is None:
            return
        self.uniqueCourseID = str(uniqueCourseID)
        courseURL = 'http://time.dev.geekbang.org/serv/v1/article'

        headers = {
            'Host': 'time.dev.geekbang.org',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-cn',
            'Content-Type': 'application/json',
            'Origin': 'http://time.dev.geekbang.org',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',

        }

        data = '{"id":%s}' % uniqueCourseID
        r = requests.post(courseURL, data=data, headers=headers)
        dict = r.json()
        return dict['data']


    def saveInfoToDisk(self, dataInfo):
        if (dataInfo is not None) and (isinstance(dataInfo, dict) == True):
            titleName = dataInfo['article_title']
            fileName = re.sub('[\/:*?"<>|]', '-', titleName)  # 去掉非法字符
            if (dataInfo['article_content'] is not None) and (isinstance(dataInfo['article_content'],str)):
                markdownPath = '%s.md'%(os.path.join(self.operator.get_downloadPath(),fileName))
                print(markdownPath)
                if self.operator.filePathExist(markdownPath) == False:
                    with open(markdownPath,'w') as f:
                        f.write(html2text.html2text(dataInfo['article_content']))

            if (dataInfo['audio_download_url'] is not None) and (isinstance(dataInfo['audio_download_url'], str) and (len(dataInfo['audio_download_url']) > 0)):
                audioURL = dataInfo['audio_download_url']
                audioPath = '%s.mp3'%(os.path.join(self.operator.get_downloadPath(),fileName))
                audioRequest = requests.get(audioURL,stream=True)
                if self.operator.filePathExist(audioPath) == False:
                    with open(audioPath,'wb+') as audio:
                        for chunk in audioRequest.iter_content(chunk_size=1024):
                            if chunk:
                                audio.write(chunk)
                                # f.flush()