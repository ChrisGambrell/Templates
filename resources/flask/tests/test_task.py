#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize(('access_username', 'message'), (
    ('username2', 'Access denied.'),
    ('username', '')
))
def test_get_task_by_id(auth, client, task, access_username, message):
    response = task.create_task(username='username')
    new_task = response.get_json() if response.get_json() is not None else {}
    
    auth_header = auth.get_auth_header(username=access_username)
    response = client.get(f'/task/{new_task.get("id", "")}', headers=auth_header)
    data = response.get_json() if response.get_json() is not None else {}

    assert message in data.get('error', '')


def test_get_tasks(auth, client):
    auth_header = auth.get_auth_header()
    response = client.get('/task/', headers=auth_header)
    data = response.get_json() if response.get_json() is not None else []
    assert type(data) is list


@pytest.mark.parametrize(('body', 'message'), (
    ('', 'Body is required.'),
    ('Test body', '')
))
def test_create_task_validate_input(task, body, message):
    response = task.create_task(body=body)
    data = response.get_json() if response.get_json() is not None else {}
    assert message in data.get('error', '')
