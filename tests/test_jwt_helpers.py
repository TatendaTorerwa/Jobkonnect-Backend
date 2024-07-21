import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import jwt
from datetime import datetime, timedelta
from flask import Flask, jsonify
from unittest.mock import patch
from jwtfunc import generate_token, token_required

class TestJWTFunctions(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        self.client = self.app.test_client()

        @self.app.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({
                'id': current_user['id'],
                'username': current_user['username'],
                'role': current_user['role']
            })

        self.user_id = 1
        self.username = 'testuser'
        self.role = 'job_seeker'
        self.expiration = (datetime.utcnow() + timedelta(hours=1)).replace(microsecond=0)
        self.token, _ = generate_token(self.user_id, self.username, self.role)

    def test_generate_token(self):
        token, exp = generate_token(self.user_id, self.username, self.role)
        self.assertIsInstance(token, str)

        # Compare datetime objects up to the second
        exp_datetime = datetime.fromisoformat(exp).replace(microsecond=0)
        self.assertEqual(exp_datetime, self.expiration)

        decoded = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        self.assertEqual(decoded['id'], self.user_id)
        self.assertEqual(decoded['username'], self.username)
        self.assertEqual(decoded['role'], self.role)

    def test_token_required_valid_token(self):
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.user_id)
        self.assertEqual(data['username'], self.username)
        self.assertEqual(data['role'], self.role)

    def test_token_required_missing_token(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Authorization header is missing!')

    def test_token_required_invalid_token_format(self):
        headers = {
            'Authorization': 'Bearer'
        }
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid token format!')

    def test_token_required_expired_token(self):
        expired_token = jwt.encode({
            'id': self.user_id,
            'username': self.username,
            'role': self.role,
            'exp': datetime.utcnow() - timedelta(hours=1)
        }, self.app.config['SECRET_KEY'], algorithm='HS256')

        headers = {
            'Authorization': f'Bearer {expired_token}'
        }
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Token has expired!')

    def test_token_required_invalid_token(self):
        headers = {
            'Authorization': 'Bearer invalidtoken'
        }
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid token!')

if __name__ == '__main__':
    unittest.main()
