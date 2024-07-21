import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import json
from endpoints import *

class FlaskTestCase(unittest.TestCase):
    """Test case for the Flask application."""

    @classmethod
    def setUpClass(cls):
        """Set up the Flask application for testing."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.client = app.test_client()

    def test_register_user(self):
        """Test user registration endpoint."""
        response = self.client.post('/api/user/register', json={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'testuser@example.com',
            'role': 'job_seeker',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

    def test_login_user(self):
        """Test user login endpoint."""
        self.client.post('/api/user/register', json={
            'username': 'testuser',
            'password': 'testpass',
            'email': 'testuser@example.com',
            'role': 'job_seeker',
            'phone_number': '1234567890'
        })
        response = self.client.post('/api/user/login', json={
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'token', response.data)

    def test_create_job(self):
        """Test creating a new job listing."""
        response = self.client.post('/api/jobs', json={
            'title': 'Software Engineer',
            'description': 'A software engineer job',
            'employer_id': 1  # Assuming this is a valid employer ID
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Software Engineer', response.data)

    def test_apply_to_job(self):
        """Test applying to a job."""
        # First, create a job listing
        job_response = self.client.post('/api/jobs', json={
            'title': 'Software Engineer',
            'description': 'A software engineer job',
            'employer_id': 1
        })
        job_id = json.loads(job_response.data)['id']

        # Then, apply to the job
        login_response = self.client.post('/api/user/login', json={
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        token = json.loads(login_response.data)['token']

        response = self.client.post(f'/api/jobs/{job_id}/apply', headers={
            'Authorization': f'Bearer {token}'
        }, data={
            'years_of_experience': '5',
            'status': 'submitted',
            'name': 'Test Applicant',
            'school_name': 'Test University',
            'portfolio': 'http://portfolio.com',
            'skills': 'Python, Flask',
            'resume': (open('test_resume.pdf', 'rb'), 'resume.pdf'),
            'cover_letter': (open('test_cover_letter.pdf', 'rb'), 'cover_letter.pdf')
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'resume', response.data)
        self.assertIn(b'cover_letter', response.data)

if __name__ == '__main__':
    unittest.main()
