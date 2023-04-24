#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ==========================================
#       Author: RicoChen
#        📧Mail: 55059@qq.com
#         ⌚Time: 2023/4/4
#           Version:
#             Description: 从网上中介超市拿数据
# ==========================================
from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
import re,time
import sqlite3
from datetime import datetime 
from prefect import task, flow, get_run_logger

data = {'序号':[],'href':[],'项目名称':[],'项目业主':[],'服务类型':[],'中选机构':[], #第一页选取
    '采购项目编码':[],'金额说明':[],'服务金额':[], 'to_page3':[],         #第二页选取
    '项目规模':[],'服务内容':[],'拟服务金额':[],'时间':[]}  #data= dict()        #第三页选取，时间是第一页的
base_url:str = r"https://ygp.gdzwfw.gov.cn"


@task(name="拉取任务Task-{page}", 
      retries=30, retry_delay_seconds=30,description="Get the Data by request")
def get_data(page: int):
    import requests
    import json
    from urllib import parse

    # 定义请求header
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'Key': '332213fa4a9d4288b5668ddd9'}
    # 定义请求地址
    url = "https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice/rest"
    # 通过字典方式定义请求body
    FormData = {"listVo.divisionCode": '441900', 
                "listVo.bidResultDateBegin": '2022-01-01', 
                "listVo.bidResultDateEnd":"2022-5-20",
                "pageNumber": page,
                "sourtType":""}
    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(FormData)
    # 请求方式
    content = requests.post(url=url, headers=HEADERS, data=data)
    print("返回码:%s"%content.status_code)
    if content.status_code != 200:
        raise Exception('第%d拉取异常！'%page)
    #content = json.loads(content)
    content = content.text
    #print(content)
    with open(r'./html/adata%d.html'%page, 'w') as f:
        f.write(content)
    return content

@flow(flow_run_name="{name}-on-{page}")
def my_flow(name: str, page: int ):
    logger = get_run_logger()
    logger.info('%s 第%d页启动'%(name,page))
    get_data(page)

@task(name="页面加载", 
      retries=30, retry_delay_seconds=30,description="Get the Data by request")
def load_page(page, href: str):
    #href = 'https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice/view/4419001257480170562212270347'
    r = page.goto(href)
    if r.status != 200:
        raise Exception("页面加载失败，重试中！")
    return page

@flow(flow_run_name="从EXCEL读出拉页面")
def read_excel(file_path):
    '''
    pandas读excel
    read_excel的原型：read_excel(io, sheet_name=0, header=0, names=None, index_col=None, usecols=None)
    '''
    #file_path = r'./总输出.xlsx'
    # sheet_name不指定时默认返回全表数据
    df = pd.read_excel(file_path, sheet_name="Sheet1", header=0)
    # 打印列标题,即表头
    print(df.columns)
    total_rows = len(df)
    print('总数:{0} 行数{1}', format(df.index.size), str(total_rows))
    data2 = df.to_dict(orient='list')
    j = 0
    for row_index, row in df.iterrows():
        di:dict = popup_page3(row['to_page3'], row_index)
        # row['序号'] =  row_index
        # row["项目规模"] = di["amo"]
        # row["服务内容"] = di["content"]+'wwwwwww'
        # row['拟服务金额'] = di['servie_amo']
        data2['序号'][row_index] =  row_index
        data2["项目规模"][row_index] = di["amo"]
        data2["服务内容"][row_index] = di["content"]
        data2['拟服务金额'][row_index] = di['servie_amo']
        j += 1
        if j == 20: #每20条存一次盘吧
            df = pd.DataFrame(data2)
            df.to_excel('输出.xlsx')
            j=0
            #break
    df = pd.DataFrame(data2)
    df.to_excel('输出.xlsx')  

@task(name="{num}任务加载", 
      retries=10, retry_delay_seconds=1,description="Get the Data by request")
def popup_page3(href: str,num):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)    
        context = browser.new_context()
        new_page = context.new_page()
        _do = True
        while _do:
            _do = False
            #load_page(new_page,href)
            r = new_page.goto(href)
            if r.status != 200:
                new_page.close()
                time.sleep(1)
                new_page = context.new_page()
                _do =True
        try:
            amo = new_page.locator('div > ul > li:has-text("项目规模")').locator("div").text_content()
        #amo = new_page2.get_by_role("li").filter(has_text="项目规模")
            _kk = re.compile(r'\d+\.?\d+') #正则中小数点加\转义,不然.就识别任一字符
            kk = re.findall(_kk,amo.replace(",",""))
            amo = float(kk[0]) if len(kk) != 0 else 0
        except:
            amo = 0
        #data["金额"].append(amo)
        #scale = new_page.locator('div > ul > li:has-text("项目规模")').locator("div").text_content()
        try:
            content = new_page.locator('li:has-text("服务内容")').locator("div").text_content()
        except:
            content=""

        try:
            servie_amo =new_page.locator('div > ul > li:has-text("服务金额")').locator("div").text_content()
        except:
            servie_amo = 0
        #servie_amo = new_page.locator('li:has-text("服务金额")').locator("div").text_content()
        #data["服务内容"].append(content)
        new_page.close()
    # time.sleep(2)
    return locals()

