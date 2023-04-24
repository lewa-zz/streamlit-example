# coding=utf-8
"""
    @Project ：playwright_env 
    @File    ：test.py
    @Author  ：gaojs
    @Date    ：2022/8/20 18:07
    @Blogs   : https://www.gaojs.com.cn
    中标金额为0的,再查第三页,拟服务金额及过清洗
"""
from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
import re,time
import sqlite3
from datetime import datetime 
from prefect import task, flow, get_run_logger
# 创建playwright对象
p = sync_playwright().start()
browser = p.chromium.launch(headless=False, devtools=False)

#在采购公告页数据，主要取规模等
@flow(flow_run_name="处理第--{num}--数据")
def popup_page3(href: str,num)-> str :
   # 创建playwright对象
    #p = sync_playwright().start()
    # headless：默认为true，无头模式   # devtools默认为false:开发者工具默认关闭
    # 浏览器对象:, args=["--start-maximized"]最大化没生效

    # 上下文管理器对象
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    # 页面对象
    new_page = context.new_page()
    new_page.set_default_navigation_timeout(20000)

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

    #_servie_amo =new_page.locator('.detail__content > ul > li:has-text("服务金额")').locator("div").filter(has=locator('b:has-text("服务金额")'))
    try:
        servie_amo =new_page.locator('//b[text()="服务金额"]/../div').text_content()
    except:
        servie_amo = 0
    print(href)

    new_page.close()
    context.close()
    #browser.close()
    # time.sleep(2)
    return servie_amo


def get_digit(amo:str) -> float:
    '''
    根据正则,提取字串中相应的金额数字,没有即为0
    '''
    _kk = re.compile(r'\d+\.?\d+') #正则中小数点加\转义,不然.就识别任一字符
    kk = re.findall(_kk,amo.replace(",",""))
    return float(kk[0]) if len(kk) != 0 else 0

def read_excel(file_path):
    '''
    pandas读excel
    1、根据EXCEL上的服务金额提取出中标金额.
    2、根据业主名称,确定主业所在那个镇街
    并写入到文件:输出.xlsx
    '''
    #file_path = r'./总输出.xlsx'
    # sheet_name不指定时默认返回全表数据
    df = pd.read_excel(file_path, sheet_name="Sheet1", header=0)
    # 打印列标题,即表头
    print(df.columns)
    total_rows = len(df)
    print('总数:{0} 行数{1}', format(df.index.size), str(total_rows))
    data2 = df.to_dict(orient='list')
    j=0
    serlist = []
    for row_index, row in df.iterrows():
        #data2['序号'][row_index] =  row_index
        if row["拟服务金额"] == 0: #或者是用中标金额?
            service_amo = popup_page3(row["to_page3"],j)
            #amo = get_digit(str(row['服务金额']))
            data2["拟服务金额"][row_index] = service_amo
            j += 1

        if j == 20: #每20条存一次盘吧
            df = pd.DataFrame(data2)
            df.to_excel('888输出.xlsx')
            j=0
    df = pd.DataFrame(data2)
    df.to_excel('888输出.xlsx')  
   
def clear_excel(file_path):
    '''
    pandas读excel
    1、清洗拟服务金额为数字
    并写入到文件:输出.xlsx
    '''
    #file_path = r'./总输出.xlsx'
    # sheet_name不指定时默认返回全表数据
    df = pd.read_excel(file_path, sheet_name="Sheet1", header=0)
    # 打印列标题,即表头
    print(df.columns)
    total_rows = len(df)
    print('总数:{0} 行数{1}', format(df.index.size), str(total_rows))
    data2 = df.to_dict(orient='list')

    for row_index, row in df.iterrows():
        service_amo = get_digit(str(row['拟服务金额']))
        data2["拟服务金额"][row_index] = service_amo

    df = pd.DataFrame(data2)
    df.to_excel('输出.xlsx')  

if __name__ == "__main__":
    #creates a flow run called 'marvin-on-Thursday'
    file_path = r'./总输出.xlsx'
    #read_excel(file_path)
    clear_excel(file_path)
    browser.close()


