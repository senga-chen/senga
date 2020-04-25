#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 11:33 上午 
@name:cmd.py

"""
import os
import sys

import options
from boot import BootOptions
from common._config import ConfigFactory


class Null(object):
    pass


_Null = Null()


class Cmd(object):

    def __init__(self, opt=None):

        self.options = opt or options

    def get_file_opt(self):
        opt = options.Options(None)
        opt.define('-c', '--config', default='./conf/setting_dev.conf',
                   help="config path (default %(default)r)", metavar="FILE")
        o = opt.parse_args(sys.argv)
        if os.path.exists(o.config):
            config = ConfigFactory.parseFile(o.config, pystyle=True)
            return config
        else:
            return ConfigFactory.empty(pystyle=True)

    def parse_cmd(self, help_doc):
        self.options.setup_options(help_doc)
        BootOptions(self.options)

        c = self._set_defaults()
        opt = self.options.parse_args()
        config = c.toSelectConfig()
        config.update(vars(opt))
        return config

    def _set_defaults(self):
        c = self.get_file_opt()
        opt = options.Options(None)
        BootOptions(opt)
        opt = opt.parse_args()
        d = {}
        config = vars(opt)
        for k in config:
            v = c.get(k, _Null)
            if v != _Null:
                d[k] = v
        self.options.set_defaults(**d)
        return c


__cmd = Cmd()


def parse_cmd(help_doc):
    return __cmd.parse_cmd(help_doc)


if __name__ == "__main__":
    pass