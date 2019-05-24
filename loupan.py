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
token = '/wEPDwULLTE5MDQ3MzMzNzMPZBYCAgMPZBYEAgsPFgIeC18hSXRlbUNvdW50AgoWFGYPZBYCZg8VCQQ1OTE3CTIwMTkwMTAwNAQ1OTE3DOW8gOWFg+WFrOmmhh8x5Y+35qW8LDLlj7fmpbwsM+WPt+alvCw15Y+35qW8CDM4MDE4LjE2AzM0NgkxMCw0OTkuODIEMC4wMGQCAQ9kFgJmDxUJBDU4NjAJMjAxODEyMDU2BDU4NjAQ6J6N5a6B5bqcSuWcsOWdlwUxLDIsMwg0Nzg1OC4yNAMzNzYJMTcsMjAwLjAwCjYzNiw0MTIuNzdkAgIPZBYCZg8VCQQ1ODM5CTIwMTgxMjA1NQQ1ODM5DOaCpumDveWFrOmmhgcxMSMsMjIjCDEzODUxLjUyAzEyMgkxMiw3ODEuNTIKMjI3LDA3NC4xMGQCAw9kFgJmDxUJBDU4MjMJMjAxODEyMDU0BDU4MjMM5pe25Luj6ZSm5ZutCTEjLDIjLDE3IwgzMDg0OS4xMAMyNjgJMTIsODE2LjgxCjIyOCwyMzAuNDRkAgQPZBYCZg8VCQQ1ODk4CTIwMTgxMjA0MAQ1ODk4EuS4lue6quiNo+W7t+Wwj+WMugIzOQgyMzM4Ny44NAMyMjQIOSw4NzcuMzgEMC4wMGQCBQ9kFgJmDxUJBDU4MjAJMjAxODEyMDM2BDU4MjAJ6b6Z5bed6YeMEDksMTAsNiw3LDgsMTEsMTIIODMyMzUuNjEDNzc4CTE1LDk5OS44OQQwLjAwZAIGD2QWAmYPFQkENTg4NAkyMDE4MTIwMzUENTg4NAznv6HnjonlhazppoYHQi04LEItOQc5MDY5LjY0AjQ4CTIwLDk5OC4zOAQwLjAwZAIHD2QWAmYPFQkENTg4MQkyMDE4MTIwMjYENTg4MQzplKbnhpnpm4Xoi5EgMiMsOCMsMTAjLDExIywxMiMsMyMsNCMsNSMsNyMsOSMINDM4NjEuOTQDMjY4CTE5LDUwMC4zNgo1MTgsNDg3LjU1ZAIID2QWAmYPFQkENTg3OAkyMDE4MTIwMjUENTg3OAzplKbnhpnpm4Xoi5ECMSMHNTc1MC44MAI0MAkxNywwMDAuMDYKNTAzLDE5NS4wMGQCCQ9kFgJmDxUJBDU4NTgJMjAxODEyMDEzBDU4NTgM5rqq5bK46KeC6YK4EUQyLEQ1LEQ2LEQ3LEQ4LEQ5BzU0NDYuNjgCMjQJMTQsNzI5Ljc5BDAuMDBkAg0PDxYGHghQYWdlU2l6ZQIKHgtSZWNvcmRjb3VudAK7FR4QQ3VycmVudFBhZ2VJbmRleAIIZGRkhhkrK0KGYBLgZA4qunZZwdacoC4='


wb = Workbook()
sheet = wb.create_sheet()
filename = datetime.now().strftime("%Y-%m-%d")

sheet.append(['备案号','楼盘名称','楼号','建筑面积(㎡)','套数','均价(元/㎡)','装修总价(元)'])

def download_lp_info(offset):
    url = 'http://220.178.124.94:8010/fangjia/ws/DefaultList.aspx'

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
        tr_list_true = tr_list[2:tr_list_len-1]
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
    while offset < 275:
        offset = offset + 1

        download_lp_info(offset)

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=======================")
        print(offset)
        print("=======================")

        # time.sleep(n)


if __name__ == '__main__':
    timer(0.1)