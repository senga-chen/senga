#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:59 上午 
@name:rounting.py

"""
from handlers.chatHandler import ChatSocketHandler
from handlers.indexHandler import MainHandler
from handlers.messageHandler import MessageHandler
from handlers.userHandler import UserHandler, LoginHandler


def handler_store():
    handlers = [
        (r'/', MainHandler),
        (r'/chatsocket', ChatSocketHandler),
        (r'/api/message', MessageHandler),
        (r'/api/user/user_info', UserHandler),
        (r'/api/user/login', LoginHandler),
    ]
    return handlers


if __name__ == "__main__":
    pass