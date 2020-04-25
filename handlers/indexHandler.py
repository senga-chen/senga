#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 9:54 下午 
@name:indexHandler.py

"""
from handlers import DefaultHandler


class MainHandler(DefaultHandler):
    def get(self):
        self.render("index.html", messages=[])


if __name__ == "__main__":
    pass