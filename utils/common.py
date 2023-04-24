# coding=utf-8
"""
    @File    : utils.py
    @Author  : rico
    @Date    : 2023/4/10 23:07
    @Desc    : 一些常用、可重复使用的函数
"""
import os
import orjson
import pandas as pd
import re
import time
import sqlite3
from datetime import datetime
from pandas.io.json import json_normalize

import requests
from PIL import Image
from io import BytesIO
import ddddocr


def imgtostr(
    url=f"https://gdgpo.czt.gd.gov.cn/freecms/verify/verifyCode.do?createTypeFlag=n&name=notice&d1678761066566",
):
    """
    网站的验证码图片转成文字
    """
    # url =f'https://gdgpo.czt.gd.gov.cn/freecms/verify/verifyCode.do?createTypeFlag=n&name=notice&d1678761066566'
    response = requests.get(url)
    response = response.content
    ocr = ddddocr.DdddOcr(old=True)
    res = ocr.classification(response)
    # print(res)

    # 写到内存中显示
    # BytesIOObj = BytesIO()
    # BytesIOObj.write(response)
    # img = Image.open(BytesIOObj)
    # img.show()
    return res


def get_digit(amo: str) -> float:
    """
    根据正则,提取字串中相应的金额数字,没有即为0
    输入:amo带数字的字串
    输出:浮点数字
    """
    _kk = re.compile(r"\d+\.?\d+")  # 正则中小数点加\转义,不然.就识别任一字符
    kk = re.findall(_kk, amo.replace(",", ""))
    return float(kk[0]) if len(kk) != 0 else 0


def json_append_cvs(json, csvfile):
    """
    REST返回的json的DATA数据和同级的MSG和code,写入EXCEL文件
    {msg:"操作成功“,code:200,
    data:[
    {name:"",sex:"",...},
    {name:"",sex:"",...},{name:"",sex:"",...}
    ....
    ]}
    输入:
        fn:输入JSON文件
        fout:输出EXCEL文件
    输出:None
    """
    df = pd.json_normalize(json, "data", ["msg", "code"])
    # df.to_excel(fnout,encoding='utf-8')
    # 利用A mode追,to_excel无这模式
    df.to_csv(csvfile, index=False, encoding="utf-8", sep="\t", mode="a", header=True)
    # 可以使用Python的`extend()`方法将两个JSON数据的"data"字段中的内容进行合并，示例代码如下：


def jsonfile_append_cvs(jsonfile, csvfile):
    """
    json 文件中的DATA数据和同级的MSG和code,追加写入csv文件
    {msg:"操作成功“,code:200,
    data:[
    {name:"",sex:"",...},
    {name:"",sex:"",...},{name:"",sex:"",...}
    ....
    ]}
    输入:
        fn:输入JSON文件
        fout:输出EXCEL文件
    输出:None
    """
    cwd = os.getcwd()  # 获取当前工作路径
    file = open(jsonfile, "r", encoding="utf-8")
    text = file.read()
    text = orjson.loads(text)
    df = pd.json_normalize(text, "data", ["msg", "code"])
    # df.to_excel(fnout,encoding='utf-8')
    # 利用A mode追,to_excel无这模式
    df.to_csv(
        r"%s/result.csv" % cwd,
        index=False,
        encoding="utf-8",
        sep="\t",
        mode="a",
        header=True,
    )
    # 可以使用Python的`extend()`方法将两个JSON数据的"data"字段中的内容进行合并，示例代码如下：


def json_data_merge(json1, json2, merge_str: str = "data"):
    """
    合并Json中的DATA项
    输入:
        输入原始JSON数据
        json1 = u'{"msg": "操作成功", "total": 46, "code": "200", "data": [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]}'
        json2 = u'{"msg": "操作成功", "total": 46, "code": "200", "data": [{"id": 3, "name": "王五"}, {"id": 4, "name": "赵六"}]}'
        merge_str 合并的串名称,一般为DATA
    输出:
        返回合并后的格式化的JSON
    输出结果为：
    {"msg": "操作成功", "total": 46, "code": "200", "data": [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}, {"id": 3, "name": "王五"}, {"id": 4, "name": "赵六"}]}
    可以看到，两个JSON数据中的"data"字段中的内容已经被合并成一个新的JSON数组。
    Created by https://GPTGO.ai
    """

    # 解析JSON数据,将json对象转化为dict对象
    data1 = json1 if type(json1) == "dict" else orjson.loads(json1)
    data2 = json2 if type(json2) == "dict" else orjson.loads(json2)
    # data2 = orjson.loads(json2)

    # 合并数据的列表extend
    # data1["data"].extend(data2["data"])
    data1[merge_str].extend(data2[merge_str])

    # 们用到了json库的dumps方法，将Python对象转化为Json对象
    # json_data = json.dumps(data1, indent=2, separators=(",", " = "))
    json_data = orjson.dumps(data1, option=orjson.OPT_INDENT_2).decode()
    return json_data


def to_jsonfile(fn: str, json_text: str, page: int = 1):
    with open(
        r"./html/%s 第%s页_%s.json"
        % (fn, page, datetime.now().strftime("%Y-%m-%d, %H:%M:%S")),
        "w",
    ) as f:
        f.write(json_text)


def append_to_list(data_list, cache_list: list) -> int:
    """
    把cache_list列表的数据列表加入到data_list列表中
    返回:data_list的长度
    """
    if len(data_list) == 0:
        data_list = cache_list
    else:
        data_list.extend(cache_list)
    return len(data_list)


def printa(str):
    print(str)
