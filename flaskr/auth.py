#!/usr/bin/env python3

import jwt
import os
from cerberus import Validator
from datetime import datetime, timedelta
from dotenv.main import dotenv_values
from flask import Blueprint, jsonify
from flaskr.db import db, User, UserSchema
from flaskr.utils import parse_data
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')
v = Validator(purge_unknown=True, require_all=True)


@bp.route('/login', methods=['POST'])
@parse_data
def login(data, **kwargs):
    schema = {
        'username': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
        'password': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    user = User.query.filter_by(username=data['username']).first()

    if user is None:
        return jsonify({'error': {'username': ['username is incorrect']}}), 401
    elif not check_password_hash(user.password, data['password']):
        return jsonify({'error': {'password': ['password is incorrect.']}}), 401

    return jsonify({'token': jwt.encode({
        'user_id': user.id,
        'password': user.password,
        'exp': (datetime.now() + timedelta(days=30)).timestamp(),
    }, os.getenv('AUTH_SECRET', dotenv_values().get('AUTH_SECRET')), algorithm='HS256')})


@bp.route('/register', methods=['POST'])
@parse_data
def register(data, **kwargs):
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
        },
        'password': {
            'type': 'string',
            'coerce': str,
            'empty': False,
        },
    }

    if not v.validate(data, schema):
        return jsonify({'error': v.errors}), 400
    data = v.normalized(data, schema)

    if User.query.filter_by(username=data['username']).count() > 0:
        return jsonify({'error': {'username': ['username is taken']}}), 401

    new_user = User(name=data['name'], username=data['username'], password=generate_password_hash(data['password']))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(UserSchema().dump(new_user))
