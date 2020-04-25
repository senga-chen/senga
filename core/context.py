#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:44 下午 
@name:context.py

"""
from tornado_mysql import pools

from core import Service, Model
from core.autoload import Autoload


class __ApplicationContext():
    def __int__(self):
        self.__mysql_pools = None
        self.__config = None

    def mysql_setup(self, host="localhost", port=0, user="root", passwd="", db="", max_idle_connections=10, max_recycle_sec=3, max_open_connections=100):
        mysql_conf = dict(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db,
            charset="utf8mb4"
        )
        self.__mysql_pools = pools.Pool(
            mysql_conf,
            max_idle_connections=max_idle_connections,
            max_recycle_sec=max_recycle_sec,
            max_open_connections=max_open_connections
        )

    def config_setup(self, config):
        self.__config = config

    def autoload_models(self, context):
        autoload = Autoload(context)
        autoload.autoload()

    def service(self, key):
        return Service(key)

    def model(self, key):
        return Model(key)

    @property
    def mysql_pool(self):
        return self.__mysql_pools

    @property
    def config(self):
        return self.__config


senga_app = __ApplicationContext()

if __name__ == "__main__":
    pass