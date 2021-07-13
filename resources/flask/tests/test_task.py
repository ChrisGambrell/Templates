#!/usr/bin/env python3

import pytest


def test_get_tasks(auth, client):
    auth_header = auth.get_auth_header()
    response = client.get('/task/', headers=auth_header)
    data = response.get_json() if response.get_json() is not None else {}
    assert type(data) is list


@pytest.mark.parametrize(('body', 'message'), (
    ('', 'Body is required.'),
    ('Test body', '')
))
def test_create_task_validate_input(task, body, message):
    response = task.create_task(body)
    data = response.get_json() if response.get_json() is not None else {}
    assert message in data.get('error', '')
