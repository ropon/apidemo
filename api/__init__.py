#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 15:23
# @Author  : Ropon
# @File    : __init__.py

import re
import flask_restful
from flask import Flask, request
from api.utils.response import api_abort
from api.utils.config import WHITE_URL_LIST
from ext import db
from .utils.auth import verify_token
from .views.login import login_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object("api.config.DevConfig")

    @app.before_request
    def before_request():
        # 白名单
        for white_url in WHITE_URL_LIST:
            if re.match(white_url, request.path):
                return None

        auth = verify_token()
        if auth.get("userinfo") and auth.get("token"):
            return None
        else:
            return api_abort(httpCode=200, **auth)

    @app.after_request
    def after_request(response):
        # 允许跨域
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'POST, DELETE, PUT, GET'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    db.init_app(app)
    flask_restful.abort = api_abort

    app.register_blueprint(login_bp)

    return app
