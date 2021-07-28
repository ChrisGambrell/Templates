#!/usr/bin/env python3

import functools
from flask import Blueprint, jsonify, request
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('task', __name__, url_prefix='/task')


def owner(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        db = get_db()
        task = db.execute('SELECT * FROM task WHERE id = ?', (kwargs.get('task_id', ''))).fetchone()

        if task is None:
            return jsonify({'error': 'Task does not exist.'})
        elif task['user_id'] != kwargs.get('user_id', ''):
            return jsonify({'error': 'Access denied.'})

        return endpoint(**kwargs)
    return wrapped_endpoint


@bp.route('/', methods=['GET'])
@login_required
def get_tasks(user_id, **kwargs):
    db = get_db()
    tasks = db.execute('SELECT * FROM task WHERE user_id = ? ORDER BY created_at', (user_id,)).fetchall()

    return jsonify([{key: task[key] for key in task.keys()} for task in tasks])


@bp.route('/', methods=['POST'])
@login_required
def create_task(user_id, **kwargs):
    data = request.get_json() if request.get_json() is not None else {}
    body = data.get('body', None)

    error = None

    if not body:
        error = 'Body is required.'

    if error:
        return jsonify({"error": error})

    db = get_db()
    db.execute('INSERT INTO task (user_id, body) VALUES (?, ?)', (user_id, body))
    db.commit()

    new_task = db.execute('SELECT * FROM task WHERE id = (SELECT max(id) FROM task)').fetchone()

    return jsonify({key: new_task[key] for key in new_task.keys()})


@bp.route('/<task_id>', methods=['PATCH'])
@login_required
@owner
def edit_task(task_id, **kwargs):
    data = request.get_json() if request.get_json() is not None else {}
    db = get_db()
    task = db.execute('SELECT * FROM task WHERE id = ?', (task_id)).fetchone()
    
    updated_task = {key: data.get(key, task[key]) for key in task.keys()}

    db.execute('UPDATE task SET body = ?, completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (updated_task['body'], updated_task['completed'], task_id))
    db.commit()

    updated_task = db.execute('SELECT * FROM task WHERE id = ?', (task_id)).fetchone()

    return jsonify({key: updated_task[key] for key in updated_task.keys()})
