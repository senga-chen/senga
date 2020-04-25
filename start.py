#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 7:16 下午
@name:start.py
tornado websocket_test
"""
import logging
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.escape
from tornado.options import define, options

from common import cmd
from core.context import senga_app
from handlers.chatHandler import ChatSocketHandler
from handlers.indexHandler import MainHandler
from handlers.messageHandler import MessageHandler
from handlers.userHandler import UserHandler

define("port", default=8080, type=int)


class SengaApp():
    def __int__(self):
        self.config = None

    def boot_start(self):
        self.config = cmd.parse_cmd("senga")
        senga_app.config_setup(self.config)
        senga_app.mysql_setup(**self.config.get("mysql"))
        senga_app.autoload_models(self)


def main():
    tornado.options.parse_command_line()
    handlers = [
        (r'/', MainHandler),
        (r'/chatsocket', ChatSocketHandler),
        (r'/message', MessageHandler),
        (r'/userinfo', UserHandler),
    ]
    settings = dict(
        template_path="templates",
        static_path="statics",
        debug=True
    )
    app = tornado.web.Application(handlers, **settings)
    app_boot = SengaApp()
    app_boot.boot_start()
    app.listen(options.port)
    logging.info("Start server at http://127.0.0.1:%s" % options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
