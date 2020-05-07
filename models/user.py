#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 11:08 下午 
@name:user.py

"""

from tornado import gen
from models.query import Query

__all__ = ["UserModel", "ChatTeamModel"]


class UserModel(Query):
    def __init__(self):
        self.table_name = "senga_user"
        super(UserModel, self).__init__()

    class Meta:
        fields = ["id", "name", "age", "description", "cover"]

    @gen.coroutine
    def get_user(self, user_id):
        ret = None
        cur = yield self.field(','.join(self.Meta.fields)).where("id=%s" % user_id).select()
        if cur.rowcount > 0:
            user = cur.fetchone()
            ret = dict(zip(self.Meta.fields, user))
        raise gen.Return(ret)


class ChatTeamModel(Query):
    def __init__(self):
        self.table_name = "senga_chat_team"
        super(ChatTeamModel, self).__init__()

    @gen.coroutine
    def get_team_by_id(self, team_id):
        ret = None
        cur = yield self.field("user_ids, team_leader").where("id=%s" % team_id).select()
        if cur.rowcount > 0:
            team = cur.fetchone()
            ret = dict(zip(["user_ids", "team_leader"], team))
        raise gen.Return(ret)


if __name__ == "__main__":
    pass
