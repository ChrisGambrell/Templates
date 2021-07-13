#!/usr/bin/env python3

import os
import pytest
import tempfile
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='username', password='password'):
        return self._client.post('/auth/login', json={'username': username, 'password': password})

    def get_auth_header(self, username='username', password='password'):
        response = self.login(username, password)
        data = response.get_json() if response.get_json() is not None else {}
        return {'Authorization': f'Bearer {data.get("token", "")}'}


@pytest.fixture
def auth(client):
    return AuthActions(client)


class TaskActions(object):
    def __init__(self, auth, client):
        self._auth = auth
        self._client = client

    def create_task(self, body='Test body'):
        return self._client.post('/task/', json={'body': body}, headers=self._auth.get_auth_header())


@pytest.fixture
def task(auth, client):
    return TaskActions(auth, client)
