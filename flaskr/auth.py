#!/usr/bin/env python3

import jwt
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from flaskr.db import db, User, UserSchema
from flaskr.utils import parse_data
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
@parse_data
def login(data, **kwargs):
    username = data.get('username', None)
    password = data.get('password', None)

    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error:
        return jsonify({'error': error}), 400

    user = User.query.filter_by(username=username).first()

    if user is None:
        error = 'Username is incorrect.'
    elif not check_password_hash(user.password, password):
        error = 'Password is incorrect.'

    if error:
        return jsonify({'error': error}), 401

    return jsonify({'token': jwt.encode({
        'user_id': user.id,
        'password': user.password,
        'exp': (datetime.now() + timedelta(days=30)).timestamp()
    }, 'secret', algorithm='HS256')})


@bp.route('/register', methods=['POST'])
@parse_data
def register(data, **kwargs):
    name = data.get('name', None)
    username = data.get('username', None)
    password = data.get('password', None)

    error = None

    if not name:
        error = 'Name is required.'
    elif not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error:
        return jsonify({'error': error}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username is taken.'}), 401

    new_user = User(name=name, username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(UserSchema().dump(new_user))
