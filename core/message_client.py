#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 12:37 下午 
@name:message_client.py
消息生产者
"""
import pika
import ujson
from pika import TornadoConnection

from core.context import senga_app


class PikaProducerExector(object):
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = PikaProducerExector()
        return cls.__instance

    def init(self):
        self.broadcast.init()
        self.single.init()

    def __init__(self):
        self.broadcast = MessageProducer("senga_broadcast_exchange", "fanout", queue_name="senga_broadcast")
        self.single = MessageProducer("senga_single_exchange", "topic", queue_name="senga_single")
        self.broadcast.pika_client.do_init = self.init
        self.single.pika_client.do_init = self.init

    def __getattr__(self, item):
        if item == 'broadcast':
            return self.broadcast
        elif item == "single":
            return self.single
        else:
            return None


class CommonPikaProducer(object):
    def __init__(self, name=""):
        self._name = name
        rabbit_conf = senga_app.config.get("rabbitmq")
        cred = pika.PlainCredentials(rabbit_conf.get("username"), rabbit_conf.get("password"))
        self._conn_param = pika.ConnectionParameters(
            host=rabbit_conf.get("host"),
            port=rabbit_conf.get("port"),
            virtual_host="/",
            credentials=cred
        )
        self.conn = None
        self.channel = None
        self._conn_times = 0

    def connect(self):
        self.conn = TornadoConnection(self._conn_param, on_open_callback=self.on_connection_open,
                                      on_open_error_callback=self.on_open_error_callback,
                                      stop_ioloop_on_close=False)
        return self.conn

    def reconnect(self):
        self._conn_times += 1
        if self.conn.is_open:
            self._conn_times = 0
        else:
            self.connect()

    def on_connection_open(self, unused_connection):
        self._conn_times = 0
        self.conn.add_on_close_callback(self.on_connection_closed)
        self.conn.channel(on_open_callback=self.on_channel_open)

    def on_open_error_callback(self):
        self.conn.add_timeout(5, self.reconnect)

    def on_channel_open(self, channel):
        self.channel = channel
        self.do_init()
        self.add_on_channel_close_callback()

    def do_init(self):
        pass

    def add_on_channel_close_callback(self):
        self.channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        if self.conn.is_open:
            self.conn.close()

    def on_connection_closed(self):
        self.channel = None
        self.conn.add_timeout(5, self.reconnect)

    def setup_exchange(self, exchange_name, exchange_type):
        if self.channel is None:
            return
        self.channel.exchange_declare(self.exchange_declare_ok, exchange_name, exchange_type, durable=False)

    def exchange_declare_ok(self, unused_frame):
        pass

    def setup_queue(self, queue_name, x_expires=None, x_queue_mode=None, bind=False, exchange_name="", routing_key=None):
        if self.channel is None:
            return
        args = {}
        if x_expires:
            args.update({"x-expires": x_expires})
        if x_queue_mode:
            args.update({"x-queue-mode": x_queue_mode})
        self.channel.queue_declare(self.queue_declare_ok, queue=queue_name, arguments=args, durable=True)
        if bind:
            self.channel.queue_bind(self.on_queue_bindok, queue_name, exchange_name, routing_key=routing_key)

    def queue_declare_ok(self, unused_frame):
        pass

    def on_queue_bindok(self):
        pass

    def publish_message(self, quname, message, expiration=None, exchange="", routing_key=None):
        if self.channel is None:
            return
        properties = pika.BasicProperties(
            app_id="senga_app_send",
            content_type="application/json",
            headers="",
            delivery_mode=2,
            expiration=expiration
        )
        send_message = ujson.dumps(message, ensure_ascii=False, encode_html_chars=True)
        if not exchange or not routing_key:
            self.channel.basic_publish("", routing_key=quname, body=send_message, properties=properties)
        else:
            self.channel.basic_publish(exchange, routing_key=routing_key, body=send_message, properties=properties)


class MessageProducer(object):
    _clients = None

    def __init__(self, exchange_name, exchange_type, queue_name=None, routing_key=None, bind=False):
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.bind = bind

    @property
    def pika_client(self):
        return self.get_client()

    @classmethod
    def get_client(cls):
        if cls._clients is None:
            _pick_client = CommonPikaProducer("message_send_client")
            _pick_client.connect()
            cls._clients = _pick_client
        return cls._clients

    def init(self):
        self.pika_client.setup_exchange(self.exchange_name, self.exchange_type)
        self.pika_client.setup_queue(self.queue_name, bind=self.bind, exchange_name=self.exchange_name, routing_key=self.routing_key)

    def publish_message(self, message):
        if not self.pika_client.conn.is_open:
            return
        routing_key = self.get_routing_key()
        self._send(message, routing_key)

    def _send(self, message, routing_key):
        try:
            expiration = message.expiration
        except Exception, e:
            expiration = None
        self.pika_client.publish_message(self.queue_name, message, expiration=expiration, exchange=self.exchange_name, routing_key=routing_key)

    def get_routing_key(self):
        return ""


class MsgSendClient():
    @classmethod
    def send_message(cls, msg):
        exchange = getattr(PikaProducerExector.instance(), msg.mq_type)
        if not exchange:
            raise TypeError("找不到对应的exchange")
        try:
            exchange.publish_message(msg)
        except Exception, e:
            print "send message error %s" % e.message


if __name__ == "__main__":
    pass