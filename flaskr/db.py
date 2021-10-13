#!/usr/bin/env python3

import click
from datetime import datetime
from flask.cli import with_appcontext
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mb = Marshmallow()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', back_populates='user')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', back_populates='tasks')
    body = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class UserSchema(mb.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True


class TaskSchema(mb.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
        include_relationships = True


def init_data():
    # If any initial data is needed for the database,
    # do it here.
    # user = User(name='John Doe', username='jdoe', password='hashed_password')
    # task = Task(user=user, body='Sample task', completed=True)
    pass


def init_db():
    # Uncomment if you want the database to reset
    # each time the app is started
    # db.drop_all()

    try:
        db.create_all()
        db.init_data()
    except Exception:
        pass


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    db.init_app(app)
    mb.init_app(app)
    app.cli.add_command(init_db_command)
