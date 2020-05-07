#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 12:59 下午 
@name:userHandler.py

"""
from schema import Schema, Use, And
from tornado import gen

from core.context import senga_app
from handlers import DefaultHandler


class UserHandler(DefaultHandler):
    @gen.coroutine
    def get(self):
        schema = Schema({"user_id": Use(int)})
        args = self.input(schema, need_token=False)
        if args is None:
            return
        user_id = args.get("user_id", 0)
        ret = yield senga_app.service("UserService").user_info(user_id)
        self.write_json(ret)


class LoginHandler(DefaultHandler):
    @gen.coroutine
    def post(self):
        schema = Schema({"username": And(str, len), "password": And(str, len)})
        args = self.input(schema, need_token=False)
        if args is None:
            return
        username = args.get("username", "")
        password = args.get("password", "")
        ret = yield senga_app.service("UserService").login(username, password)
        self.write_json(ret)


if __name__ == "__main__":
    pass