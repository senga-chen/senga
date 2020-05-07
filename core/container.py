#!/usr/bin/env python
# encoding: utf-8
"""
@Author:chen
@time: 10:57 下午 
@name:container.py

"""
import ujson


class ResponseParam:
    def __init__(self, code, msg):
        self.error_code = code
        self.error_msg = msg

    def add_attr(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def __str__(self):
        return ujson.dumps(self, ensure_ascii=False)


class RETURN():
    @classmethod
    def SUCCESS(cls):
        return ResponseParam(0, "success")

    @staticmethod
    def NOTOKEN():
        return ResponseParam(30001, "接口需要TOKEN")


class BusinessException(Warning):
    """
    业务异常
    """

    def __init__(self, msg="业务错误"):
        self.response_param = ResponseParam(30004, msg)

    @property
    def response(self):
        return self.response_param

    def add_attr(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self.response_param, k, v)
        return self

    def __str__(self):
        return self.response_param.error_msg

if __name__ == "__main__":
    pass