#中选公告页面数
#@task(name="打开第二页Task",retries=3, retry_delay_seconds=10,description="Get the Data by request")
def popup_page2(context,href):
    new_page = context.new_page()
    _do = True
    while _do:
        _do = False
        #load_page(new_page,href)
        r = new_page.goto(href)
        if r.status != 200:
            new_page.close()
            time.sleep(3)
            new_page = context.new_page()
            _do =True

    to_page3 = new_page.locator('li:has-text("采购项目名称")').locator("a").get_attribute("href") # Opens a new tab
    purchase_nu = new_page.locator('div > ul > li:has-text("采购项目编码")').locator("div").text_content()
    amo_memo =  new_page.locator('div > ul > li:has-text("金额说明")').locator("div").text_content()
    try:
        servie_amo =new_page.locator('div > ul > li:has-text("服务金额")').locator("div").text_content()
    except:
        servie_amo = 0
    #selected_amo = new_page.locator('div > ul > li:has-text("中选金额")').locator("div").text_content()
    new_page.close()
    # time.sleep(2)
    return locals()

def run(playwright: Playwright,htmlfile: str) -> None:
    global data
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    #browser,context,page = open_browser()
    page.goto(htmlfile)
    #page.wait_for_timeout(1000)
    #定位表格的行,然后遍历
    tr = page.locator('//*[@id="resultPannel"]/table/tbody/tr') #[1]/td[1]'.locator("a")
    #print(li.text_content())  
    i = 0 
    for row in tr.all():
        data['序号'].append(i)
        #定位每行下面的列TD
        td = row.locator("td").all()
        # tdo = expect(row.locator("td")).to_have_count(5)期待有5列
        alink = td[0].get_by_role("link") #或ahref = row.locator("a")
        ahref = base_url+str(alink.get_attribute("href"))
        data["href"].append(ahref)
        data["项目名称"].append(alink.text_content())
        data["项目业主"].append(td[1].inner_text())
        data["服务类型"].append(td[2].inner_text())
        data["中选机构"].append(td[3].inner_text())
        data["时间"].append(td[4].inner_text())
        #print("url is %s ,content is :%s"%(td[0].get_attribute("href"),td[0].text_content))
        i += 1
        #处理第二页
        di:dict = popup_page2(browser.new_context(),ahref)
        data["采购项目编码"].append(di["purchase_nu"])
        data["金额说明"].append(di["amo_memo"])
        data["服务金额"].append(di["servie_amo"])
        #data["中选金额"].append(di["selected_amo"]cle
        ahref = base_url+str(di['to_page3'])
        data["to_page3"].append(ahref)
        #处理第三页
        data["项目规模"].append("")
        data["服务内容"].append("")
        data['拟服务金额'].append(0) 

        # di:dict = popup_page3(browser.new_context(),ahref)
        # data["项目规模"].append(di["amo"])
        # data["服务内容"].append(di["content"])
        # data['拟服务金额'].append(di['servie_amo'])   
        df = pd.DataFrame(data)
        df.to_excel('输出.xlsx')  
    print("=====================================================") 
    browser.close()
    # time.sleep(2)

def open_page3(url:str):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)    
        page = browser.new_page()
        page.goto(url)


@flow(flow_run_name="取数据-on-{pagenu}")
def parse_html_flow(pagenu: int):
    logger = get_run_logger()
    logger.info('第%d页启动'%(pagenu))
    htmlfile = r"file:///Users/ricochen/program/streamlit-example/html/adata%d.html"%pagenu
    with sync_playwright() as playwright:
        run(playwright,htmlfile)

if __name__ == "__main__":
    #creates a flow run called 'marvin-on-Thursday'
    file_path = r'./总输出.xlsx'
    read_excel(file_path)
    #for i in range(0,424): #1417
        #my_flow(name="取东莞数据", page=i)
        #parse_html_flow(i) #取第二页数据
                            #取第三页数据
        # time.sleep(3)    

    # df = pd.DataFrame(data)
    # df.to_excel('输出.xlsx')