#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   items.py
@Time    :   2023/04/19 21:03:40
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   投资网取出BAID, 然后给tab_ba_detail.py去查询详情
"""
import os
import sys

# 引入上一级或兄弟子目录的文件
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
fp = sys.path.append(parent)

from peewee import *
import datetime
from typing import Optional
import json
from utils.common import *
from db_pool import *


class BeiAn(BaseModel):
    baId = CharField(
        50,
        verbose_name="项目ID",
        primary_key=True,
    )
    projectCode = CharField(100, verbose_name="备案项目编号")
    totalMoney = FloatField(verbose_name="金额")
    fullName = CharField(100, verbose_name="项目业主")
    finishDate = CharField(50, verbose_name="备案通过日期")
    stateFlagName = CharField(50, verbose_name="状态")
    projectName = CharField(200, verbose_name="项目名称")
    createDate = DateTimeField(default=datetime.now, verbose_name="创建日期")
    updatedDate = DateTimeField(default=datetime.now, verbose_name="更新日期")
    isGet = IntegerField(default=0, verbose_name="已取")

    class Meta:
        db_table = "tab_beian"

    # 计算属性元
    @property
    def money(self):
        return "%d" + self.totalMoney * 1000

    @staticmethod
    @db.atomic()
    def insert__from_list(data_list: list):
        """
        数据批量插入数据库
        data_list = [{"baId": "1"...},{},]
        """
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
        ).on_conflict_ignore(ignore=True).execute()


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
    with db.connection_context():
        db.connect(reuse_if_open=True)
        if not BeiAn.table_exists():
            print("表不存在,创建中", BeiAn.table_exists)
            db.create_tables([BeiAn])

        BeiAn.insert__from_list(data_list)
        print(db.is_closed())
