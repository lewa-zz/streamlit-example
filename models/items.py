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
import json
from utils.common import *

# db = MySQLDatabase(
#     setting.MYSQL_DB,
#     host=setting.MYSQL_IP,
#     port=setting.MYSQL_PORT,
#     user=setting.MYSQL_USER_NAME,
#     password=setting.MYSQL_USER_PASS,
# )
fn = os.getcwd() + "/db.db"
db = SqliteDatabase(fn)
db.connect()


# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = db


class BeiAn(BaseModel):
    baId = CharField(50, verbose_name="项目ID")
    projectCode = CharField(100, verbose_name="备案项目编号")
    totalMoney = FloatField(verbose_name="金额")
    fullName = CharField(100, verbose_name="项目业主")
    finishDate = CharField(50, verbose_name="备案通过日期")
    stateFlagName = CharField(50, verbose_name="状态")
    projectName = CharField(200, verbose_name="项目名称")
    createDate = DateTimeField(default=datetime.now)
    updatedDate = DateTimeField(default=datetime.now)
    isGet = IntegerField()

    #
    class Meta:
        db_table = "beian"

    # 计算属性万元
    @property
    def amo_m(self):
        return "%d万" + self.totalMoney / 1000


def create_tables():
    db.create_tables([BeiAn])  # or  BeiAn.create_table()


# @db.atomic()
def insert__from_list(data_list: list):
    """
    数据批量插入数据库
    data_list = [{"baId": "1"...},{},]
    """
    import beeprint

    # with db.atomic():
    # for row in data_list:
    #     beeprint.pp(row)
    #     p = ne
    # BeiAn.insert(row,fields).execute()
    BeiAn.insert_many(
        data_list,
        fields=[
            "baId",
            "projectCode",
            "totalMoney",
            "fullName",
            "finishDate",
            "stateFlagName",
            "projectName",
        ],
    ).execute()


if not BeiAn.table_exists:
    create_tables()

if __name__ == "__main__":
    data_list = [
        {
            "baId": "1649223131300102146",
            "projectCode": "2304-441900-04-01-135254",
            "totalMoney": 50,
            "fullName": "东莞市长安镇经济发展局",
            "finishDate": "2023-04-21",
            "stateFlagName": "办结（通过）",
            "projectName": "东莞市长安镇振安东路155号101.26kWp分布式光伏发电项目",
        },
        {
            "baId": "1649223156969242625",
            "projectCode": "2304-441900-04-01-386559",
            "totalMoney": 20,
            "fullName": "东莞市长安镇经济发展局",
            "finishDate": "2023-04-21",
            "stateFlagName": "办结（通过）",
            "projectName": "东莞市长安镇霄边上洋路17号35.69kWp分布式光伏发电项目",
        },
    ]
    create_tables()
    # insert__from_list(data_list)
    # print(db.is_closed())
    # print(printa("asdfdsfdsfdsafdsaf"))
