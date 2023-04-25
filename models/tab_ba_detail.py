#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   items.py
@Time    :   2023/04/19 21:03:40
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   根据tab_beian的isGet为空的记录,取期BaId,
"""
import os
import sys

# 引入上一级或兄弟子目录的文件
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
fp = sys.path.append(parent)
from peewee import *
import datetime
from utils.common import *
import json
from db_pool import *


class TabBa(BaseModel):
    id = CharField(
        50,
        verbose_name="项目ID",
        primary_key=True,
    )
    addTime = CharField(null=True)
    applyOrgan = CharField(100, null=True, verbose_name="建设单位")
    beginDate = DateField(null=True, verbose_name="项目起")
    expiryDate = DateField(null=True, verbose_name="项目")
    finishDate = DateField(null=True, verbose_name="复核通过日期")
    fullName = CharField(100, null=True, verbose_name="备案机关")
    hasStart = IntegerField(null=True, default=0)
    isValidity = CharField(10, null=True, verbose_name="有效?")
    note = CharField(null=True, verbose_name="备注")
    overDate = DateField(null=True, verbose_name="项目止")
    place = CharField(20, null=True, verbose_name="所在地")
    projectName = CharField(100, verbose_name="项目名称")
    proofOrSerialCode = CharField(100, null=True, verbose_name="备案项目编号")
    scope = TextField(null=True, verbose_name="规模及内容")
    sfjz = CharField(null=True)
    stateFlagName = CharField(20, null=True, verbose_name="状态")
    submitDate = DateTimeField("%Y-%m-%d %H:%M:%S", null=True, verbose_name="申报日期")
    totalInvest = IntegerField(null=True, verbose_name="总投资")
    updateTime = DateTimeField(
        "%Y-%m-%d %H:%M:%S", null=True, verbose_name="复核通过日期", default=datetime.now()
    )
    createDate = DateTimeField(default=datetime.now, verbose_name="增加日期")

    class Meta:
        table_name = "tab_ba"

    @staticmethod
    def save_from_dict(di: dict):
        """
        从保存更新一条记录
        """
        p = TabBa()
        p.id = di["data"]["id"]
        p.addTime = di["data"]["addTime"]
        p.applyOrgan = di["data"]["applyOrgan"]
        p.beginDate = di["data"]["beginDate"]
        p.expiryDate = di["data"]["expiryDate"]
        p.finishDate = di["data"]["finishDate"]
        p.fullName = di["data"]["fullName"]
        p.hasStart = di["data"]["hasStart"]
        p.isValidity = di["data"]["isValidity"]
        p.note = di["data"]["note"]
        p.overDate = di["data"]["overDate"]
        p.place = di["data"]["place"]
        p.projectName = di["data"]["projectName"]
        p.proofOrSerialCode = di["data"]["proofOrSerialCode"]
        p.scope = di["data"]["scope"]
        p.sfjz = di["data"]["sfjz"]
        p.stateFlagName = di["data"]["stateFlagName"]
        p.submitDate = di["data"]["submitDate"]
        p.totalInvest = di["data"]["totalInvest"]
        p.updateTime = di["data"]["updateTime"]
        p.save(force_insert=True)
        # 当模型包含非整数字段作为主键时，模型实例的 save() 方法不会导致数据库驱动自动生成新ID，因此我们需要传递 force_insert=True 参数。 但是，请注意 create() 方法隐式指定了 force_insert 参数。
        # save() 方法还会更新表中的现有行，此时不需要 force_insert primary，因为具有唯一主键的 ID 已经存在。

    @staticmethod
    def insert_from_jsonstr(json_str: str):
        """
        众JSON
        """
        if json_str == "":
            return False
        di = json.loads(json_str)
        if di["status"] != 200:
            return False
        TabBa.insert(di["data"]).on_conflict_ignore(ignore=True).execute()
        return True


if __name__ == "__main__":
    di = {
        "overDate": "2024-05-01",
        "note": "",
        "addTime": "2024-05-01",
        "proofOrSerialCode": "2304-441900-04-01-135254",
        "submitDate": "2023/04/20 21:22:12",
        "fullName": "东莞市长安镇经济发展局",
        "updateTime": "2023/04/21 09:26:50",
        "expiryDate": "2025-04-21",
        "applyOrgan": "广东聚鑫新能源科技有限公司",
        "beginDate": "2023-04-01",
        "hasStart": 0,
        "sfjz": "0",
        "scope": "广东聚鑫新能源科技有限公司在建筑楼顶上建设101.26kWp 分布式光伏发电项目,拟安装415w单晶硅太阳能电池板244块, 拟占用屋顶面积约557平方米;年平均发电约11万kWp,产品 技术及系统安装符合相关国家和行业标准。",
        "finishDate": "2023-04-21",
        "id": "1649223131300102146",
        "place": "东莞市长安镇振安东路155号",
        "stateFlagName": "办结（通过）",
        "projectName": "东莞市长安镇振安东路155号101.26kWp分布式光伏发电项目",
        "totalInvest": 50,
        "isValidity": "有效",
    }

    s = '{"code":"0","data":{"overDate":"2024-05-01","note":null,"addTime":null,"proofOrSerialCode":"2304-441900-04-01-135254","submitDate":"2023/04/20 21:22:12","fullName":"东莞市长安镇经济发展局","updateTime":"2023/04/21 09:26:50","expiryDate":"2025-04-21","applyOrgan":"广东聚鑫新能源科技有限公司","beginDate":"2023-04-01","hasStart":0,"sfjz":"0","scope":"广东聚鑫新能源科技有限公司在建筑楼顶上建设101.26kWp 分布式光伏发电项目,拟安装415w单晶硅太阳能电池板244块, 拟占用屋顶面积约557平方米;年平均发电约11万kWp,产品 技术及系统安装符合相关国家和行业标准。","finishDate":"2023-04-21","id":"1649223131300102146","place":"东莞市长安镇振安东路155号","stateFlagName":"办结（通过）","projectName":"东莞市长安镇振安东路155号101.26kWp分布式光伏发电项目","totalInvest":50.0000,"isValidity":"有效"},"message":"查询成功！","status":200}'

    with db.connection_context():
        db.connect(reuse_if_open=True)
        if not TabBa.table_exists():
            print("表不存在,创建中")
            db.create_tables([TabBa])

        # TabBa.insert(di).execute()
        TabBa.insert_from_jsonstr(s)
        # TabBa.save_from_dict(di)
