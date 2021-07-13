#!/usr/bin/env python3

import pytest


def test_get_task_by_id(client):
    response = client.get('/task/1')
    data = response.get_json() if response.get_json() is not None else {}
    assert type(data) is dict


def test_get_tasks(client):
    response = client.get('/task/')
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
