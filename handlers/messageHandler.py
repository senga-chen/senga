#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:16 下午 
@name:messageHandler.py

"""
from schema import Schema, And
from tornado import gen

from core.context import senga_app
from handlers import DefaultHandler


class MessageHandler(DefaultHandler):
    @gen.coroutine
    def get(self):
        schma = Schema({"message": And(str, len)})
        args = self.input(schma)
        if not args:
            return
        message = args.get("message", "")
        ret = yield senga_app.service("MessageService").single_message(1, 2, message)


if __name__ == "__main__":
    pass