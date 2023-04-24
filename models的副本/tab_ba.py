#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   items.py
@Time    :   2023/04/19 21:03:40
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   None
"""
import os
import sys

# 引入上一级或兄弟子目录的文件
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

fp = sys.path.append(os.pardir)
from peewee import *
import datetime
from typing import Optional
import setting
from utils.common import *
import json

# db = MySQLDatabase(
#     setting.MYSQL_DB,
#     host=setting.MYSQL_IP,
#     port=setting.MYSQL_PORT,
#     user=setting.MYSQL_USER_NAME,
#     password=setting.MYSQL_USER_PASS,
# )
# fn = os.getcwd() + "/db.db"
# db = SqliteDatabase(fn)
# db.connect()

db = MySQLDatabase(
    "bid",
    **{
        "charset": "utf8",
        "sql_mode": "PIPES_AS_CONCAT",
        "use_unicode": True,
        "host": "ooo.dgpms.cn",
        "port": 3306,
        "user": "bid",
        "password": "gcmc@0769",
    }
)


class BaseModel(Model):
    class Meta:
        database = db


class TabBa(BaseModel):
    id = BigAutoField()
    data_id = CharField(null=True)
    add_time = CharField(null=True)
    apply_organ = CharField(null=True)
    begin_date = DateField(null=True)
    expiry_date = DateField(null=True)
    finish_date = DateField(null=True)
    full_name = CharField(null=True)
    has_start = IntegerField(null=True)
    is_validity = CharField(null=True)
    note = CharField(null=True)
    over_date = DateField(null=True)
    place = CharField(null=True)
    project_name = CharField(null=True)
    proof_or_serial_code = CharField(null=True)
    scope = TextField(null=True)
    sfjz = CharField(null=True)
    state_flag_name = CharField(null=True)
    submit_date = CharField(null=True)
    total_invest = IntegerField(null=True)
    update_time = CharField(null=True)

    class Meta:
        table_name = "tab_ba"


if not TabBa.table_exists:
    TabBa.create_table()

# di ={
#         "overDate": "2024-05-01",
#         "note": null,
#         "addTime": null,
#         "proofOrSerialCode": "2304-441900-04-01-135254",
#         "submitDate": "2023/04/20 21:22:12",
#         "fullName": "东莞市长安镇经济发展局",
#         "updateTime": "2023/04/21 09:26:50",
#         "expiryDate": "2025-04-21",
#         "applyOrgan": "广东聚鑫新能源科技有限公司",
#         "beginDate": "2023-04-01",
#         "hasStart": 0,
#         "sfjz": "0",
#         "scope": "广东聚鑫新能源科技有限公司在建筑楼顶上建设101.26kWp 分布式光伏发电项目,拟安装415w单晶硅太阳能电池板244块, 拟占用屋顶面积约557平方米;年平均发电约11万kWp,产品 技术及系统安装符合相关国家和行业标准。",
#         "finishDate": "2023-04-21",
#         "id": "1649223131300102146",
#         "place": "东莞市长安镇振安东路155号",
#         "stateFlagName": "办结（通过）",
#         "projectName": "东莞市长安镇振安东路155号101.26kWp分布式光伏发电项目",
#         "totalInvest": 50,
#         "isValidity": "有效"
#     }


def insert_from_dict(json_str: str):
    if json_str == "":
        return False
    di = json.loads(json_str)
    if di["status"] != 200:
        return False
    p = TabBa()
    p.data_id = di["data"]["id"]
    p.add_time = di["data"]["addTime"]
    p.apply_organ = di["data"]["applyOrgan"]
    p.begin_date = di["data"]["beginDate"]
    p.expiry_date = di["data"]["expiryDate"]
    p.finish_date = di["data"]["finishDate"]
    p.full_name = di["data"]["fullName"]
    p.has_start = di["data"]["hasStart"]
    p.is_validity = di["data"]["isValidity"]
    p.note = di["data"]["note"]
    p.over_date = di["data"]["overDate"]
    p.place = di["data"]["place"]
    p.project_name = di["data"]["projectName"]
    p.proof_or_serial_code = di["data"]["proofOrSerialCode"]
    p.scope = di["data"]["scope"]
    p.sfjz = di["data"]["sfjz"]
    p.state_flag_name = di["data"]["stateFlagName"]
    p.submit_date = di["data"]["submitDate"]
    p.total_invest = di["data"]["totalInvest"]
    p.update_time = di["data"]["updateTime"]
    p.save()
    return True


# s = '{"code":"0","data":{"overDate":"2024-05-01","note":null,"addTime":null,"proofOrSerialCode":"2304-441900-04-01-135254","submitDate":"2023/04/20 21:22:12","fullName":"东莞市长安镇经济发展局","updateTime":"2023/04/21 09:26:50","expiryDate":"2025-04-21","applyOrgan":"广东聚鑫新能源科技有限公司","beginDate":"2023-04-01","hasStart":0,"sfjz":"0","scope":"广东聚鑫新能源科技有限公司在建筑楼顶上建设101.26kWp 分布式光伏发电项目,拟安装415w单晶硅太阳能电池板244块, 拟占用屋顶面积约557平方米;年平均发电约11万kWp,产品 技术及系统安装符合相关国家和行业标准。","finishDate":"2023-04-21","id":"1649223131300102146","place":"东莞市长安镇振安东路155号","stateFlagName":"办结（通过）","projectName":"东莞市长安镇振安东路155号101.26kWp分布式光伏发电项目","totalInvest":50.0000,"isValidity":"有效"},"message":"查询成功！","status":200}'
# insert_from_dict(s)
