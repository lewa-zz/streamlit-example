#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   投资项目审核平台.py
@Time    :   2023/04/17
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   None
@GetFrom :   https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html
@APIrest :   https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectByPageBA
'''
import os
import requests
from urllib import parse
import json
import pandas as pd
from datetime import timedelta, datetime
# import httpx

# @task(name="拉取任务Task-{regionCode}-{page}", 
#       retries=10, retry_delay_seconds=3,description="Get the Data by request")
def get_data(regionCode: str,page:int=1):
    '''
    拉取任务,返回多少页,和当前页
    '''

    post_data={
      "flag": "1",
      "nameOrCode": "",
      "pageSize": 15,
      "city": regionCode,
      "pageNumber": page
    }
    # 定义请求header
    headers = {'Content-Type': 'application/json;charset=utf-8',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
               'Cookie':'JSESSIONID=A94C38004848A513C6A9363785BD6320; __jsluid_s=b8e1e4dedc982cbb7edb29a3b2772aa4'}

    # 定义请求地址
    url = "https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectByPageBA"
    data=json.dumps(post_data)
 
# 请求方式
    #r = requests.post(url=url, headers=headers, json=post_data) 
    r = requests.post(url=url, headers=headers, data=data) 

    #print(r.url)
    #print("返回码:%s"%r.status_code)
    if r.status_code != 200:
        raise Exception('第%d拉取异常！'%page)
    txt = r.json()

if __name__ == '__main__': 
  get_data("4419")


