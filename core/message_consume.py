#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:08 上午 
@name:message_consume.py
消费者
"""
import logging
import uuid

import tornado.escape
import ujson

from core.message_client import CommonPikaProducer


class MessageConsume(object):
    _clients = None

    def __init__(self, queue_name, exchange_name, qos=30):
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.routing_key = "senga_app_1"
        self.qos = qos
        self.no_ack = False

    @property
    def pika_client(self):
        return self.get_client()

    @classmethod
    def get_client(cls):
        if cls._clients is None:
            _pick_client = CommonPikaProducer("message_consume_client")
            _pick_client.connect()
            cls._clients = _pick_client
        return cls._clients

    def init(self):
        self.pika_client.setup_queue(queue_name=self.queue_name, exchange_name=self.exchange_name,
                                     bind=True, routing_key=self.routing_key)
        self.pika_client.channel.basic_qos(prefetch_count=self.qos)
        self.consume_message()

    def consume_message(self):
        self.pika_client.channel.basic_consume(self.on_message, queue=self.queue_name, no_ack=self.no_ack)

    def on_message(self, channel, method, prop, body):
        pass


class ClientManage():
    @property
    def client_manager(self):
        return self._client_mgr

    @client_manager.setter
    def client_manager(self, client_manager):
        self._client_mgr = client_manager


client_manager = ClientManage()


class SingleConsume(MessageConsume):
    def on_message(self, channel, method, prop, body):
        try:
            message = ujson.loads(body)
            to_user_id = message.get("target_user_id", 0)
            to_user_id = 1
            client = client_manager.client_manager.get_current_client(to_user_id)
            msg = ujson.loads(message.get("body", ""))
            if client:
                client.write_socket_message(msg)
            else:
                # todo 用户不在线，消息处理
                pass
        except Exception, e:
            logging.error("single consume message error [%s]" % e.message)
        finally:
            if not self.no_ack:
                self.pika_client.channel.basic_ack(delivery_tag=method.delivery_tag)


class PikaConsumeExector(object):
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = PikaConsumeExector()
        return cls.__instance

    def init(self):
        # self.broadcast.init()
        self.single.init()

    def __init__(self):
        # self.broadcast = MessageConsume("senga_broadcast", "senga_broadcast_exchange")
        self.single = SingleConsume("senga_single", "senga_single_exchange")
        # self.broadcast.pika_client.do_init = self.init
        self.single.pika_client.do_init = self.init

    def __getattr__(self, item):
        if item == 'broadcast':
            return self.broadcast
        elif item == "single":
            return self.single
        else:
            return None


if __name__ == "__main__":
    pass
