#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 9:35 下午
@name:__init__.py.py

"""
import logging

import tornado.web
import ujson


class DefaultHandler(tornado.web.RequestHandler):
    Log = logging

    def write_json(self, ret, expire=0):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        if expire:
            self.set_header('Cache-Control', 'max-age=%s, must-revalidate' % (expire,))
        self.write(ret)
        self.finish()

    def input(self, schema):
        ret = {}
        args = self.request.arguments
        DefaultHandler.Log.info("%s %s %s" % (
            self.request.method, self.request.path, ujson.dumps(args, ensure_ascii=False).replace(" ", '_')))
        if len(args):
            for r in args:
                ret[r] = self.get_argument(r).encode('utf-8')
        validated = schema.validate(ret)
        return validated


if __name__ == "__main__":
    pass