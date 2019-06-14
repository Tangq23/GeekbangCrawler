import sqlite3
import argparse
import os
import re
import requests
import html2text
from geekCourseFileOperator import geekCourseFileOperator

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", "--dbpath", help="数据库地址")
    parser.add_argument("-dp", "--dlpath", help="download path,本地保存地址,默认程序根目录")
    parser.add_argument("-q", "--quality", help="视频质量,默认HD,可选 SD LD HD")
    args = parser.parse_args()

    if args.dbpath is None :
        print('请输入数据库地址')
        exit()

    if args.dlpath:
        geekCourseFileOperator = geekCourseFileOperator()
        geekCourseFileOperator.set_rootDirPath(args.dlpath)

    dbPath = args.dbpath
    fileOperator = geekCourseFileOperator()

    if fileOperator.filePathExist(dbPath) is False:
        print('数据库地址不存在')
        exit()
    path = os.path.realpath(dbPath)
    print(path)
    conn = sqlite3.connect(dbPath)
    conn.row_factory = dict_factory
    c = conn.cursor()

    sqlString = '''SELECT * FROM Course'''
    c.execute(sqlString)
    res = c.fetchall()
    if len(res) == 0:
        print('数据库空')
        c.close()
        conn.close()
        exit()

    c.close()
    conn.close()

    firstCourse = res[0]
    fileOperator.set_courseName(firstCourse['CID'])

    quality = 'HD'
    if args.quality == 'HD':
        quality = 'HD'
    elif args.quality == 'SD':
        quality = 'SD'
    elif args.quality == 'LD':
        quality = 'LD'

    for dataInfo in res:

        if (dataInfo is not None) and (isinstance(dataInfo, dict) == True):
            titleName = dataInfo['COURSETITLE']
            fileName = re.sub('[\/:*?"<>|]', '-', titleName)  # 去掉非法字符
            fileName = ''.join(fileName.split())
            if 'CONTENT' in (dict(dataInfo)).keys() and (dataInfo['CONTENT'] is not None) and (
            isinstance(dataInfo['CONTENT'], str)):
                markdownPath = '%s.md' % (os.path.join(fileOperator.get_downloadPath(), fileName))
                # print(markdownPath)
                if fileOperator.filePathExist(markdownPath) == False:
                    with open(markdownPath, 'w') as f:
                        f.write(html2text.html2text(dataInfo['CONTENT']))


            if 'PRODUCTTYPE' in (dict(dataInfo)).keys()  and dataInfo["PRODUCTTYPE"] == 'c3':
                qualityString = 'VIDEO%sURL'%quality
                print(qualityString)
                if (qualityString in (dict(dataInfo)).keys()) and   (dataInfo[qualityString] is not None) and (
            isinstance(dataInfo[qualityString], str)):
                    # 视频
                    videoPath = '%s.mp4' % (os.path.join(fileOperator.get_downloadPath(), fileName))
                    downloadCommand = 'ffmpeg -i %s %s '%(dataInfo[qualityString],videoPath)
                    # print(downloadCommand)
                    os.system(downloadCommand)
                else:
                    print('不存在此质量视频')
            else:
                #音频
                if 'AUDIOURL' in (dict(dataInfo)).keys() and (dataInfo['AUDIOURL'] is not None) and (
                        isinstance(dataInfo['AUDIOURL'], str) and (len(dataInfo['AUDIOURL']) > 0)):
                    audioURL = dataInfo['AUDIOURL']
                    audioPath = '%s.mp3' % (os.path.join(fileOperator.get_downloadPath(), fileName))
                    audioRequest = requests.get(audioURL, stream=True)
                    if fileOperator.filePathExist(audioPath) == False:
                        with open(audioPath, 'wb+') as audio:
                            for chunk in audioRequest.iter_content(chunk_size=1024):
                                if chunk:
                                    audio.write(chunk)

