#!/usr/bin/env python

import requests
from datetime import datetime
import time
import urllib
import re
import os
import sys

from random import choice

UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)", 
]

offset = -1
question_id = input("请输入问题id:")  # 需要爬取的问题id
answer_num = 100  # 需要爬取的回答个数
FILE_PATH = 'result/octodex/' + question_id


def download_pic(offset_num):
    if not question_id:
        sys.exit(0)
    else:
        url = 'https://www.zhihu.com/api/v4/questions/' + question_id + '/answers?include=content&limit=1&offset=' + str(
            offset_num) + '&sort_by=default'  # 需要爬数据的网址

        session = requests.Session()
        session.headers= {
            'User-Agent': choice(UA_LIST),
        }
        page = session.get(url, timeout=30000)

        content = page.json()['data'][0]['content']

        result = re.findall('data-original|data-actualsrc="(.*?)"', content)

        if os.path.isdir(FILE_PATH):
            pass
        else:
            print('创建文件夹' + question_id)
            os.mkdir(FILE_PATH)

        # opener = urllib.request.build_opener()
        # opener.addheaders = [('User-agent', choice(UA_LIST))]
        # urllib.request.install_opener(opener)

        for index in range(len(result)):
            if result[index] != '':
                path = FILE_PATH + '/' + str(result[index]).split("/")[-1]
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