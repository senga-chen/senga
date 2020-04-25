#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 9:56 下午 
@name:chatHandler.py

"""
import logging

import tornado.escape
import tornado.websocket
import uuid


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def open(self, *args, **kwargs):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, chat):
        logging.info("send message ===> %s" % chat)
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except Exception, e:
                logging.error("error send message")

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    def on_message(self, message):
        logging.info("get message ==> %s" % message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed.get("body")
        }
        chat["html"] = tornado.escape.to_basestring(self.render_string("message.html", message=chat))
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)


if __name__ == "__main__":
    pass