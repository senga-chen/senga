#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 9:56 下午 
@name:chatHandler.py

"""
import logging
import tornado.websocket
from tornado import gen
from core.context import senga_app
from core.socket_client_manage import WebSocketUser


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(ChatSocketHandler, self).__init__(application, request, **kwargs)
        self.web_socket_user = None
        self.opened = False

    def open(self, *args, **kwargs):
        user = self.init_user()
        user.set_user_client(self)
        self.web_socket_user = user
        self.application.socket_client_manger.register_client(user)

    def on_close(self):
        self.opened = False

    def init_user(self):
        # token = "token" in self.request.arguments and self.request.arguments["token"][0] or ""
        # if token:
            # operator_id = senga_app.redis.get("token:%s" % token)
        operator_id = 1
        if operator_id:
            self.opened = True
            return WebSocketUser(operator_id)
        else:
            return None

    @gen.coroutine
    def on_message(self, message):
        logging.info("get message ==> %s" % message)
        self.web_socket_user.ping_active()
        yield senga_app.service("MessageService").single_message(1, 2, message)


if __name__ == "__main__":
    pass