#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:16 下午 
@name:message_service.py

"""
from tornado import gen

from core.context import senga_app
from core.message_client import MsgSendClient
from models.message import TextMsg, MessageBox
from services import BaseService

__all__ = ["MessageService"]


class MessageService(BaseService):
    @gen.coroutine
    def single_message(self, from_id, target_id, message):
        msg_body = TextMsg()
        from_user = yield senga_app.service("UserService").userinfo(from_id)
        target_user = yield self.content.service("UserService").userinfo(target_id)
        msg_body.add_user(from_user=from_user, target_user=target_user)
        msg_body.add_content(desc=message)
        msg = MessageBox(action="single_msg").add_message(msg_body)
        MsgSendClient.send_message(msg)


if __name__ == "__main__":
    pass
