#!/usr/bin/env python3

import json
import sys
from flask import Blueprint, jsonify, request
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.route('/', methods=['GET'])
def get_tasks():
    db = get_db()
    tasks = db.execute('SELECT * FROM task ORDER BY created_at').fetchall()
    
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
