#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:44 下午 
@name:__init__.py.py

"""

__model = dict()
__service = dict()


def Service(key):
    return __service.get(key)


def Model(key):
    return __model.get(key)

if __name__ == "__main__":
    pass