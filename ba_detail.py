#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   ba_detail.py
@Time    :   2023/04/23 11:24:17
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   备案第二页,详情页
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
from models.tab_beian import *

import os
import sys

fp = sys.path.append(os.pardir)

base_url = "https://gd.tzxm.gov.cn"
post_data = {"baId": "1649223131300102146"}
url = (
    "%s/PublicityInformation/resultDetail2.html?id=%s&audit=ba&flag=gk&textShowFlag=true"
    % (base_url, post_data["baId"])
)
apiurl = "%s/tzxmspweb/api/publicityInformation/selectBaProjectInfo" % base_url

# 创建playwright对象
driver = sync_playwright().start()
browser = driver.chromium.launch(headless=False, devtools=False)
context: BrowserContext = browser.new_context(base_url=base_url)

current_json_result: str = ""  # 本次返回的数据json字符
cache_json = []


def handle_route(route):
    # print("路由拦截%s ,其POSTDATA数据为了:%s" %
    #       (route.request.url, str(route.request.post_data)))
    print("正在提取id:%s的数据" % post_data["baId"])
    # 以下代码可以运行。
    if route.request.method == "POST":
        route.continue_(post_data=post_data)


def on_response(response, url) -> None:
    """
    page on response的监听器,返回结束集
    """
    global current_json_result
    if apiurl in response.request.url and response.status == 200:
        # print("**********"+response.url)
        # current_json_result = response.json() #这个不能用,浅copy,不能这样返回,执行完,要深copy
        current_json_result = response.text()


def quit(self):
    # page.close()
    context.close()
    browser.close()
    driver.stop()


# @task(
#     name="拉取任务Get-data-Task--{baId}",
#     retries=10,
#     retry_delay_seconds=3,
#     description="Get the Data by request",
# )
def get_data(context: BrowserContext, baId: str) -> str:
    """
    请求页面,返回页面res及中间拦截的Json字典,放在类的current_json_result中
    """
    global post_data
    post_data["baId"] = baId
    need_request = True
    while need_request:
        page: Page = context.new_page()
        page.on("response", lambda response: on_response(response, url))
        page.route(apiurl, handle_route)

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


@task(name="写入json文件}")
def to_jsonfile(json_text: str, pagenu: int = 1):
    with open(
        r"./html/备案详情第%s条_%s.json"
        % (pagenu, datetime.now().strftime("%Y-%m-%d, %H:%M:%S")),
        "w",
    ) as f:
        f.write(json_text)


@task(name="写入数据库")
def to_tab_db(j_str: str):
    insert_from_dict(j_str)


@flow(flow_run_name="{name}")
def start_flow(name: str):
    global context
    logger = get_run_logger()
    i: int = 1
    for item in BeiAn.select().where(BeiAn.isGet == 0):
        logger.info("第%d条记录启动--%s" % (i, item.baId))
        rst = get_data(context, item.baId)
        beeprint.pp(rst)
        to_jsonfile(rst, i)
        to_tab_db(rst)
        item.isGet = 1
        item.save()


if __name__ == "__main__":
    start_flow("备案详情")
