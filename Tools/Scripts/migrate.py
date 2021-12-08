#!/usr/bin/env python3

import os
from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////{}'.format(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(app.instance_path))), 'instance', 'flaskr.sqlite'))).replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # noqa: A003
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    tasks = db.relationship('Task', back_populates='user', cascade='all, delete')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # noqa: A003
    user = db.relationship('User', back_populates='tasks')
    body = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
