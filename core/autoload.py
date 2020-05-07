#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:47 下午 
@name:autoload.py

"""
import logging
import os
import re

import core


class AutoLoader():

    REG = re.compile(r"(\w[\w\d_]+)\s*\-\s*>\s*(\w[\w\d_]+)")

    def __init__(self, content, mod_prefix=None):
        self.content = content
        self.models = {}
        self.services = {}
        self.mod_prefix = mod_prefix or 'models.'
        self.service_prefix = mod_prefix or 'services.'

    def autoload(self):
        self.mount_model()
        self.mount_service()

    def mount_model(self):
        self.__import("models", "__model")

    def mount_service(self):
        self.__import("services", "__service")

    def __import(self, path, core_lib_name, args=None):
        current_path = os.path.dirname(__file__)
        current_path = os.path.abspath(os.path.join(current_path, os.path.pardir))
        module_path = os.path.join(current_path, path)
        models = filter(lambda x: str(x).endswith(".py"), os.listdir(module_path))
        for name in models:
            model_path = "%s.%s" % (path, ''.join(name.split(".")[:1]))
            try:
                m = __import__(model_path, globals(), locals(), ['__all__'])
                names = getattr(m, '__all__', [])
                for model_name in names:
                    model = getattr(m, model_name, None)
                    if model:
                        if args:
                            self.models[model_name] = model(args)
                        else:
                            self.models[model_name] = model()
                        logging.info("load model %s.%s" % (model_path,model_name))
            except Exception as e:
                logging.error("In module %s : %s", model_path, e)
                continue
        setattr(core, core_lib_name, self.models)


if __name__ == "__main__":
    pass