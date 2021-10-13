#!/usr/bin/env python3

import jwt
import pytest
from datetime import datetime, timedelta
from flaskr import create_app
from tests.conftest import parse_data


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'hello, world!'


@pytest.mark.parametrize(('token', 'status', 'error'), (
    (jwt.encode({'user_id': 1, 'password': 'pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', 'exp': (datetime.now() + timedelta(days=1)).timestamp()}, 'secret', algorithm='HS256'), 400, 'Missing token.'),
    ('Bearer ' + jwt.encode({'user_id': 1, 'password': 'pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', 'exp': (datetime.now() - timedelta(days=1)).timestamp()}, 'secret', algorithm='HS256'), 400, 'Token expired.'),
    ('Bearer ' + jwt.encode({'user_id': 1, 'password': 'pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', 'exp': (datetime.now() + timedelta(days=1)).timestamp()}, 'bad_secret', algorithm='HS256'), 400, 'Invalid token.'),
    ('Bearer ' + jwt.encode({'user_id': 0, 'password': 'pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', 'exp': (datetime.now() + timedelta(days=1)).timestamp()}, 'secret', algorithm='HS256'), 404, "User doesn't exist."),
    ('Bearer ' + jwt.encode({'user_id': 1, 'password': 'password', 'exp': (datetime.now() + timedelta(days=1)).timestamp()}, 'secret', algorithm='HS256'), 401, 'Unauthorized.'),
    ('Bearer ' + jwt.encode({'user_id': 1, 'password': 'pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155', 'exp': (datetime.now() + timedelta(days=1)).timestamp()}, 'secret', algorithm='HS256'), 200, '')
))
def test_validate_token(client, token, status, error):
    response = client.get('/secret', headers={'Authorization': token})
    data = parse_data(response)

    assert status == response.status_code
    assert error == data.get('error', '')
