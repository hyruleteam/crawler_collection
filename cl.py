# coding:UTF-8
import requests
from datetime import datetime
import time
import urllib
import re
import os
import sys
import json
import random

from random import choice
from bs4 import BeautifulSoup

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

url = input("请输入要下载的网址：")

FILE_PATH= "result/cl/"
data = {}

def httpGet(url):
    session= requests.Session()
    session.headers= {
        'User-Agent': choice(UA_LIST),
    }

    proxies = { "http": "http://127.0.0.1:1087", "https": "http://127.0.0.1:1087", } 

    page = session.get(url,timeout=30000,proxies=proxies)
    page.encoding='GBK'

    soup = BeautifulSoup(page.text, features="html.parser")

    # 如果遇到报错，建议开启延时执行
    # try:
    #     time.sleep(1)
    # except:
    #     print('error')

    return soup;

def getContent():
    http_text = httpGet(url)

    title = http_text.select('title')[0].get_text().split('-')[0]
    file_path = FILE_PATH + title

    if os.path.isdir(file_path):
        pass
    else:
        print("\033[0;32;40m创建文件夹:"+title+"\033[0m")
        os.mkdir(file_path)

    img_list = http_text.select('input[type="image"]');

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', choice(UA_LIST))]
    urllib.request.install_opener(opener)

    print("共" + str(len(img_list)) + "张图片需要下载")

    for item in range(0,len(img_list)):
        print("\033[0;31;40m下载第" + str(item + 1) + "张图片\033[0m")
        src = img_list[item]["data-src"]
        path = file_path + '/' + str(src).split("/")[-1]
        urllib.request.urlretrieve(src, path)

    print("\033[0;37;42m下载完成\033[0m")


if __name__ == '__main__':
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    getContent()

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
