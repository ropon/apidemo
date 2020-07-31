#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 15:25
# @Author  : Ropon
# @File    : manager.py

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ext import db
from api import create_app, models

# 迁移时模型必须导入

app = create_app()

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
