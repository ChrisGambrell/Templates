#!/usr/bin/env python3

from cerberus import Validator
from flask import Blueprint, jsonify
from flaskr.db import db, Task, TaskSchema
from flaskr.utils import exists_task, login_required, owner, parse_data

bp = Blueprint('tasks', __name__, url_prefix='/tasks')
v = Validator(purge_unknown=True)


@bp.route('/', methods=['GET'])
@login_required
def get_tasks(authed_user, **kwargs):
    tasks = Task.query.filter_by(user_id=authed_user.id)
    return jsonify(TaskSchema(many=True).dump(tasks))


@bp.route('/', methods=['POST'])
@login_required
@parse_data
def create_task(authed_user, data, **kwargs):
    schema = {
        'body': {
            'type': 'string',
            'coerce': str,
            'empty': False,
            'required': True,
        },
        'completed': {
            'type': 'boolean',
            'coerce': bool,
            'empty': False,
            'default': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    new_task = Task(user=authed_user, body=data['body'], completed=data['completed'])
    db.session.add(new_task)
    db.session.commit()

    return jsonify(TaskSchema().dump(new_task))


@bp.route('/<task_id>', methods=['GET'])
@login_required
@exists_task
def get_task_by_id(fetched_task, **kwargs):
    return jsonify(TaskSchema().dump(fetched_task))


@bp.route('/<task_id>', methods=['PATCH'])
@owner
@parse_data
def edit_task(owned_task, data, **kwargs):
    schema = {
        'body': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'completed': {
            'type': 'boolean',
            'coerce': bool,
            'empty': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    for key in data.keys():
        setattr(owned_task, key, data[key])
    db.session.commit()

    return jsonify(TaskSchema().dump(owned_task))


@bp.route('/<task_id>', methods=['DELETE'])
@owner
def delete_task(owned_task, **kwargs):
    db.session.delete(owned_task)
    db.session.commit()
    return jsonify({})
