#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:47 下午 
@name:autoload.py

"""
import logging
import os

import core


class Autoload():
    def __init__(self, context):
        self.context = context
        self.models = {}
        self.services = {}

    def autoload(self):
        self.mount_models()
        self.mount_service()

    def mount_models(self):
        self._import("models", "__model")

    def mount_service(self):
        self._import("services", "__service")

    def _import(self, path, core_lib_name):
        current_path = os.path.dirname(__file__)
        current_path = os.path.abspath(os.path.join(current_path, os.path.pardir))
        module_path = os.path.join(current_path, path)
        models = filter(lambda x: str(x).endswith(".py"), os.listdir(module_path))
        for name in models:
            model_path = "%s.%s" % (path, ''.join(name.split(".")[:1]))
            try:
                m = __import__(model_path, globals(), locals(), ['__all__'])
                names = getattr(m, "__all__", [])
                for model_name in names:
                    model = getattr(m, model_name, None)
                    if model:
                        self.models[model_name] = model()
                        logging.info("load mode %s.%s" % (model_path, model_name))
            except Exception, e:
                pass
        setattr(core, core_lib_name, self.models)


if __name__ == "__main__":
    pass