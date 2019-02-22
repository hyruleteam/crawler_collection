#!/usr/bin/env python

import requests
from datetime import datetime
import time
import urllib
import re
import os
import sys

offset = -1
question_id = input("请输入问题id:")  # 需要爬取的问题id
answer_num = 100  # 需要爬取的回答个数
FILE_PATH = '你的脚本路径' + question_id


def download_pic(offset_num):
    if not question_id:
        sys.exit(0)
    else:
        url = 'https://www.zhihu.com/api/v4/questions/' + question_id + '/answers?include=content&limit=1&offset=' + str(
            offset_num) + '&sort_by=default'  # 需要爬数据的网址

        session = requests.Session()
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        page = session.get(url, timeout=30000)

        content = page.json()['data'][0]['content']

        result = re.findall('data-original|data-actualsrc="(.*?)"', content)

        if os.path.isdir(FILE_PATH):
            pass
        else:
            print('创建文件夹' + question_id)
            os.mkdir(FILE_PATH)

        for index in range(len(result)):
            if result[index] != '':
                path = FILE_PATH + '/' + \
                    str(offset_num) + '_' + str(index) + ".jpg"
                urllib.request.urlretrieve(result[index], path)
                print('下载第' + str(offset_num) + '条的第' + str(index) + '张')


# 每n秒执行一次
def timer(n):
    global offset
    while offset < int(answer_num):
        offset = offset + 1

        download_pic(offset)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=======================")
        print("五秒钟后执行下一个")
        print("=======================")

        time.sleep(n)


timer(5)