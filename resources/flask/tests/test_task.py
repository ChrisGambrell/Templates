#!/usr/bin/env python3

import pytest


@pytest.mark.parametrize(('use_task_id', 'access_username', 'message'), (
    (False, 'username', 'Task does not exist.'),
    (True, 'username2', 'Access denied.'),
    (True, 'username', '')
))
def test_get_task_by_id(auth, client, task, use_task_id, access_username, message):
    response = task.create_task(username='username')
    new_task = response.get_json() if response.get_json() is not None else {}
    
    auth_header = auth.get_auth_header(username=access_username)
    response = client.get(f'/task/{new_task.get("id", "") if use_task_id else "a"}', headers=auth_header)
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
