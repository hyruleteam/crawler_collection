# coding=utf-8
import requests
from datetime import datetime
import time
import urllib
import re
import os
import sys
import json
from bs4 import BeautifulSoup

data = []
FILE_PATH = "/"
def download_info():
    url = 'http://youxi.029815.cn/down/yxdownvip.html'

    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    # payload = {'__EVENTARGUMENT':str(offset),'__VIEWSTATE':token,'__EVENTTARGET':'AspNetPager1'}
    page = session.get(url,timeout=30000)
    page.encoding='utf-8'

    soup = BeautifulSoup(page.text, features="html.parser")

    # print(soup.prettify())

    file = open('data.json','w')
    for content in soup.select('span > p'):
        urlstr = content.select('a')
        if len(urlstr)>0:
            click_url = urlstr[0].get('onclick')
            if click_url and len(click_url) > 0:
                url = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')",click_url)
                data.append({
                    'content':content.get_text().strip().replace("\n", ""),
                    'url':url[0]
                })
                # print(content.get_text().strip().replace("\n", ""))
                # print(url[0])
                # print("====================")
    
    file.write(json.dumps(data))
    file.close();
    print("执行完毕")


if __name__ == '__main__':
    download_info()