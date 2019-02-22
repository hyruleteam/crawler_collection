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
token = '/wEPDwULLTE5MDQ3MzMzNzMPZBYCAgMPZBYEAgsPFgIeC18hSXRlbUNvdW50Ag8WHmYPZBYCZg8VCQIzOQkyMDExMDYwMjACMzkG6KeC6YK4AjMjBzk4MzAuMzcCOTkJMTEsMzE2LjE0AGQCAQ9kFgJmDxUJAjUzCTIwMTEwNjAyMwI1MwznmofpqazoirHlm60OMzgsNDIsNDMsNDQsNDUIMTQ4NjkuNDQDMTMzCDUsNDkwLjQ2AGQCAg9kFgJmDxUJAjM0CTIwMTEwNjAxNwIzNBLmmJPlsYXlkIzovonljJfoi5EDMTYjCDEyNzUwLjkxAzIzNgg3LDg0Ni4wOABkAgMPZBYCZg8VCQI1MAkyMDExMDYwMTYCNTAM5Lmm6aaZ6Zeo56ysAjkjCDI2MzgwLjA4AzI3Mgg3LDAzMS44NABkAgQPZBYCZg8VCQI0MwkyMDExMDYwMTUCNDMS5Y2X6Imz5rmW55WU5bCP5Yy6AjEzCDI1MTQ0Ljk2AzI2NAg2LDMyNC45NgBkAgUPZBYCZg8VCQI0NQkyMDExMDYwMTkCNDUS5oGS55ub55qH5a626Iqx5ZutBTIjLDQjCDQxMDM1LjcxAzM4NAg1LDUxOC45OABkAgYPZBYCZg8VCQIzNQkyMDExMDYwMTMCMzUM5aSn5a+M57u/5rSyATgIMjA5NTguOTQDMjE2CDYsNTUwLjc2AGQCBw9kFgJmDxUJAjM4CTIwMTEwNjAxOAIzOAzlpKflr4znu7/mtLIFNyw2LDUIMzU1MjQuODgDMzA2CDYsOTkxLjM5AGQCCA9kFgJmDxUJAjQ0CTIwMTEwNjAxMgI0NAnmmIrlpKnlm60GMzAj5qW8CDE1OTA0LjU2AzE3NAg2LDAwMi40NABkAgkPZBYCZg8VCQIyMAkyMDExMDYwMDcCMjAM6YeR5rW36Iqx5ZutATYHOTAyMi42MgI5MAg2LDI5NC45OQBkAgoPZBYCZg8VCQE2CTIwMTEwNjAxMQE2DOWkqemqj+iKseWbrQMxMCMIMjM3MDkuODADMjMxCDcsMDUyLjE3AGQCCw9kFgJmDxUJAjI1CTIwMTEwNjAwOAIyNRPkv6Hovr4u5rC05bK46IyX6YO9BzEzIywxNyMIMTQyNjIuNjIDMTMwCDcsMjE0LjIxAGQCDA9kFgJmDxUJAjQyCTIwMTEwNzAwNAI0Mhjnu7/ln47nv6Hnv6DmuZbnjqvnkbDlm60PMTEj5rOV5byP5ZCI6ZmiBzc5MDkuNjACMTIJMjUsMDI5Ljg5AGQCDQ9kFgJmDxUJAjQwCTIwMTEwNjAwOQI0MAzph5HoibLlkI3pg6EBOQgyMjAyNC4yNgMxMjQJMTAsNDMxLjM4AGQCDg9kFgJmDxUJAjEzCTIwMTEwNjAxMAIxMxzlh6Tlh7Dln44/5a625a625pmv5Zut5Zub5pyfAkE3CDEwMTE3LjQ0AzEwOAg2LDk1MC41NgBkAg0PDxYEHgtSZWNvcmRjb3VudAL7FB4QQ3VycmVudFBhZ2VJbmRleAKyAWRkZAprHYx2dSVKpGJdGfrVokc/iqCm'


wb = Workbook()
sheet = wb.create_sheet()
filename = datetime.now().strftime("%Y-%m-%d")
print(filename)
def download_lp_info(offset):
    url = 'http://220.178.124.94/fangjia/ws/DefaultList.aspx'

    session = requests.Session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    payload = {'__EVENTARGUMENT':str(offset),'__VIEWSTATE':token,'__EVENTTARGET':'AspNetPager1'}
    page = session.post(url, data = payload, timeout=30000)

    soup = BeautifulSoup(page.text, features="html.parser")
    
    data = []
    tr_list = soup.find_all('tr')
    tr_list_len = len(tr_list)
    tr_list_true = []

    if tr_list_len<18:
        tr_list_true = tr_list[2:tr_list_len]
    else:
        tr_list_true = tr_list[2:17]

    for link in tr_list_true:
        data1 = link.find_all('td')[0].a.getText().strip()
        data2 = link.find_all('td')[1].a.getText().strip()
        data3 = link.find_all('td')[2].getText().strip()
        data4 = link.find_all('td')[3].getText().strip()
        data5 = link.find_all('td')[4].getText().strip()
        data6 = link.find_all('td')[5].getText().strip()
        data7 = link.find_all('td')[6].getText().strip()

        arr = [data1,data2,data3,data4,data5,data6,data7]
        sheet.append(arr)

    wb.save(filename+'.xlsx')

# 每n秒执行一次
def timer(n):
    global offset
    while offset < 179:
        offset = offset + 1

        download_lp_info(offset)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=======================")
        print("1秒钟后执行下一个")
        print("=======================")

        time.sleep(n)


if __name__ == '__main__':
    timer(1)