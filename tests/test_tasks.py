#!/usr/bin/env python3

import pytest
from flaskr.db import Task
from tests.conftest import parse_data


def test_get_tasks(task):
    response = task.get()
    data = parse_data(response)

    assert type(data) is list
    assert len(data) > 0


@pytest.mark.parametrize(('data', 'status', 'error'), (
    ({'body': '', 'completed': 'foobar'}, 400, {'body': ['empty values not allowed']}),
    ({'body': 'Test task'}, 200, {})
))
def test_validate_create_task_input(task, data, status, error):
    response = task.create(data=data)
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', {}) == error


def test_create_task(task):
    num_tasks = Task.query.filter_by(user_id=1).count()
    task.create()

    assert Task.query.filter_by(user_id=1).count() > num_tasks


@pytest.mark.parametrize(('data', 'status', 'error'), (
    ({'body': '', 'completed': 'foobar'}, 400, {'body': ['empty values not allowed']}),
    ({'body': 'Editing task', 'completed': True}, 200, {})
))
def test_validate_edit_task_input(task, data, status, error):
    response = task.edit(data=data)
    data = parse_data(response)

    assert response.status_code == status
    assert data.get('error', {}) == error


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
