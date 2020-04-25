#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 8:43 下午 
@name:message.py
消息定义
"""
import sys
import time
import uuid

import ujson


class MessageBox(object):
    def __init__(self, action="", comments="消息", mq_type="single"):
        self.action = action
        self.comments = comments
        self.mq_type = mq_type
        self.target_user_id = 0
        self.body = ""

    def add_message(self, msg):
        if self.mq_type == "single":
            self.target_user_id = msg.target_user.get("id", 0)
        self.body = ujson.dumps(msg, ensure_ascii=False)
        return self


class MessageContent():
    def __init__(self):
        self.title = ""
        self.desc = ""


class MessageObj(object):
    def __init__(self, **kwargs):
        self.msg_type = ""
        self.msg_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid1())).int & sys.maxint)
        self.from_user = {}
        self.target_user = {}
        self.content = MessageContent()
        self.create_time = int(time.time())
        self.tips = "支持的消息类型，请升级最新客户端！"
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_content(self, **kwargs):
        if kwargs and self.content is None:
            self.content = MessageContent()
        for k, v in kwargs.items():
            if k or v:
                setattr(self.content, k, v)
        return self

    def add_user(self, from_user=None, target_user=None):
        if from_user:
            self.from_user = from_user
        if target_user:
            self.target_user = target_user


class TextMsg(MessageObj):
    """
    文本消息
    """
    def __init__(self, **kwargs):
        super(TextMsg, self).__init__(**kwargs)
        self.msg_type = "text_msg"


if __name__ == "__main__":
    pass
