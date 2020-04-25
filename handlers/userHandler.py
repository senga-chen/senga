#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 12:59 下午 
@name:userHandler.py

"""
from schema import Schema, Use
from tornado import gen

from core.context import senga_app
from handlers import DefaultHandler


class UserHandler(DefaultHandler):
    @gen.coroutine
    def get(self):
        schema = Schema({"user_id": Use(int)})
        args = self.input(schema)
        if args is None:
            return
        user_id = args.get("user_id", 0)
        ret = yield senga_app.service("UserService").userinfo(user_id)
        self.write_json(ret)


if __name__ == "__main__":
    pass