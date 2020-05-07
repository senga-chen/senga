#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 7:16 下午
@name:start.py
启动文件
"""
import logging
import os

import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.escape
from tornado.options import define, options

from common import cmd
from core.context import senga_app
from core.rounting import handler_store
from core.socket_client_manage import SocketClientManager

define("port", default=8088, type=int)


class App(object):
    def __init__(self, config, app):
        self.config = config
        self.app = app

    def boot_start(self):
        senga_app.mysql_setup(**self.config.get("mysql"))
        senga_app.redis_setup(**self.config.get('redis'))
        senga_app.autoload_module(self)

        from core.message_client import PikaProducerExector
        PikaProducerExector.instance()

        from core.message_consume import PikaConsumeExector
        PikaConsumeExector.instance()

        self.init_socket_manage()

    def init_socket_manage(self):
        from core.message_consume import client_manager
        self.app.socket_client_manger = SocketClientManager(self)
        client_manager.client_manager = self.app.socket_client_manger


def main():
    try:
        tornado.options.parse_command_line()
        config = cmd.parse_cmd("senga")
        senga_app.config_setup(config)
        handlers = handler_store()
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "statics"),
            debug=config.get("debug", False),
            cookie_secret=config.get("secert_key", None)
        )
        app = tornado.web.Application(handlers, **settings)
        app_boot = App(config, app)
        app_boot.boot_start()
        app.listen(options.port)
        logging.info("Start server at http://127.0.0.1:%s" % options.port)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()


if __name__ == "__main__":
    main()
