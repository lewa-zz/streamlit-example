#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   tzxm.py
@Time    :   2023/04/17 17:01:30
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   None
"""
import beeprint
from collections import defaultdict
from utils.perfect_dict import *
from prefect import task, flow, get_run_logger
import orjson
import pandas as pd
from datetime import timedelta, datetime
from playwright.sync_api import Page, BrowserContext, ViewportSize, ProxySettings
from playwright.sync_api import Playwright, Browser
from playwright.sync_api import Response
from playwright.sync_api import sync_playwright
from models.items import *


import os
import sys

fp = sys.path.append(os.pardir)

baseurl = "https://gd.tzxm.gov.cn"
url = r"%s/PublicityInformation/PublicityHandlingResults.html#" % baseurl
apiurl = r"%s/tzxmspweb/api/publicityInformation/selectByPageBA" % baseurl

# 创建playwright对象
driver = sync_playwright().start()
browser = driver.chromium.launch(headless=False, devtools=False)
context: BrowserContext = browser.new_context(base_url=baseurl)

current_json_result: str = ""  # 本次返回的数据json字符
cache_list: list = []  # 数据暂存列表


post_data = {
    "city": "4419",
    "flag": "1",
    "nameOrCode": "",
    "pageNumber": 1,
    "pageSize": 15,
}


def append_cache_list(data_list: list) -> int:
    """
    json中的数据列表加入到暂存列表中
    """
    global cache_list
    if len(cache_list) == 0:
        cache_list = data_list
    else:
        cache_list.extend(data_list)
    return len(cache_list)


def handle_route(route):
    # print("路由拦截%s ,其POSTDATA数据为了:%s" %
    #       (route.request.url, str(route.request.post_data)))
    print("正在提取第%d页的数据" % post_data["pageNumber"])
    # 以下代码可以运行。
    if route.request.method == "POST":
        route.continue_(post_data=post_data)


def on_response(response, url) -> None:
    """
    page on response的监听器,返回结束集
    """
    global current_json_result
    # 向接口提交的有api
    # r_headers =response.all_headers()
    # body= response.body()
    # beeprint.pp("response的头,其POSTDATA数据为了:%s" %r_headers)
    if apiurl in response.request.url and response.status == 200:
        # print("**********"+response.url)
        # current_json_result = response.json() #这个不能用,浅copy,不能这样返回,执行完,要深copy
        current_json_result = response.text()


def quit(self):
    # page.close()
    context.close()
    browser.close()
    driver.stop()


def postdata_make(
    city: str = "4419",
    flag: str = "1",
    nameOrCode: str = "",
    pageNumber: int = 1,
    pageSize: int = 15,
):
    # 目前的postdata模式，以后可以做个自适应？
    post_data = {
        "city": city,
        "flag": flag,
        "nameOrCode": nameOrCode,
        "pageNumber": pageNumber,
        "pageSize": pageSize,
    }
    # 字典转换k1=v1 & k2=v2 模式
    # data = parse.urlencode(postData)
    return post_data


# @task(
#     name="拉取任务Get-data-Task--{pagenu}",
#     retries=10,
#     retry_delay_seconds=3,
#     description="Get the Data by request",
# )
def get_data(context: BrowserContext, pagenu: int = 1) -> str:
    """
    请求页面,返回页面res及中间拦截的Json字典,放在类的current_json_result中
    """
    global post_data
    need_request = True
    while need_request:
        page: Page = context.new_page()
        page.on("response", lambda response: on_response(response, url))
        page.route(apiurl, handle_route)
        post_data["pageNumber"] = pagenu

        try:
            res = page.goto(url, wait_until="networkidle")
            if res.status == 200:
                need_request = False
            if res.status != 200:
                page.close()
                # raise Exception("第%d拉取异常！" % pagenu)
        except Exception as e:
            page.close()
            # raise Exception("第%d拉取异常！" % pagenu)
        page.close()
    return current_json_result


@flow(name="处理分析第-{pagenu}-页任务结果")
def parse(current_str_result: str, pagenu: int = 1):
    """
    返回的current_json_result字串,JSON解释和后处理.
    """
    if current_str_result == "":
        return 0, 0
    data = json.loads(current_str_result)
    print(type(data["data"]["list"]))
    res_dict = PerfectDict(data)

    total_page = res_dict.data.totalPage
    rec_total = res_dict.data.totalRow
    amo = append_cache_list(res_dict.data.list)
    print("暂存记录数量为:%d,总页数:%d,记录数%d" % (amo, total_page, rec_total))

    to_jsonfile(current_str_result, pagenu)
    # to_db(res_dict.data.list, pagenu)
    return amo, total_page


@task(name="写入json文件-{pagenu}")
def to_jsonfile(json_text: str, pagenu: int = 1):
    with open(
        r"./html/备案第%s页_%s.json"
        % (pagenu, datetime.now().strftime("%Y-%m-%d, %H:%M:%S")),
        "w",
    ) as f:
        f.write(json_text)


@task(name="第-{pagenu}-页写入数据库")
def to_db(data_list: list, pagenu: int = 1):
    insert__from_list(data_list)


@flow(flow_run_name="{name}-第-{pagenu}")
def start_flow(name: str, regionCode: str, pagenu: int = 1):
    global context
    logger = get_run_logger()
    logger.info("%s 第%d页启动" % (name, pagenu))
    i: int = 640
    b = True
    while b:
        rst = get_data(context, i)
        amo, total_page = parse(rst, i)
        i += 1
        if i > total_page + 1:
            b = False


if __name__ == "__main__":
    start_flow("备案", "441900", 1)
