#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 1:03 下午 
@name:UserService.py
用户service
"""
from tornado import gen

from core.context import senga_app
from services import BaseService

__all__ = ["UserService"]


class UserService(BaseService):
    @gen.coroutine
    def userinfo(self, user_id):
        user = yield senga_app.model("UserModel").get_user(user_id)
        raise gen.Return(user)


if __name__ == "__main__":
    pass