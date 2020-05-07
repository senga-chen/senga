#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:44 下午 
@name:context.py

"""
import sys
import traceback
import urllib
import logging

import redis
import ujson
from elasticsearch import Elasticsearch
from kazoo.client import KazooClient
from tornado import gen
from tornado.concurrent import Future
from tornado.gen import coroutine, Return
from tornado.ioloop import IOLoop
from tornado.locks import Semaphore
from tornado_mysql import connect
from tornado_mysql.cursors import Cursor
from tornado_mysql.pools import Pool
from core import Service, Model
from core.autoload import AutoLoader

LOG = logging


class DCPool(Pool):
    def _get_conn(self):  # -> Future[connection]
        now = self.io_loop.time()

        # Try to reuse in free pool
        while self._free_conn:
            try:
                conn = self._free_conn.popleft()
                if now - conn.connected_time > self.max_recycle_sec:
                    self._close_async(conn)
                    continue
                LOG.debug("Reusing connection from pool: %s, conn: %s", self.stat(), id(conn))
                fut = Future()
                fut.set_result(conn)
                return fut
            except IndexError:
                fut = Future()
                self._waitings.append(fut)
                return fut

        # Open new connection
        if self.max_open == 0 or self._opened_conns < self.max_open:
            self._opened_conns += 1
            LOG.debug("Creating new connection: %s", self.stat())
            fut = connect(**self.connect_kwargs)
            fut.add_done_callback(self._on_connect)  # self._opened_conns -=1 on exception
            return fut

        # Wait to other connection is released.
        fut = Future()
        self._waitings.append(fut)
        return fut

    def _on_connect(self, fut):
        if fut.exception():
            self._opened_conns -= 1

    def _put_conn(self, conn):
        LOG.debug("put conn to pool: %s, conn: %s", self.stat(), id(conn))
        if (len(self._free_conn) < self.max_idle and
                        self.io_loop.time() - conn.connected_time < self.max_recycle_sec):
            if self._waitings:
                try:
                    fut = self._waitings.popleft()
                    fut.set_result(conn)
                    LOG.debug("Passing returned connection to waiter: %s", self.stat())
                except IndexError:
                    self._free_conn.append(conn)
                    LOG.debug("Add conn to free pool: %s", self.stat())
            else:
                self._free_conn.append(conn)
                LOG.debug("Add conn to free pool: %s", self.stat())
        else:
            LOG.debug("close conn from pool: %s, conn: %s", self.stat(), id(conn))
            self._close_async(conn)

    def _close_conn(self, conn):
        LOG.debug("close conn from pool: %s, conn: %s", self.stat(), id(conn))
        conn.close()
        self._after_close()

    @coroutine
    def execute(self, query, params=None, cursor=None):
        """Execute query in pool.

        Returns future yielding closed cursor.
        You can get rows, lastrowid, etc from the cursor.
        :param cursor: cursor class(Cursor, DictCursor. etc.)

        :return: Future of cursor
        :rtype: Future
        """
        conn = yield self._get_conn()
        try:
            LOG.debug("DCPool execute conn id: %s , query: %s, params: %s", id(conn), query, params or "")
            cur = conn.cursor(cursor)
            yield cur.execute(query, params)
            yield cur.close()
        except Exception, e:
            LOG.exception("DCPool Exception, e: %s \n [traceback]: %s", e, traceback.format_exc())
            self._close_conn(conn)
            raise
        else:
            self._put_conn(conn)
        raise Return(cur)


class __ApplicationContext():
    def __init__(self):
        self.__redis = {}
        self.__mysql_pool = None
        self.__config = None

    def redis_setup(self, host='localhost', port=6379, db=0, max_connections=None, key='default', password=None,
                    socket_timeout=None, **connection_kwargs):
        LOG.debug("connect redis %s:%s ,db=%s" % (host, port, db))
        pool = redis.ConnectionPool(host=host, port=port, db=db, max_connections=max_connections, password=password,
                                    socket_timeout=socket_timeout, **connection_kwargs)
        self.__redis[key] = redis.StrictRedis(connection_pool=pool)
        LOG.info("redis %s finish. %s" % (key, self.redis_check(key)))

    def mysql_setup(self, host='localhost', port=3306, user='root',
                    passwd='root', db='amazsic', charset='utf8mb4', max_idle_connections=10, max_open_connections=100,
                    autocommit=True, **connection_kwargs):
        LOG.debug("connect mysql_pool %s:%s db=%s" % (host, port, db))
        self.__mysql_pool = DCPool(
            dict(host=host, port=port, user=user,
                 passwd=passwd, db=db, charset=charset, autocommit=autocommit),
            max_idle_connections=max_idle_connections, max_open_connections=max_open_connections, max_recycle_sec=connection_kwargs.get("max_recycle_sec", 3600))
        # flag = IOLoop.instance().run_sync(self.check)
        # LOG.debug("mysql finish? %s" %(flag))

    # def route_setup(self, application):
    #     from handlers.views import route
    #     for host_pattern, host_handlers in route.urls.items():
    #         LOG.debug("register host:{0}, url:{1}".format(host_pattern, len(host_handlers)))
    #         application.add_handlers(host_pattern, host_handlers)

    def config_setup(self, config):
        self.__config = config

    def get_redis(self, key='default'):
        return self.__redis[key]

    @property
    def redis(self):
        return self.get_redis()

    @property
    def cache_redis(self):
        return self.get_redis("cache")

    @property
    def config(self):
        return self.__config

    @property
    def mysql_pool(self):
        return self.__mysql_pool

    @classmethod
    def autoload_module(cls, context):
        auto_loader = AutoLoader(context)
        auto_loader.autoload()

    @gen.coroutine
    def check(self):
        if self.__mysql_pool:
            cur = yield self.__mysql_pool.execute("select now()")
            if cur:
                raise gen.Return(True)
        raise gen.Return(False)

    def redis_check(self, key):
        if self.get_redis(key):
            flag = self.get_redis(key).set("app_start", 1, ex=5)
            return flag
        return False

    def service(self, key):
        return Service(key)

    def model(self, key):
        return Model(key)


senga_app = __ApplicationContext()


if __name__ == "__main__":
    pass