#!/usr/bin/env python3

import jwt
import pytest
from datetime import datetime
from flaskr.db import User
from tests.conftest import parse_data


@pytest.mark.parametrize(('username', 'password', 'status', 'error'), (
    ('', '', 400, 'Username is required.'),
    ('username', '', 400, 'Password is required.'),
    ('foobar', 'password', 401, 'Username is incorrect.'),
    ('username', 'foobar', 401, 'Password is incorrect.'),
    ('username', 'password', 200, '')
))
def test_validate_login_input(auth, username, password, status, error):
    response = auth.login(data={'username': username, 'password': password})
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', '') == error


@pytest.mark.parametrize(('name', 'username', 'password', 'status', 'error'), (
    ('', '', '', 400, 'Name is required.'),
    ('John Doe', '', '', 400, 'Username is required.'),
    ('John Doe', 'jdoe', '', 400, 'Password is required.'),
    ('John Doe', 'username', 'password', 401, 'Username is taken.'),
    ('John Doe', 'jdoe', 'password', 200, '')
))
def test_validate_register_input(auth, name, username, password, status, error):
    response = auth.register(data={'name': name, 'username': username, 'password': password})
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', '') == error


def test_register(auth):
    num_users = User.query.count()
    auth.register()

    assert User.query.count() > num_users
