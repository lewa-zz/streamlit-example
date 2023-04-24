#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   tzxm.py
@Time    :   2023/04/17 17:01:30
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   None
'''

import beeprint
from collections import defaultdict
from utils.perfect_dict import *
import asyncio
from playwright.async_api import Playwright, async_playwright, expect
from prefect import task, flow, get_run_logger
import orjson
import pandas as pd
from datetime import timedelta, datetime
from playwright.async_api import Page, BrowserContext, ViewportSize, ProxySettings
from playwright.async_api import Playwright, Browser
from playwright.async_api import Response
from playwright.async_api import async_playwright

import os
import sys
fp = sys.path.append(os.pardir)
print(fp)

class PlaywrightRequest():
    # driver: Playwright = None
    # browser: Browser = None
    # context: BrowserContext = None
    # page: Page = None
    # url = None
    response:Response = None #返回的Response
    current_json_result:str = ""#本次返回的数据json字符
    _page_on_event_callback: dict = {}
    post_data = {
        "city": "4419",
        "flag": "1",
        "nameOrCode": "",
        "pageNumber": 1,
        "pageSize": 15,
    }
    def __init__(self, href=""):
        self._window_size = (1980, 1080)
        view_size = ViewportSize(
            width=self._window_size[0], height=self._window_size[1]
        )
        self.baseurl = "https://gd.tzxm.gov.cn"
        self.url = href if href != "" else r"%s/PublicityInformation/PublicityHandlingResults.html#" % self.baseurl
        self.apiurl ="%s/tzxmspweb/api/publicityInformation/selectByPageBA" %self.baseurl
        self.driver: Playwright = await async_playwright().launch()
        self.browser: Browser = await self.driver.chromium.launch(headless=False, args=["--start-maximized"])
        self.context: BrowserContext = await self.browser.new_context(screen=view_size, viewport=view_size)
        self.page: Page = await self.context.new_page()
        if self._page_on_event_callback:
            for event, callback in self._page_on_event_callback.items():
                await self.page.on(event, callback)
        await self.page.on("response", lambda response: self.on_response(response, self.url))
        await self.page.route(self.apiurl, self.handle_route)
        # self.page.goto(self.url,wait_until="networkidle")

    async def handle_route(self, route):
        # print("路由拦截%s ,其POSTDATA数据为了:%s" %
        #       (route.request.url, str(route.request.post_data)))
        #print("正在提取第%d页的数据"%self.post_data['pageNumber'])
        # 以下代码可以运行。
        if route.request.method == "POST": #and not postdata 
            route.continue_(post_data=str(self.post_data))
            print(str(self.post_data))


    async def on_response(self, response, url) -> None:
        '''
        page on response的监听器,返回结束集
        '''
        # 向接口提交的有api
        # r_headers =response.all_headers()
        # body= response.body()
        # beeprint.pp("response的头,其POSTDATA数据为了:%s" %r_headers)
        if "selectByPageBA" in response.request.url and response.status == 200:
            #print("**********"+response.url)
            #self.current_json_result = response.json() #这个不能用,浅copy,不能这样返回,执行完,要深copy
            self.current_json_result = response.text()
            print(self.current_json_result)

    def quit(self):
        self.page.close()
        self.context.close()
        self.browser.close()
        self.driver.stop()

    def __del__(self):
        self.quit()

    async def request_data(self,url:str="",post_data:dict ={}) ->str:
        '''
        请求页面,返回页面res及中间拦截的Json字典,放在类的current_json_result中
        '''
        if url !="":
            self.url = url
        #self.post_data = str(post_data)
        res = await self.page.goto(self.url, wait_until="networkidle")
        response = res
        if res.status != 200 :
            raise Exception('第%d拉取异常！'%page) 
        return self.current_json_result

    # def parse(self):
        '''
        返回的current_json_result字串,JSON解释和后处理.
        '''
        data = json.loads(self.current_json_result)
        res_dict = PerfectDict(data)

        #如果是第一次取回的数据,要知道总页数和每页条数,放于_totalPage和post_data中
        if self.post_data['pageNumber'] == 1: 
            self.post_data['pageSize'] = res_dict.data.pageSize
            self._totalPage = res_dict.data.totalPage

        self.to_jsonfile(self.current_json_result,self.post_data['pageNumber'])
        amo = self.append_cache_list(res_dict.data.list)
        print("暂存记录数量为:%d"%amo)
        return None

def postdata_make(city: str ="4419", flag: str="1",
                nameOrCode:str="", pageNumber:int=1,
                pageSize:int =15):
    post_data={
        "city": city,
        "flag": flag,
        "nameOrCode": nameOrCode,
        "pageNumber": pageNumber,
        "pageSize": pageSize,
    }
    # 字典转换k1=v1 & k2=v2 模式
    #data = parse.urlencode(postData)
    #return str(post_data)
    return post_data 
sp = PlaywrightRequest()
# @task(name="拉取任务第-{page}-页", retries=10, retry_delay_seconds=3,description="Get the Data by request")
def request_task(page:int=1):
    #sp = PlaywrightRequest()
    tt =  sp.request_data(post_data=postdata_make())
    return tt

# @flow(flow_run_name="{name}-on-{page}")
def start_flow(name: str, regionCode: str,page:int=1):
    # logger = get_run_logger()
    # logger.info('%s 第%d页启动'%(name,page))
    i:int = 1 
    b = True
    while b:
        tt= request_task(i)
        print(tt)
        # sp.parse()
        # i += 1
        # if i > sp._totalPage+1:
        #     b = False

if __name__ == "__main__":
    # from gevent import monkey
    # monkey.patch_all() #debug模式下会对线程的切换造成混乱,解决方案:
    start_flow("备案","441900",1)
