#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 11:08 下午 
@name:user.py

"""

from tornado import gen
from models.query import Query

__all__ = ["UserModel"]


class UserModel(Query):
    def __init__(self):
        self.table_name = "senga_user"
        super(UserModel, self).__init__()

    class Meta:
        fields = ["id", "name", "age", "description"]

    @gen.coroutine
    def get_user(self, user_id):
        ret = None
        cur = yield self.field(','.join(self.Meta.fields)).where("id=%s" % user_id).select()
        if cur.rowcount > 0:
            user = cur.fetchone()
            ret = dict(zip(self.Meta.fields, user))
        raise gen.Return(ret)


if __name__ == "__main__":
    pass