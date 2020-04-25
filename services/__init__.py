#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 9:50 下午 
@name:__init__.py.py

"""
import logging

from core.context import senga_app


class BaseService(object):
    LOG = logging
    content = senga_app

    def info(self, msg, *args, **kwargs):
        self.LOG.info("[%s] %s" % (self._name(), msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.LOG.error("[%s] %s" % (self._name(), msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.LOG.debug("[%s] %s" % (self._name(), msg), *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.LOG.exception("[%s] %s" % (self._name(), msg), *args, **kwargs)

    def _name(self):
        if hasattr(self, "name"):
            return self.name
        else:
            return self.__class__.__name__


if __name__ == "__main__":
    pass