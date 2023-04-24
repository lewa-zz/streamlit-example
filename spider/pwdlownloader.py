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
from utils.tools import *
from playwright.sync_api import Playwright, sync_playwright, expect
from prefect import task, flow, get_run_logger
import orjson
import pandas as pd
from datetime import timedelta, datetime
from playwright.sync_api import Page, BrowserContext, ViewportSize, ProxySettings
from playwright.sync_api import Playwright, Browser
from playwright.sync_api import Response
from playwright.sync_api import sync_playwright
from utils.common import json_data_merge
import os
import sys
fp = sys.path.append(os.pardir)
print(fp)

from dataclasses import dataclass

post_data = {
    "city": "4419",
    "flag": "1",
    "nameOrCode": "",
    "pageNumber": 1,
    "pageSize": 15,
}

@dataclass
class PlaywrightDownloader():
    driver: Playwright = None
    browser: Browser = None
    context: BrowserContext = None
    page: Page = None
    url = None
    _page_on_event_callback=[]

    '''
    spider base class
    '''
    def __init__(self, href=""):
        self._window_size = (1980, 1080)
        view_size = ViewportSize(
            width=self._window_size[0], height=self._window_size[1]
        )
        self.baseurl = "https://gd.tzxm.gov.cn"
        self.url = href if href != "" else r"%s/PublicityInformation/PublicityHandlingResults.html#" % self.baseurl
        self.driver: Playwright = sync_playwright().start()
        self.browser: Browser = self.driver.chromium.launch(
            headless=True, args=["--start-maximized"])
        self.context: BrowserContext = self.browser.new_context(
            screen=view_size, viewport=view_size)
        self.page: Page = self.context.new_page()
        if self._page_on_event_callback:
            for event, callback in self._page_on_event_callback.items():
                self.page.on(event, callback)
        self.page.on("response", lambda response: self.on_response(response, self.url))
        self.page.route("%s/tzxmspweb/api/publicityInformation/selectByPageBA" %self.baseurl, self.handle_route)
        # self.page.goto(self.url,wait_until="networkidle")

    def to_jsonfile(self, json_text: str,page:int =1):
        with open(r'./html/备案第%s页_%s.json' %(page,datetime.now().strftime("%Y-%m-%d, %H:%M:%S")), 'w') as f:
            f.write(json_text)

    def append_cache_list(self, data_list:list) -> int:
        '''
        json中的数据列表加入到暂存列表中
        '''
        if len(self._cache_list) == 0:
            self._cache_list =data_list
        else:
            self._cache_list.extend(data_list)
        return len(self._cache_list)

    def handle_route(self, route):
        # print("路由拦截%s ,其POSTDATA数据为了:%s" %
        #       (route.request.url, str(route.request.post_data)))
        print("正在提取第%d页的数据"%self.post_data['pageNumber'])
        # 以下代码可以运行。
        if route.request.method == "POST":
            route.continue_(post_data=self.post_data)

    def get_totalpage_pagesize(self,res_dict:PerfectDict):
        if self.post_data['pageNumber'] == 1:
            self._totalPage = res_dict.data.totalPage
            self.post_data["pageSize"] = res_dict.data.pageSize
            self._cache_list = res_dict.data.list        

    def on_response(self, response, url) -> None:
        '''
        page on response的监听器,返回结束集
        '''
        # 向接口提交的有api
        # r_headers =response.all_headers()
        # body= response.body()
        # beeprint.pp("response的头,其POSTDATA数据为了:%s" %r_headers)
        if "selectByPageBA" in response.request.url and response.status == 200:
            # print("**********"+response.url)
            #self.current_json_result = response.json() #这个不能用,浅copy,不能这样返回,执行完,要深copy
            self.current_json_result = response.text()

    def quit(self):
        self.page.close()
        self.context.close()
        self.browser.close()
        self.driver.stop()

    def __del__(self):
        self.quit()
    
    #@task(name="拉取任务第-{page}-页", retries=10, retry_delay_seconds=3,description="Get the Data by request")
    def get_data(self,page:int = 1,postdata={}) ->str:
        '''
        请求页面,返回页面res及中间拦截的Json字典,放在类的current_json_result中
        '''
        self.post_data["pageNumber"] = page
        res = self.page.goto(self.url, wait_until="networkidle")
        if res.status != 200 :
            raise Exception('第%d拉取异常！'%page) 
        return self.current_json_result
    
    def parse(self):
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


@flow(flow_run_name="{name}-on-{page}")
def start_flow(self, name: str, regionCode: str,page:int=1):
    logger = get_run_logger()
    logger.info('%s 第%d页启动'%(name,page))
    i:int = 1 
    b = True
    while b:
        tt= self.get_data(i)
        self.parse()
        i += 1
        if i > self._totalPage+1:
            b = False

if __name__ == "__main__":
    sp = TzxmSpider()
    sp.start_flow("备案","441900",1)
