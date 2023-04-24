#!/usr/bin/python3
# -*- coding: utf-8 -*-
from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
from pandas import DataFrame
import re
import utils as utls
import ddddocr
import orjson
from prefect import task, flow, get_run_logger

data1 = { "msg": "操作成功","total": 1031,"code": "200","data": []}
base_url = "https://gdgpo.czt.gd.gov.cn/cms-gd/site/guangdong/xmcggg/index.html"

def on_response(res,url) -> None:
    global data1
    print("**********"+res.url)
    #print("@@@@@@@@@@"+res.request.url) 
    if "currPage" in res.url and res.status == 200:
        #print(res.json())
        
        data2 = res.json() #json.loads(res.json())
        #print("data2 type is :"+str(type(data2)))
        # 合并数据
        data1["data"].extend(data2["data"])
        #们用到了json库的dumps方法，将Python对象转化为Json对象
        #json_data = json.dumps(data1, indent=2, separators=(",", " = "))
        json_data = orjson.dumps(data1, option=orjson.OPT_INDENT_2).decode()
        df = pd.json_normalize(data1, 'data',['msg','code'])
        df.to_excel("output.xlsx",encoding='utf-8')
    if res.status != 200:
        print("失败的url:%s"%url)

def run(playwright: Playwright) -> None:
    data = {'序号':[],'href':[],'项目':[],'项目1':[],'局办':[],'类目':[],'采购编号':[],'金额':[],'时间':[]}  #data= dict()
    base_url:str = r"https://gdgpo.czt.gd.gov.cn/"

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # page.on("request", res)
    page.on("response", lambda response: on_response(response, base_url))
    #如果出错,打印出错原因
    page.on("requestfailed", lambda request: print(request.url + " 出错了" + request.failure))
    page.goto("https://gdgpo.czt.gd.gov.cn/cms-gd/site/guangdong/xmcggg/index.html")
    page.wait_for_timeout(1000)
    #page.wait_for_selector("text=请选择区域")
    #time.sleep(8) 不用这个方法等
    page.get_by_placeholder("请选择区域").click()
    page.get_by_placeholder("请选择区域").fill("石龙镇")
    page.get_by_title("石龙镇",exact=True).click()
    page.locator("#noticeTypeList").get_by_text("中标（成交）结果公告").dblclick()
    page.get_by_placeholder("请选择开始时间").click()
    page.get_by_placeholder("请选择开始时间").fill("2022-01-01 00:00:00")
    page.get_by_placeholder("请选择结束时间").click()
    page.get_by_placeholder("请选择结束时间").fill("2022-12-31 23:59:59")

    #page.locator("#code_img").screenshot(path=f"screenshot.png")
    #载图id为code_img的图片，放入内存中，待识别用
    code_img = page.locator("#code_img").screenshot()
    ocr =  ddddocr.DdddOcr(old=True)
    code_text =  ocr.classification(code_img)
    #识别出验证码,并填入
    page.get_by_placeholder("请输入验证码").click()
    page.get_by_placeholder("请输入验证码").fill(code_text)
    page.get_by_role("button", name="查询").click()
    page.wait_for_timeout(2000)
    #==================================================================
    #查询出来后，读取表格的内容

    #查找ID=pagination下面的LI标签，合多少条记录
    rec_total = page.locator('#pagination').locator('li:has-text("合计")').text_content()
    rec_total = int(re.findall(r'\d+',rec_total)[0])
    page_amo =page.locator('#pagination').locator('li:has-text("共")').text_content()
    kk = re.compile(r'\d+(\.\d+)?')
    page_amo = int(re.findall(r'\d+',page_amo)[0])
    print("记录数%d,页数%d"%(rec_total,page_amo))

    for row in range(1,page_amo):
        page.locator('#pagination').locator('li:text(">")').click()
        page.wait_for_timeout(2000)
        print("---------%d-页--------------"%row )
        # if row == 2:
        #     break   
    page.close()

    # ---------------------
    context.close()
    browser.close()

if __name__ == "__main__":
     with sync_playwright() as playwright:
        run(playwright)