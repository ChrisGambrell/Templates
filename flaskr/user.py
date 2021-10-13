#!/usr/bin/env python3

from cerberus import Validator
from flask import Blueprint, jsonify
from flaskr.db import db, User, UserSchema
from flaskr.utils import exists, login_required, parse_data

bp = Blueprint('user', __name__, url_prefix='/user')
v = Validator(purge_unknown=True)


@bp.route('/', methods=['GET'])
@login_required
def get_user(authed_user, **kwargs):
    return jsonify(UserSchema().dump(authed_user))


@bp.route('/', methods=['PATCH'])
@login_required
@parse_data
def edit_user(authed_user, data, **kwargs):
    schema = {
        'name': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'username': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        }
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    for key in data.keys():
        if key == 'username' and User.query.filter_by(username=data[key]).count() > 0:
            return jsonify({'error': {'username': ['username is taken']}}), 401
        setattr(authed_user, key, data[key])
    db.session.commit()

    return jsonify(UserSchema().dump(authed_user))


@bp.route('/', methods=['DELETE'])
@login_required
def delete_user(authed_user, **kwargs):
    db.session.delete(authed_user)
    db.session.commit()
    return jsonify({})


@bp.route('/<user_id>', methods=['GET'])
@login_required
@exists
def get_user_by_id(fetched_user, **kwargs):
    return jsonify(UserSchema().dump(fetched_user))
