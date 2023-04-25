#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   db_pool.py
@Time    :   2023/04/24 15:33:17
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   peewee 数据库重连，连接池数量连接
"""

from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from peewee import *
import setting
import os, sys

sys.path.append(os.pardir)


class RetryMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    _instance = None

    @staticmethod
    def get_db_instance():
        if not RetryMySQLDatabase._instance:
            RetryMySQLDatabase._instance = RetryMySQLDatabase(
                setting.MYSQL_DB,
                max_connections=8,
                stale_timeout=300,
                host=setting.MYSQL_IP,
                port=setting.MYSQL_PORT,
                user=setting.MYSQL_USER_NAME,
                password=setting.MYSQL_USER_PASS,
                # autoconnect=False,
            )
        return RetryMySQLDatabase._instance


db = RetryMySQLDatabase.get_db_instance()


class BaseModel(Model):
    class Meta:
        database = db


# fn = os.getcwd() + "/db.db"
# db = SqliteDatabase(fn)

# 如何使用？
# 在model文件中
# db = RetryMySQLDatabase.get_db_instance()

# 为了不用不停的连接断开peewee提供with 操作
# with db.connection_context():
#     Person.select()
#     ....
