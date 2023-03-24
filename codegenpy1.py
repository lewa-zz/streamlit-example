#!/usr/bin/python3
# -*- coding: utf-8 -*-

from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
import re
import sqlite3
from datetime import datetime 

data = {'序号':[],'href':[],'项目':[],'项目业主':[],'服务类型':[],'中选机构':[],'金额':[],'服务内容':[],'时间':[]}  #data= dict()
base_url:str = r"https://ygp.gdzwfw.gov.cn"

def write_excel(data):
    '''
    写一个全新的文件也很简单：
    data = {'name': ['zs', 'ls', 'ww'], 'age': [
        11, 12, 13], 'gender': ['man', 'man', 'woman']}
    '''
    df = pd.DataFrame(data)
    df.to_excel('网上中介.xlsx')

def res(res) -> None:
    print("**********"+res.url)
    # if "id" in res.url:
    #     print("**********"+res.url)


def popup(context,href):
    new_page = context.new_page()
    new_page.goto(href)
    new_page.wait_for_timeout(2000)  

    #pop up a new_page to locate the amo
    _do = True
    while _do:
        with context.expect_page() as new_page2_info:
            new_page.locator('li:has-text("采购项目名称")').locator("a").click() # Opens a new tab
        new_page2 = new_page2_info.value
        new_page2.wait_for_load_state()
        new_page2.wait_for_timeout(4000) 
        print(new_page2.url)
        _do = False
        if  (new_page2.url == r"https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/home") or (new_page2.title() == "Error"):
                _do = True
                new_page2.close()

    amo = new_page2.locator('div > ul > li:has-text("项目规模")').locator("div")
    #amo = new_page2.get_by_role("li").filter(has_text="项目规模")
    _kk = re.compile(r'\d+\.?\d+') #正则中小数点加\转义,不然.就识别任一字符
    kk = re.findall(_kk,amo.text_content().replace(",",""))
    amo = float(kk[0]) if len(kk) != 0 else 0
    #data["金额"].append(amo)
    content = new_page2.locator('li:has-text("服务内容")').locator("div").text_content()
    #data["服务内容"].append(content)

    new_page2.close()
    new_page.close()
    return locals()

