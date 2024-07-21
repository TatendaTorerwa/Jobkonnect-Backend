import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db_operations import (
    register_user, login_user, get_user_by_id, get_all_users,
    get_all_jobs, create_job, get_job_by_id, get_jobs_by_employer_id,
    update_job, delete_job, create_application, get_applications,
    get_application_by_id, update_application_status, delete_application
)
from models.user import User
from models.job import Job
from models.application import Application

class TestDBOperations(unittest.TestCase):

    @patch('db_operations.SessionLocal')
    def test_register_user(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.commit.side_effect = None  # Simulate successful commit

        register_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            role='job_seeker',
            phone_number='1234567890',
            address='123 Test St',
            first_name='Test',
            last_name='User'
        )

        # Verify that the session's add and commit methods were called
        self.assertTrue(mock_session_instance.add.called)
        self.assertTrue(mock_session_instance.commit.called)

    @patch('db_operations.SessionLocal')
    def test_login_user(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_user = User(username='testuser', email='testuser@example.com')
        mock_user.check_password = MagicMock(return_value=True)
        mock_session_instance.query().filter_by().one.return_value = mock_user

        user = login_user(email='testuser@example.com', password='testpass')

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    @patch('db_operations.SessionLocal')
    def test_get_user_by_id(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_user = User(username='testuser', email='testuser@example.com')
        mock_session_instance.query().get.return_value = mock_user

        user = get_user_by_id(1)

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    @patch('db_operations.SessionLocal')
    def test_get_all_users(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_user1 = User(username='testuser1', email='testuser1@example.com')
        mock_user2 = User(username='testuser2', email='testuser2@example.com')
        mock_session_instance.query().all.return_value = [mock_user1, mock_user2]

        users = get_all_users()

        self.assertEqual(len(users), 2)

    @patch('db_operations.SessionLocal')
    def test_create_job(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        job_data = {
            'title': 'Test Job',
            'description': 'Job description',
            'requirements': 'Job requirements',
            'employer_id': 1,
            'salary': '50000',
            'location': 'Test Location',
            'job_type': 'Full-time',
            'application_deadline': '2023-07-20',
            'skills_required': 'Skills',
            'preferred_qualifications': 'Qualifications'
        }

        job_id = create_job(job_data)
        self.assertIsNotNone(job_id)
        self.assertTrue(mock_session_instance.add.called)
        self.assertTrue(mock_session_instance.commit.called)

    @patch('db_operations.SessionLocal')
    def test_get_job_by_id(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_job = Job(title='Test Job')
        mock_session_instance.query().get.return_value = mock_job

        job = get_job_by_id(1)

        self.assertIsNotNone(job)
        self.assertEqual(job['title'], 'Test Job')

    @patch('db_operations.SessionLocal')
    def test_get_jobs_by_employer_id(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_job1 = Job(title='Test Job 1')
        mock_job2 = Job(title='Test Job 2')
        mock_session_instance.query().filter_by().all.return_value = [mock_job1, mock_job2]

        jobs = get_jobs_by_employer_id(1)

        self.assertEqual(len(jobs), 2)

    @patch('db_operations.SessionLocal')
    def test_update_job(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_job = Job(title='Test Job')
        mock_session_instance.query().get.return_value = mock_job

        job_data = {
            'title': 'Updated Job',
            'description': 'Updated description',
            'requirements': 'Updated requirements',
            'salary': '60000',
            'location': 'Updated Location',
            'job_type': 'Part-time',
            'application_deadline': '2023-08-20',
            'skills_required': 'Updated skills',
            'preferred_qualifications': 'Updated qualifications'
        }

        result = update_job(1, job_data)
        self.assertTrue(result)
        self.assertEqual(mock_job.title, 'Updated Job')

    @patch('db_operations.SessionLocal')
    def test_delete_job(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_job = Job(title='Test Job')
        mock_session_instance.query().get.return_value = mock_job

        result = delete_job(1)
        self.assertTrue(result)
        self.assertTrue(mock_session_instance.delete.called)
        self.assertTrue(mock_session_instance.commit.called)

    @patch('db_operations.SessionLocal')
    def test_create_application(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        application_data = {
            'job_id': 1,
            'employer_id': 1,
            'user_id': 1,
            'years_of_experience': 5,
            'resume': 'Resume.pdf',
            'cover_letter': 'CoverLetter.pdf',
            'status': 'applied',
            'name': 'Test Applicant',
            'school_name': 'Test School',
            'portfolio': 'portfolio.com',
            'skills': 'Skills'
        }

        application = create_application(application_data)
        self.assertIsNotNone(application)
        self.assertTrue(mock_session_instance.add.called)
        self.assertTrue(mock_session_instance.commit.called)

    @patch('db_operations.SessionLocal')
    def test_get_applications(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_application1 = Application(status='applied')
        mock_application2 = Application(status='reviewed')
        mock_session_instance.query().filter_by().all.return_value = [mock_application1, mock_application2]

        applications = get_applications(1, 'job_seeker')
        self.assertEqual(len(applications), 2)

    @patch('db_operations.SessionLocal')
    def test_get_application_by_id(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_application = Application(status='applied')
        mock_session_instance.query().get.return_value = mock_application

        application = get_application_by_id(1)
        self.assertIsNotNone(application)
        self.assertEqual(application.status, 'applied')

    @patch('db_operations.SessionLocal')
    def test_update_application_status(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_application = Application(status='applied')
        mock_session_instance.query().get.return_value = mock_application

        data = {'status': 'reviewed'}
        application_dict = update_application_status(1, data)

        self.assertIsNotNone(application_dict)
        self.assertEqual(application_dict['status'], 'reviewed')

    @patch('db_operations.SessionLocal')
    def test_delete_application(self, mock_session):
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_application = Application(status='applied')
        mock_session_instance.query().get.return_value = mock_application

        result = delete_application(1)
        self.assertTrue(result)
        self.assertTrue(mock_session_instance.delete.called)
        self.assertTrue(mock_session_instance.commit.called)

if __name__ == '__main__':
    unittest.main()
