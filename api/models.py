#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 15:24
# @Author  : Ropon
# @File    : models.py

import datetime
from ext import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"useexisting": True}
    nid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    password = db.Column(db.String(256))
    status = db.Column(db.Boolean, default=0)
    errtimes = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.now)

    @classmethod
    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def add(self):
        db.session.add(self)
        return session_commit()

    @classmethod
    def update(cls, nid, update_dict):
        cls.query.filter_by(nid=nid).update(update_dict)
        return session_commit()

    @classmethod
    def get(cls, nid):
        return cls.query.filter_by(nid=nid).first()

    @classmethod
    def updateplus(cls, nid):
        cls.query.filter_by(nid=nid).update({cls.errtimes: cls.errtimes + 1},
                                            synchronize_session="evaluate")
        return session_commit()


class Token(db.Model):
    __tablename__ = "token"
    __table_args__ = {"useexisting": True}
    nid = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256))
    created = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.nid"))
    token2user = db.relationship("User", backref="user2token", uselist=False)

    def add(self):
        db.session.add(self)
        return session_commit()

    @classmethod
    def uupdate(cls, user_id, update_dict):
        cls.query.filter_by(user_id=user_id).update(update_dict)
        return session_commit()

    @classmethod
    def uget(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()


def session_commit():
    try:
        db.session.commit()
    except db.SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        print(reason)
        return reason
