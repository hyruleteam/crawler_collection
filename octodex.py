import requests
from datetime import datetime
import time
import urllib
import re
import os
import sys
from bs4 import BeautifulSoup
from openpyxl import Workbook

offset = 0
FILE_PATH = "/Users/wenyu/Documents/work_project/github/wenyuking/python_code/oct"
def download_lp_info(offset):
    url = 'https://octodex.github.com'

    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    # payload = {'__EVENTARGUMENT':str(offset),'__VIEWSTATE':token,'__EVENTTARGET':'AspNetPager1'}
    page = session.get(url,timeout=30000)

    soup = BeautifulSoup(page.text, features="html.parser")
    
    data = []
    img_list = soup.find_all("a", class_="preview-image")

    if os.path.isdir(FILE_PATH):
        pass
    else:
        print('创建文件夹')
        os.mkdir(FILE_PATH)

    for item in img_list:
        src = item.img["data-src"]
        path = FILE_PATH + str(src)
        urllib.request.urlretrieve(url + src, path)


# 每n秒执行一次
def timer(n):
    global offset
    while offset < 1:
        offset = offset + 1

        download_lp_info(offset)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=======================")
        print("1秒钟后执行下一个")
        print("=======================")

        time.sleep(n)


if __name__ == '__main__':
    timer(1)