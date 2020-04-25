#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 11:44 上午 
@name:__init__.py.py

"""
import os


class BootOptions(object):

    def __init__(self, options):
        self.options = options
        self.mod_prefix = 'boot.'
        self.auto_boot()

    def auto_boot(self):
        current_path = os.path.dirname(__file__)
        for name in os.listdir(current_path):
            path = os.path.join(current_path, name)
            prefix, ext = name.split(".")
            if ext == 'py' and prefix != '__init__':
                boot_path = self.mod_prefix + prefix + '.' + prefix.capitalize() + 'Boot'
            else:
                continue
            boot = self._import_boot(boot_path)
            if boot:
                boot(self.options)

    def _import_boot(self, module2object):
        try:
            d = module2object.rfind(".")
            menu_func = module2object[d + 1: len(module2object)]
            m = __import__(module2object[0:d], globals(), locals(), [menu_func])
            return getattr(m, menu_func, None)
        except ImportError:
            return None


if __name__ == "__main__":
    pass