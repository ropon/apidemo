#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/13 14:16
# @Author  : Ropon
# @File    : response.py

from flask_restful import abort
from flask import jsonify

# 返回码说明
codeType = {
    4011: "参数不完整", 4012: "传递参数为空",
    4013: "站点名或数据库名不合法", 4014: "域名不合法",
    4015: "路径不合法", 4016: "域名已绑定",
    4017: "站点名或数据库名已存在", 4018: "记录不存在",
    4019: "未传入修改的值", 4020: "用户名不存在",
    4021: "密码错误，错误3次账号将锁定5分钟", 4022: "密码错误次数超过3次，账号已锁定",
    4023: "认证失败", 4024: "认证超时", 4025: "", 4026: "时间戳超过5分钟", 4027: "连接地址不合法"
}


class BaseResponse(object):
    def __init__(self):
        self.errcode = 0
        self.errmsg = "ok"
        self.data = None

    @property
    def dict(self):
        return self.__dict__


def api_abort(httpCode=400, errcode=None, message=None, key=""):
    res = BaseResponse()
    res.errcode = errcode or 4011
    if message:
        res.errmsg = message
        # 取具体错误信息
        if isinstance(message, dict):
            res.errmsg = str(list(message.values())[0])
    else:
        res.errmsg = key + codeType.get(res.errcode)
    res.dict.pop('data')
    if httpCode == 200:
        return jsonify(res.dict)
    return abort(httpCode, **res.dict)
