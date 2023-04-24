#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import re
import sqlite3
from datetime import datetime 
import xlsxwriter

def place(name:str) -> str:
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


def clearDirtyData(file_path:str)-> None:
    '''
    把金额清理一下
    '''
     # sheet_name不指定时默认返回全表数据
    df = pd.read_excel(file_path, sheet_name="中选公示信息总列表2021-2023内容输出")
    #总行列数,返回[12723,17]
    print(df.shape)
    amolist = []
    datelist = []
    for index, row in df.iterrows():
        print('the index is ', index)
        amo = row['服务金额'] #or using this : df.loc[index,"服务金额"]
        print(row['服务金额'])
        # print(row['监理手机'])
        
        #利用正则清洗金额
        _kk = re.compile(r'\d+\.?\d+') #正则中小数点加\转义,不然.就识别任一字符
        kk = re.findall(_kk,amo.replace(",",""))
        amo = float(kk[0]) if len(kk) != 0 else 0
        amolist.append(amo)
        #df[index,'清洗后金额'] = amo
        
        # #利用正则取出日期
        _kk = re.compile(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}') #正则中小数点加\转义,不然.就识别任一字符
        kk = re.findall(_kk,row['说明'])
        thedate = str(kk[0]) if len(kk) != 0 else "2000-01-01 00:00"
        thedate = datetime.strptime(thedate,"%Y-%m-%d %H:%M")
        #df[index,"清洗日期1"] = thedate
        datelist.append(thedate)

    df["清洗后金额"] = amolist
    df["清洗后日期"] = datelist
    print(df)
    outfile = r'/Users/ricochen/Desktop/分析/output1.xlsx'
    df.to_excel(outfile)
    #数据量大时用下面的ExcelWriter不会溢出
    # writer = pd.ExcelWriter(outfile, engine='xlsxwriter')#, options={'strings_to_urls':False})  # options参数可带可不带，根据实际情况
    # df.to_excel(writer, index=False)
    # writer.save()
    

if __name__ == "__main__":
    file_path = r'/Users/ricochen/Desktop/分析/ww中选公示信息总列表2021-2023.xlsx'
    clearDirtyData(file_path)