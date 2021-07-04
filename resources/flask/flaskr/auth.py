#!/usr/bin/env python3

from flask import Blueprint, jsonify, request
from flaskr.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET'))
def login():
    data = request.get_json() if request.get_json() is not None else {}
    username = data.get('username', None)
    password = data.get('password', None)

    db = get_db()
    error = None
    user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

    if user is None:
        error = 'Invalid username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is not None:
        return jsonify({error: error})

    return jsonify(user)


@bp.route('/register', methods=('POST'))
def register():
    data = request.get_json() if request.get_json() is not None else {}
    username = data.get('username', None)
    password = data.get('password', None)

    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
        error = f'The username {username} is already taken.'

    if error is not None:
        return jsonify({error: error})

    db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
    db.commit()
    
    return jsonify({})
