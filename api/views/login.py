#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/28 13:42
# @Author  : Ropon
# @File    : login.py

from flask import Blueprint, views, jsonify, request
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with, output_json

from api.models import User, Token
from api.utils.response import api_abort

login_bp = Blueprint("login_bp", __name__, url_prefix="/api/v1")
api = Api(login_bp)

# api.representations = {'application/json;charset=utf-8': output_json}

parser = reqparse.RequestParser()
parser.add_argument("username", type=inputs.regex(r"^[a-z][a-z0-9]{3,5}$"), required=True, help="请输入4~8位字母数字用户名",
                    location=["form"])
parser.add_argument("password", type=inputs.regex(r"^[a-z][a-z0-9]{5,7}$"), required=True, help="请输入6~8位字母密码",
                    location=["form"])


class UserStatus(fields.Raw):
    def format(self, value):
        return "正常" if value else "禁用"


class DiyTDate(fields.Raw):
    def format(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")


user_fields = {
    "id": fields.Integer(attribute="nid"),
    'name': fields.String(attribute="username"),
    'status': UserStatus(attribute="status"),
    'errors': fields.Integer(attribute="errtimes"),
    # 'creattime':fields.DateTime(dt_format="iso8601",default="未获取到注册时间",attribute='created')
    'creattime': DiyTDate(attribute='created')
}


class LoginView(Resource):
    @marshal_with(user_fields)
    def get(self):
        print(request.headers)
        users = User.query.all()
        # print(users)
        return users
        # return {"code": 0, "msg": "中文测试"}

    def post(self):
        args = parser.parse_args()
        username = args.get("username")
        api_abort(errcode=4025, message=username)


api.add_resource(LoginView, "/login")

# flask 原生
# class LoginView(views.MethodView):
#     def get(self):
#         return {"code": 0, "msg": "中文测试"}
#
# login_bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
