import sqlite3
import os
from  geekCourseFileOperator import geekCourseFileOperator

class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

@Singleton
class geekCourseDBManager(object):
    def __init__(self):
        self.fileOperator = geekCourseFileOperator()
        pass

    def startConfig(self):
        self.dbPath = os.path.join(self.fileOperator.get_downloadPath(),'course.db')

        conn = sqlite3.connect(self.dbPath)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Course
               (id          INTEGER           PRIMARY KEY     AUTOINCREMENT,
               PRODUCTTYPE    TEXT,
               CID            TEXT,
               SUBCID         TEXT,
               COURSETITLE    TEXT,
               AUTHOR         TEXT,
               SUMMARY        TEXT,
               CONTENT        TEXT,
               AUDIOURL       TEXT,
               AUDIOTIME      TEXT,
               VIDEOHDURL     TEXT,
               VIDEOHDSIZE    TEXT,
               VIDEOSDURL     TEXT,
               VIDEOSDSIZE    TEXT,
               VIDEOLDURL     TEXT,
               VIDEOLDSIZE    TEXT
               
               );''')
        print("Table created successfully")
        conn.commit()
        conn.close()

    def beginCommit(self):
        self.conn =  sqlite3.connect(self.dbPath)
        self.cursor = self.conn.cursor()

    def endCommit(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def startRecord(self,infoDict):
        if (infoDict is None) or isinstance(infoDict,dict) == False:
            return
        sqlString = '''SELECT * FROM Course where SUBCID = %s ''' % str(infoDict['id'])
        self.cursor.execute(sqlString)
        res = self.cursor.fetchall()


        cid = infoDict['cid']
        #产品类型 c1 音频+文字 c3 视频
        productType = infoDict['product_type']
        subcid = infoDict['id']
        articleTitle = infoDict['article_title']
        authorName = infoDict['author_name']
        summary = infoDict['article_summary']
        content = infoDict['article_content']
        audioURL = infoDict['audio_download_url']
        audioTime = infoDict['audio_time']

        videoHDURL = ''
        videoHDSize = ''
        videoSDURL = ''
        videoSDSize = ''
        videoLDURL = ''
        videoLDSize = ''
        if productType == 'c3':
            videoHDURL = infoDict['video_media_map']['hd']['url']
            videoHDSize = infoDict['video_media_map']['hd']['size']
            videoSDURL = infoDict['video_media_map']['sd']['url']
            videoSDSize = infoDict['video_media_map']['sd']['size']
            videoLDURL = infoDict['video_media_map']['ld']['url']
            videoLDSize = infoDict['video_media_map']['ld']['size']




        if len(res) == 0:
            #不存在数据,插入
            print('Insert')
            self.cursor.execute(u'insert into Course (PRODUCTTYPE,CID,SUBCID,COURSETITLE,AUTHOR,SUMMARY,CONTENT,AUDIOURL,AUDIOTIME,VIDEOHDURL,VIDEOHDSIZE,VIDEOSDURL,VIDEOSDSIZE,VIDEOLDURL,VIDEOLDSIZE) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(productType,cid,subcid,articleTitle,authorName,summary,content,audioURL,audioTime,videoHDURL,videoHDSize,videoSDURL,videoSDSize,videoLDURL,videoLDSize))
        else:
            # 存在数据,更新
            print('Update')
            self.cursor.execute(u'update Course set PRODUCTTYPE = ? , CID = ? ,COURSETITLE = ? ,AUTHOR = ? ,SUMMARY = ? ,CONTENT = ? ,AUDIOURL = ? ,AUDIOTIME = ? , VIDEOHDURL = ? , VIDEOHDSIZE = ? , VIDEOSDURL = ? , VIDEOSDSIZE = ? , VIDEOLDURL = ? , VIDEOLDSIZE = ? where SUBCID = ?',(productType,cid,articleTitle,authorName,summary,content,audioURL,audioTime,subcid,videoHDURL,videoHDSize,videoSDURL,videoSDSize,videoLDURL,videoLDSize))
        self.conn.commit()

