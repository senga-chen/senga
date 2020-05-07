#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 11:59 上午 
@name:socket_client_manage.py
socket连接管理
"""
import time

from tornado.websocket import WebSocketClosedError


class SocketClientStore(object):
    def __init__(self):
        self.clients = dict()

    def add_client(self, client):
        if self.clients.get(client.uid, None):
            self.clients.get(client.uid).close_socket()
        self.clients[client.uid] = client

    def remove_client(self, client_user):
        if self.clients.get(client_user.uid, None):
            self.clients.get(client_user.uid).close_socket()

    def get_client_by_uid(self, uid):
        client = self.clients.get(uid, None)
        return client

    def get_all_clients(self):
        clients = []
        clients.extend(self.clients)
        return clients


class SocketClientManager(object):
    def __init__(self, app):
        self.app = app
        self.client_store = SocketClientStore()

    @property
    def all_clients(self):
        return self.client_store.get_all_clients()

    def register_client(self, client):
        self.client_store.add_client(client)

    def get_all_clients(self):
        return self.all_clients

    def get_current_client(self, uid):
        return self.client_store.get_client_by_uid(uid)


class WebSocketUser(object):
    def __init__(self, uid, **kwargs):
        self.uid = uid
        self.last_active_time = time.time()
        self.last_notify_time = 0
        self.socket_client = None

    def set_user_client(self, socket_client):
        self.socket_client = socket_client

    def close_socket(self, code=None, reason=None):
        if self.socket_client:
            self.socket_client.close(code=code, reason=reason)

    def write_socket_message(self, message):
        if self.socket_client:
            self.socket_client.write_message(message)
        else:
            raise WebSocketClosedError()

    def ping_active(self):
        self.last_active_time = time.time()


if __name__ == "__main__":
    pass