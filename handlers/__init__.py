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

from core.container import RETURN
from core.context import senga_app


class DefaultHandler(tornado.web.RequestHandler):
    Log = logging

    def write_json(self, ret, expire=0):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        if expire:
            self.set_header('Cache-Control', 'max-age=%s, must-revalidate' % (expire,))
        if not isinstance(ret, basestring):
            ret = ujson.dumps(ret, escape_forward_slashes=False, encode_html_chars=False, ensure_ascii=False)
        self.write(ret)
        self.finish()

    def input(self, schema, need_token=True):
        ret = {}
        args = self.request.arguments
        DefaultHandler.Log.info("%s %s %s" % (
            self.request.method, self.request.path, ujson.dumps(args, ensure_ascii=False).replace(" ", '_')))
        if len(args):
            for r in args:
                ret[r] = self.get_argument(r).encode('utf-8')
        if need_token and (ret.get("token", None) is None or len(ret.get("token", "")) == 0):
            self.write_json(RETURN.NOTOKEN())
            return None
        validated = schema.validate(ret)
        if validated.has_key("token"):
            # check user
            operator_id = senga_app.redis.get("token:%s" % validated["token"])
            if operator_id:
                validated["operator_id"] = int(operator_id)
        return validated


if __name__ == "__main__":
    pass