# Handle POST requests.
def handle_post(route,request):
     # override headers
    # headers = {
    #     **request.headers,
    #     "foo": "foo-value" # set "foo" header
    #     "bar": None # remove "bar" header
    # }
    post_data=f'query_params_url=%2Fzjfwcs%2Fgd-zjcs-pub%2FbidResultNotice&query_params_rest_url=bidResultNotice%2Frest&reloadQueryParamsReload=false&listVo.projectName=&listVo.purOrgName=&listVo.divisionCode=441900&listVo.selectModeType=&listVo.bidResultDateBegin=2022-01-01&listVo.bidResultDateEnd=2022-01-31&pageNumber=6&sourtType=&'
 
    
    #第一次提交 'query_params_url=%2Fzjfwcs%2Fgd-zjcs-pub%2FbidResultNotice&query_params_rest_url=bidResultNotice%2Frest&reloadQueryParamsReload=false&listVo.projectName=&listVo.purOrgName=&listVo.divisionCode=441900&listVo.selectModeType=&listVo.bidResultDateBegin=2022-01-01&listVo.bidResultDateEnd=2022-01-31&listVo.selectServiceTypes=005&listVo.selectServiceTypes=020'
   
     # {
    #     #query_params_url=%2Fzjfwcs%2Fgd-zjcs-pub%2FbidResultNotice
    #     #query_params_rest_url=bidResultNotice%2Frest&reloadQueryParamsReload=false&
    #     #listVo.projectName=&listVo.purOrgName=&
    #     #listVo.divisionCode=441900,
    #     #listVo.selectModeType=&listVo.bidResultDateBegin=2022-01-01&listVo.bidResultDateEnd=2022-01-31&listVo.selectServiceTypes=005&listVo.selectServiceTypes=010
    # }
    if route.request.method == "POST":
        route.continue_(post_data=post_data)

    

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice")
    page.wait_for_timeout(3000)
    #print(page.request.all_headers())
    #如果出错,打印出错原因
    page.on("requestfailed", lambda request: print("出错了"+request.url + " " + request.failure))
    page.on("request", lambda request: print("提交URL:"+request.url))
    page.on("response", res)
    #拦住路由
    page.route("*https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice/rest", handle_post)
    #page.locator("//html/body/div[6]/div[2]/div/span").click() #展开选择面板
    #page.locator("div").filter(has_text="展开").first.click()
    page.locator("span").filter(has_text="展开").click()
    #选择东莞市
    # page.locator("#divisionCodePlugs").get_by_placeholder("请选择").click()
    # page.get_by_role("listitem", name="东莞市").click()
    # page.get_by_role("button", name="确定").click()

    #填入查询日期
    page.get_by_placeholder("选取时间").click()
    page.get_by_placeholder("选取时间").press("Enter") #要加个回车才能fill入数据
    page.get_by_placeholder("选取时间").fill("2022-01-01")
    page.get_by_placeholder("选取时间").press("Tab")
    # page.locator("#publishDateEnd").click()
    # page.locator("#publishDateEnd").fill("2022-01-31")
    page.get_by_placeholder("至").click()
    page.get_by_placeholder("至").press("Enter") 
    page.get_by_placeholder("至").fill("2022-01-31")
    page.get_by_placeholder("至").press("Tab")

    #选择服务项目
    page.get_by_text("展开").click()
    #page.locator("label").filter(has_text="工程监理").locator("span").nth(1).click()
    #page.locator("label").filter(has_text="信息系统工程监理").locator("span").nth(1).click()
    page.locator("#serviceType").get_by_text("收起").click()
    #rel  = page.locator("#reloadQueryParamsReload").input_value()
    pd="listVo.divisionCode=441900"
    # with page.expect_request(lambda request: request.url == "https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice/rest" and request.method == "POST") as second:
    #     page.click("#searchButton")
    # second_request = second.value
    # print(second_request.url+"::::::::::::")

    page.click("#searchButton")
    page.wait_for_timeout(4000)
   
    rec_total = page.locator("#totalElementsView").text_content()
    rec_total = re.findall(r'\d+',rec_total) 
    rec_total = 0 if not rec_total else int(rec_total[0]) #列表空为FALSE,取0,不空,提出数字
        
    #根据查询到的结果进行资料收集
    i = 0
     #循环取出记录,打开新页面.
    while i < rec_total:
        #定位表格的行,然后遍历
        tr = page.locator('//*[@id="resultPannel"]/table/tbody/tr') #[1]/td[1]'.locator("a")
        #print(li.text_content())
        #j+=1
        for row in tr.all():
            data['序号'].append(i)
            #定位每行下面的列TD
            td = row.locator("td").all()
            # tdo = expect(row.locator("td")).to_have_count(5)期待有5列
            alink = td[0].get_by_role("link") #或ahref = row.locator("a")
            ahref = base_url+str(alink.get_attribute("href"))
            data["href"].append(ahref)
            data["项目"].append(alink.text_content())
            data["项目业主"].append(td[1].inner_text())
            data["服务类型"].append(td[2].inner_text())
            data["中选机构"].append(td[3].inner_text())
            data["时间"].append(td[4].inner_text())
            #print("url is %s ,content is :%s"%(td[0].get_attribute("href"),td[0].text_content))
            i += 1
            # di:dict = popup(context,ahref)
            # data["金额"].append(di["amo"])
            # data["服务内容"].append(di["content"])
        
        if i < rec_total: 
            #write_excel(data) #做一页写一页
            page.get_by_text(">",exact=True).click
            page.wait_for_load_state()
            page.wait_for_timeout(2000)


    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
