#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.route('/<task_id>', methods=['GET'])
@login_required
def get_task_by_id(user_id, task_id):
    db = get_db()
    error = None
    task = db.execute('SELECT * FROM task WHERE id = ?', (task_id)).fetchone()

    if task['user_id'] != user_id:
        error = 'Access denied.'

    if error:
        return jsonify({'error': error})

    return jsonify({key: task[key] for key in task.keys()})


@bp.route('/', methods=['GET'])
@login_required
def get_tasks(user_id):
    db = get_db()
    tasks = db.execute('SELECT * FROM task WHERE user_id = ? ORDER BY created_at', (user_id,)).fetchall()

    return jsonify([{key: task[key] for key in task.keys()} for task in tasks])


@bp.route('/', methods=['POST'])
@login_required
def create_task(user_id):
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
