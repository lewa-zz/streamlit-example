#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   财政网request.py
@Time    :   2023/04/11 22:07:13
@Author  :   Rico Chen 
@Version :   1.0
@Site    :   https://www.dgpms.cn/
@Desc    :   None
'''
import os
import requests
from urllib import parse
import utils
from prefect import task, flow, get_run_logger
import orjson
import pprint
import pandas as pd
import beeprint
from datetime import timedelta, datetime

#base_url = "https://gdgpo.czt.gd.gov.cn/cms-gd/site/guangdong/xmcggg/index.html"
#rest_url:str = r"https://gdgpo.czt.gd.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=cd64e06a-21a7-4620-aebc-0576bab7e07a&channel=fca71be5-fc0c-45db-96af-f513e9abda9d&currPage=3&pageSize=10&noticeType=&regionCode=441900002&verifyCode=0908&subChannel=false&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime&cityOrArea="

@task(name="拉取任务Task-{regionCode}-{page}", 
      retries=10, retry_delay_seconds=3,description="Get the Data by request")
def get_data(regionCode: str,page:int=1):
    '''
    拉取任务,返回多少页,和当前页
    '''
    # 定义请求header
    HEADERS = {'Content-Type': 'application/json;charset=utf-8', 'Key': '332213fa4a9d4288b5668ddd9'}
    # 定义请求地址
    url = "https://gdgpo.czt.gd.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do"
    # 通过字典方式定义请求body
    FormData = {"siteId": "cd64e06a-21a7-4620-aebc-0576bab7e07a", 
                "channel": 'fca71be5-fc0c-45db-96af-f513e9abda9d',
                "currPage": page,
                "pageSize": "10",
                "noticeType":"00102",
                "regionCode":regionCode,
                "operationStartTime":'2022-01-01 00:00:00',
                "operationEndTime":'2022-12-31 00:00:00',
                "verifyCode":utils.imgtostr(),
                "selectTimeName":"noticeTime"}
    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(FormData)
    #print(data)
    # 请求方式
    r = requests.get(url=url, headers=HEADERS, params=data)
    #print(r.url)
    #print("返回码:%s"%r.status_code)
    if r.status_code != 200:
        raise Exception('第%d拉取异常！'%page)
    
    content = r.json()
    rec_amo = content["total"]
    print("记录数%s"%rec_amo)
    json_data = orjson.dumps(content, option=orjson.OPT_INDENT_2).decode()

    with open(r'./html/%s-%d.json'%(regionCode,page), 'w') as f:
        f.write(json_data)
    return rec_amo

@flow(flow_run_name="{name}-on-{page}")
def my_flow(name: str, regionCode: str,page:int=1):
    logger = get_run_logger()
    logger.info('%s 第%d页启动'%(name,page))
    i = 1 
    b = True
    while b:
        rec_amo = get_data(regionCode,i)
        i += 1
        if i > int(rec_amo/10)+1:
            b = False
    
@flow(flow_run_name="{name}-on-{page})")

def dg():
    '''
    根据JSON文件,返回东莞各镇及其编码的数组
    可以通过下面防问:
    for j in a:
        print("%s %s"%(j['name'],j["regionCode"]))
    print("总数:%d"%len(a))
    '''
    f = open(r"./财政网的json/gdTree.json","rb")
    json_data = orjson.loads(f.read())

    a = []
    for i in json_data:
      if i['id'] == "2278":
        a = i['children']
        break
    return a

if __name__ == "__main__":
    for i in dg():
        print("%s %s"%(i['name'],i["regionCode"]))
        my_flow(i['name'],i["regionCode"],1)  


