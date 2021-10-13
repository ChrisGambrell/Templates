#!/usr/bin/env python3

import functools
import jwt
from flask import jsonify, request
from flaskr.db import Task, User


def exists(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        if kwargs.get('task_id', None) is not None:
            task = Task.query.filter_by(id=kwargs.get('task_id', '')).first()

            if task is None:
                return jsonify({'error': 'Task does not exist.'}), 404
            return endpoint(fetched_task=task, **kwargs)
        elif kwargs.get('user_id', None) is not None:
            user = User.query.filter_by(id=kwargs.get('user_id', '')).first()

            if user is None:
                return jsonify({'error': 'User does not exist.'}), 404
            return endpoint(fetched_user=user, **kwargs)
        else:
            return endpoint(**kwargs)
    return wrapped_endpoint


def login_required(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        authorization = request.headers.get('Authorization', '')
        if len(authorization.split('Bearer ')) > 1:
            token = authorization.split('Bearer ')[1]
        else:
            return jsonify({'error': 'Missing token.'}), 400

        try:
            decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
            decoded_user = User.query.filter_by(id=decoded_token.get('user_id', '')).first()

            if decoded_user is None:
                return jsonify({'error': "User doesn't exist."}), 404
            elif decoded_user.password != decoded_token.get('password', ''):
                return jsonify({'error': 'Unauthorized.'}), 401

            return endpoint(authed_user=decoded_user, **kwargs)
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'error': 'Token expired.'}), 400
        except jwt.exceptions.DecodeError:
            return jsonify({'error': 'Invalid token.'}), 400
    return wrapped_endpoint


def owner(endpoint):
    @functools.wraps(endpoint)
    @login_required
    @exists
    def wrapped_endpoint(authed_user, fetched_task, **kwargs):
        if fetched_task.user_id != authed_user.id:
            return jsonify({'error': 'Access denied.'}), 401

        return endpoint(owned_task=fetched_task, **kwargs)
    return wrapped_endpoint


def parse_data(endpoint):
    @functools.wraps(endpoint)
    def wrapped_endpoint(**kwargs):
        data = request.get_json() if request.get_json() is not None else {}
        return endpoint(data=data, **kwargs)
    return wrapped_endpoint
