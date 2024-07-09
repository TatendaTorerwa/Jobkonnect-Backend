#!/usr/bin/env python3
"""
JWT helper functions.
"""
import os
import jwt
import datetime
from functools import wraps
from flask import Flask, request, jsonify, current_app

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

def generate_token(user_id, username, role):
    """
    Generates a JWT token for a given user.

    Args:
    - user_id (int): The ID of the user.
    - username (str): The username of the user.
    - role (str): The role of the user.

    Returns:
    - str: JWT token encoded with user information.

    Raises:
    - None

    This function encodes the user_id, username, and role into a JWT token
    using a secret key configured in the Flask application (`app.config['SECRET_KEY']`).
    """
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'id': user_id,
        'username': username,
        'role': role,
        'exp': expiration
    }

    secret_key = app.config['SECRET_KEY']  # Correctly reference the secret key
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return token, expiration.isoformat()


def token_required(f):
    """
    Decorator function to authenticate user based on JWT token.

    Args:
    - route_function (function): The route function to be decorated.

    Returns:
    - function: Decorated route function.

    Raises:
    - None

    This decorator function checks the 'Authorization' header in the request for a valid
    JWT token. If the token is valid, it extracts the user information and passes it to
    the decorated route function. If the token is invalid or missing, it returns a 401
    Unauthorized response.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])  # Correctly reference the secret key
            current_user = {
                'id': data['id'],
                'username': data['username'],
                'role': data['role']
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
