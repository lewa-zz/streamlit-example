#!/usr/bin/python3
# -*- coding: utf-8 -*-

from playwright.sync_api import Playwright, sync_playwright, expect
import time
import requests
from PIL import Image
from io import BytesIO
import ddddocr
import pandas as pd
from pandas import DataFrame
import re
import sqlite3
from datetime import datetime 

def write_excel(data):
    '''
    写一个全新的文件也很简单：
    data = {'name': ['zs', 'ls', 'ww'], 'age': [
        11, 12, 13], 'gender': ['man', 'man', 'woman']}
    '''
    df = pd.DataFrame(data)
    df.to_excel('new.xlsx')

def create_db():
    # 创建与数据库的连接
    conn = sqlite3.connect('db.sqlite3')
    # 建表的sql语句
    sql_text_1 = '''CREATE TABLE scores
            (姓名 TEXT,
                班级 TEXT,
                性别 TEXT,
                语文 NUMBER,
                数学 NUMBER,
                英语 NUMBER);'''
    #创建一个游标 cursor
    cur = conn.cursor()
    # 执行sql语句
    cur.execute(sql_text_1)
    # 插入单条数据
    sql_text_2 = "INSERT INTO scores VALUES('A', '一班', '男', 96, 94, 98)"
    cur.execute(sql_text_2)
    # 提交改动的方法
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()

def popup(context,row):
    with context.expect_page() as new_page_info:
        row.click() # Opens a new tab
    new_page = new_page_info.value
    new_page.wait_for_load_state()    
    #print(new_page.title())
    prj_name       = new_page.locator('#print-content > p').text_content() #项目名称
    budget      = new_page.locator("#f_budget").text_content() #预算金额字符串
    budget      = float(budget[len("预算金额："):-2].replace(",","")) #转成float,取出数值，过滤逗号

    buye_type   = new_page.locator("#f_catalogueNameList").text_content() #采购品目
    buyer_plan  = new_page.locator("#f_openTenderCode").text_content()  #采购计划编号
    buyer_time  = new_page.locator("#f_noticeTime").text_content()  #发布时间: xxxx-xx-xx hh:mm:ss
    buyer_time  = buyer_time[len("发布时间："):]           #取出日期字串
    buyer_time  = datetime.strptime(buyer_time,'%Y-%m-%d %H:%M:%S') #转换成日期类型
    
    #agaent =  new_page.locator('//*[@id="noticeArea"]').locator('//*[@class="innercontent"]')
    #方法二、通过">" 通过上级> 下级 定位
    agaent = new_page.locator('#noticeArea > .innercontent > p').all()
    # for a in agaent:
    #     print(a.text_content())
    #agaent.screenshot(path=f"采购人信息%d.png"%i)
    buyer         = agaent[0].text_content()
    buyer_address = agaent[1].text_content()
    buyer_phone   = agaent[2].text_content()
    #print("采购人：%s 地址：%s 电话：%s "%(buyer,buyerAddress,buyerPhone))
    new_page.close()
    return locals()

def run(playwright: Playwright) -> None:
    data = {'序号':[],'href':[],'项目':[],'项目1':[],'局办':[],'类目':[],'采购编号':[],'金额':[],'时间':[]}  #data= dict()
    base_url:str = r"https://gdgpo.czt.gd.gov.cn/"

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://gdgpo.czt.gd.gov.cn/cms-gd/site/guangdong/xmcggg/index.html")
    page.wait_for_timeout(1000)
    #page.wait_for_selector("text=请选择区域")
    #time.sleep(8) 不用这个方法等
    page.get_by_placeholder("请选择区域").click()
    page.get_by_placeholder("请选择区域").fill("东莞市")
    page.get_by_title("东莞市").click()
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
    #amo      = int(re.findall(r'\d+(\.\d+)?',page_amo)[0]
    i=0
    j=1
    #循环取出记录,打开页面.
    while i < rec_total:
    #for j in range(0,page_amo):
        #每页的记录 id为procurementAnnouncementShowList下级的li中的a标签
        #li = page.locator('//*[@id="procurementAnnouncementShowList"]/li/a')
        li = page.locator('#procurementAnnouncementShowList').locator("a")
        #print(li.text_content())
        #j+=1
        for row in li.all():
            data['序号'].append(i)
            cc = base_url+str(row.get_attribute("href"))
            data['href'].append(base_url+str(row.get_attribute("href")))
            data['项目'].append(row.text_content())
            print("序号:【%d】 %s , 【url】%s\n"%(i,cc,row.text_content()))
            i += 1
            di:dict = popup(context,row)
            data['项目1'].append(di['prj_name'])
            data['局办'].append(di['buyer'])   
            data['类目'].append(di['buye_type'])
            data['采购编号'].append(di['buyer_plan'])
            data['金额'].append(di['budget'])
            data['时间'].append(di['buyer_time'])
            #print(data)
        #每页做完,点下一页继续.
        #ID为pagination下面的<li>></li> text是精准,不用has_text
        print("记录i: %d , 第J页 is %d"%(i,j))
        #if j <= page_amo-1: #最后一页不用点
        if i < rec_total: 
            page.locator('#pagination').locator('li:text(">")').click()
            page.wait_for_timeout(2000)
            #page.wait_for_load_state()
            j += 1
        

    write_excel(data)
    print("-----------end-------------")

    
    '''
    查询totalpage，出来的是一个数组，
    <li class="totalPage">…</li> aka get_by_text("跳转到页")
    2) <li class="totalPage">共 104 页</li> aka get_by_text("共 104 页")
    3) <li class="totalPage">每页 10 条</li> aka get_by_text("每页 10 条")
    4) <li class="totalPage">合计 1031 条数据</li> aka get_by_text("合计 1031 条数据")
    '''
    #page.locator('//*[@class="totalPage"][2]').screenshot(path=f"totalpages.png")
    #page.locator("text=/共 \s* 页").screenshot(path=f"totalpagesre.png")
    #page.get_by_text(re.compile('^(共)*? 页$')).screenshot(path=f"totalpagesre.png") 正则错
    #==================================================================
    #page.locator("text=''/共%d页").screenshot(path=f"多少页.png")
    page.locator('li:has-text("共")').screenshot(path=f"totalpagesre.png") 
    print("------------------------")
    print('多少页：%s ,\n inner text is : ',page.locator('li:has-text("共")').text_content())

    for row in  page.locator('//*[@class="totalPage"]').all(): #page.get_by_role("listitem"). filter(has_text="共").all():
        print(row.text_content())

    print("------------------------")
    page.close()

    # ---------------------
    context.close()
    browser.close()

def imgtostr():
    url =f'https://gdgpo.czt.gd.gov.cn/freecms/verify/verifyCode.do?createTypeFlag=n&name=notice&d1678761066566'
    response = requests.get(url)
    response = response.content
    ocr =  ddddocr.DdddOcr(old=True)
    res =  ocr.classification(response)
    print(res)

    #写到内存中显示
    BytesIOObj = BytesIO()
    BytesIOObj.write(response)
    img = Image.open(BytesIOObj)
    img.show()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)

    #imgtostr()