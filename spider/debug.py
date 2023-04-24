# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/20 16:51
@Auth ： protossjames
@File ：debug.py
@IDE ：PyCharm
@notes：
"""
from prefect import task,flow
import requests
from fake_useragent import UserAgent
from urllib import parse
import re

def postData_make(begindate: str, enddate: str, page: int):

    #目前的postdata模式，以后可以做个自适应？
    postData={"query_params_url":"/zjfwcs/gd-zjcs-pub/bidResultNotice",
              "query_params_rest_url":"bidResultNotice/rest",
              "reloadQueryParamsReload":"false",
              "listVo.divisionCode":"441900",
              "listVo.bidResultDateBegin":begindate,
              "listVo.bidResultDateEnd":enddate,
              "pageNumber":page,
              "sourtType":""
              }
    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(postData)
    return data

def header_make():

    #随机User-Agent减少被检测风险
    ua = UserAgent().chrome
    #根据需要制作表头
    headers = {
        'User-Agent': ua,
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Key': '332213fa4a9d4288b5668ddd9'
    }
    #返回表头信息
    return headers

beginday="2023-04-19"
endday="2023-04-20"
requestURL="https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice/rest"
requestMethod="POST"
name="东莞中介超市"
page=0

headers=header_make()
data=postData_make(beginday,endday,page)

response=requests.post(url=requestURL, headers=headers, data=data)
html=response.text
print(html)