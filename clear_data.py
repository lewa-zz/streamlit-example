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

def in_place(name:str) -> str:
    '''
    输入主业名称
    根据主业名称在的位置返回相应的区域
    没有确定的区域信息,即返回空
    '''
    _dg ="东城、南城、万江、莞城、石碣、石龙、茶山、石排、企石、横沥、桥头、谢岗、东坑、常平、寮步、樟木头、大朗、黄江、清溪、塘厦、凤岗、大岭山、长安、虎门、厚街、沙田、道滘、洪梅、麻涌、望牛墩、中堂、高埗、松山湖"
    dg = _dg.split("、")
    #name =input("请输入主业名称，以确定所在区域：").strip()
    o:str =""
    for p in dg:
        if p in name:
            o = p
            break;
    return o

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
    amo_list = []
    place_list = []
    for row_index, row in df.iterrows():
        data2['序号'][row_index] =  row_index
        amo = get_digit(str(row['服务金额']))
        amo_list.append(amo)
        place_list.append(in_place(row["项目业主"]))
    data2["中标金额"] = amo_list
    data2["所属区域"] = place_list
    df = pd.DataFrame(data2)
    df.to_excel('输出.xlsx')  

if __name__ == "__main__":
    #creates a flow run called 'marvin-on-Thursday'
    file_path = r'./总输出.xlsx'
    read_excel(file_path)