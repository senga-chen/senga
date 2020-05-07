#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:00 下午 
@name:userAccount.py

"""
from tornado import gen

from models.query import Query

__all__ = ["UserAccountModel"]


class UserAccountModel(Query):
    def __init__(self):
        self.table_name = "senga_user_account"
        super(UserAccountModel, self).__init__()

    @gen.coroutine
    def get_login_user(self, username, password):
        ret = None
        cur = yield self.field("user_id, token").where("username='%s' and password='%s'" % (username, password)).select()
        if cur.rowcount > 0:
            tmp = cur.fetchone()
            ret = dict(zip(["user_id", "token"], tmp))
        raise gen.Return(ret)

    @gen.coroutine
    def update_account_token(self, user_id, token):
        data = {
            "token": token
        }
        yield self.data(data).where("user_id=%s" % user_id).update()


if __name__ == "__main__":
    pass