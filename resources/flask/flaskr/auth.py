#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from flaskr.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() if request.get_json() is not None else {}
    username = data.get('username', None)
    password = data.get('password', None)

    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error:
        return jsonify({'error': error})

    db = get_db()
    user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
    user_data = {key: user[key] for key in user.keys()} if user is not None else None

    if user_data is None:
        error = 'Username is incorrect.'
    elif not check_password_hash(user_data.get('password', ''), password):
        error = 'Password is incorrect.'

    if error:
        return jsonify({'error': error})

    return jsonify(user_data)


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() if request.get_json() is not None else {}
    name = data.get('name', None)
    username = data.get('username', None)
    password = data.get('password', None)

    db = get_db()
    error = None

    if not name:
        error = 'Name is required.'
    elif not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
        error = f'Username {username} is taken.'

    if error:
        return jsonify({"error": error})

    db.execute('INSERT INTO user (name, username, password) VALUES (?, ?, ?)', (name, username, generate_password_hash(password)))
    db.commit()
    return jsonify({})
