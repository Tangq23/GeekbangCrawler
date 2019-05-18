import argparse
from geekCourseSeeker import *
from geekCourseFileOperator import geekCourseFileOperator

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-cid", help ="input course id to Download,课程地址")
    parser.add_argument("-dp","--dlpath",help ="download path,本地保存地址,默认程序根目录")
    args = parser.parse_args()
    if args.dlpath:
        geekCourseFileOperator = geekCourseFileOperator()
        geekCourseFileOperator.set_rootDirPath(args.dlpath)

    if args.cid:
        courseSeeker = geekCourseSeeker()
        courseSeeker.findCourse(args.cid)
