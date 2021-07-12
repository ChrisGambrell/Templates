#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize(('name', 'username', 'password', 'message'), (
    ('', '', '', 'Name is required.'),
    ('user', '', '', 'Username is required.'),
    ('user', 'username', '', 'Password is required.'),
    ('user', 'username', 'password', 'is taken.'),
    ('user', 'username2', 'password', '')
))
def test_register_validate_input(client, name, username, password, message):
    response = client.post('/auth/register', json={'name': name, 'username': username, 'password': password})
    data = response.get_json() if response.get_json() is not None else {}
    assert message in data.get('error', '')
