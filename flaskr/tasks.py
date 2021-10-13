#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from flaskr.db import db, Task, TaskSchema
from flaskr.utils import login_required, owner, parse_data

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/', methods=['GET'])
@login_required
def get_tasks(authed_user, **kwargs):
    tasks = Task.query.filter_by(user_id=authed_user.id)
    return jsonify(TaskSchema(many=True).dump(tasks))


@bp.route('/', methods=['POST'])
@login_required
@parse_data
def create_task(authed_user, data, **kwargs):
    body = data.get('body', None)

    error = None

    if not body:
        error = 'Body is required.'

    if error:
        return jsonify({"error": error}), 400

    new_task = Task(user=authed_user, body=body)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(TaskSchema().dump(new_task))


@bp.route('/<task_id>', methods=['PATCH'])
@login_required
@owner
@parse_data
def edit_task(owned_task, data, **kwargs):
    for key in data.keys():
        if key in ['body', 'completed']:
            if key == 'body' and data[key] == '':
                return jsonify({'error': 'Body is required.'}), 400
            elif key == 'completed' and type(data[key]) is not bool:
                return jsonify({'error': 'Completed must be a boolean.'}), 400
            setattr(owned_task, key, data[key])
        else:
            return jsonify({'error': f'{key} is not an editable property.'}), 400
    db.session.commit()

    return jsonify(TaskSchema().dump(owned_task))
