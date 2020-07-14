# GeekbangCrawler
~~极客时间爬虫(仅供内部环境使用!).另外会不定期更新相关课程数据库~~
已经失效，极客时间已使用阿里云验证

# 安装requirements.txt依赖

```
pip install -r requirements.txt
```

 **还需要ffmpeg , 自行安装**

# 课程数据库写入

```
python geekMain.py -cid 课程地址 (-dp 本地下载地址,可选,默认默认程序根目录 'course' 文件夹下)
```

# 课程爬取

```
 python geekCourseDownloader.py -db 数据库地址 (-dp 本地保存地址,默认程序根目录,可选,默认默认程序根目录 'course' 文件夹下) (-q 视频质量,默认HD,可选 SD LD HD)
```
