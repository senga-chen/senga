#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 1:03 下午 
@name:UserService.py
用户service
"""
import hashlib
import time
import uuid

from tornado import gen

from core.container import RETURN, BusinessException
from core.context import senga_app
from services import BaseService

__all__ = ["UserService"]


class UserService(BaseService):
    @gen.coroutine
    def user_info(self, user_id):
        user = yield self.get_user_info(user_id)
        ret = RETURN.SUCCESS()
        ret.add_attr(user=user)
        raise gen.Return(ret)

    @gen.coroutine
    def get_user_info(self, user_id):
        user = yield senga_app.model("UserModel").get_user(user_id)
        raise gen.Return(user)

    @gen.coroutine
    def login(self, username, password):
        if not username or not password:
            raise gen.Return("用户名密码不可为空")
        password = hashlib.md5(password).hexdigest()
        user_session = yield senga_app.model("UserAccountModel").get_login_user(username, password)
        if user_session:
            user_id = user_session.get("user_id", 0)
            token = user_session.get("token", "")
            user = yield self.get_user_info(user_id)
            if not user:
                raise BusinessException("用户不存在")
            r_uid = "%s_%s" % (str(user_id), str(time.time()))
            if not token:
                token = str(uuid.uuid3(uuid.NAMESPACE_DNS, r_uid)).replace('-', '')
                yield self.content.model("UserAccountModel").update_account_token(user_id, token)
            user["token"] = token
            self.content.redis.set("token:%s" % token, user_id)
            ret = RETURN.SUCCESS()
            ret.add_attr(user=user)
            raise gen.Return(ret)
        else:
            raise BusinessException("用户不存在")


if __name__ == "__main__":
    pass