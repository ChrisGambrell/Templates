#!/usr/bin/env python3

import pytest
from flaskr.db import Task
from tests.conftest import parse_data


def test_get_tasks(task):
    response = task.get()
    data = parse_data(response)

    assert type(data) is list
    assert len(data) > 0


@pytest.mark.parametrize(('body', 'status', 'error'), (
    ('', 400, 'Body is required.'),
    ('Test task', 200, '')
))
def test_validate_create_task_input(task, body, status, error):
    response = task.create(data={'body': body})
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', '') == error


def test_create_task(task):
    num_tasks = Task.query.count()
    task.create()

    assert Task.query.count() > num_tasks


@pytest.mark.parametrize(('data', 'status', 'error'), (
    ({'body': '', 'completed': True}, 400, 'Body is required.',),
    ({'body': 'Editing task', 'completed': 'True'}, 400, 'Completed must be a boolean.',),
    ({'foo': 'bar'}, 400, 'foo is not an editable property.'),
    ({'body': 'Editing task', 'completed': True}, 200, '')
))
def test_validate_edit_task_input(task, data, status, error):
    response = task.edit(data=data)
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', '') == error


def test_edit_task(task):
    response = task.create()
    new_task = parse_data(response)

    response = task.edit(data={'body': 'Updating the body!', 'completed': True})
    data = parse_data(response)

    for key in ['body', 'completed']:
        assert data[key] != new_task[key]


@pytest.mark.parametrize(('task_id', 'access_user', 'status', 'error'), (
    (-1, {'username': 'username', 'password': 'password'}, 404, 'Task does not exist.'),
    (None, {'username': 'username2', 'password': 'password'}, 401, 'Access denied.'),
    (None, {'username': 'username', 'password': 'password'}, 200, '')
))
def test_task_ownership(task, task_id, access_user, status, error):
    response = task.create()
    new_task = parse_data(response)

    response = task.edit(task_id=(task_id if task_id is not None else new_task['id']), data={'body': 'Attempting to update the body'}, user=access_user)
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', '') == error
