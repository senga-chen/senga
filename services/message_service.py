#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:16 下午 
@name:message_service.py

"""
from tornado import gen

from services import BaseService

__all__ = ["MessageService"]


class MessageService(BaseService):
    @gen.coroutine
    def send_message(self, message):
        pass


if __name__ == "__main__":
    pass
