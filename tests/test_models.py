import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from models.user import User
from models.job import Job
from models.application import Application

class ModelsTestCase(unittest.TestCase):


    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/test_db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()
        
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'role': 'job_seeker',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'address': '123 Test St'
        }

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    
    

    def test_user_creation(self):
        user = User(
            username='testuser',
            password='password',
            email='testuser@example.com',
            role='job_seeker',
            phone_number='1234567890'
        )
        user.set_password('password')
        self.session.add(user)
        self.session.commit()

        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('password'))

    def test_job_creation(self):
        employer = User(
            username='employer',
            password='password',
            email='employer@example.com',
            role='employer',
            phone_number='1234567890',
            company_name='Test Company',
            website='https://example.com'
        )
        employer.set_password('password')
        self.session.add(employer)
        self.session.commit()

        job = Job(
            title='Software Engineer',
            description='Develop software applications.',
            requirements='Experience in Python.',
            employer_id=employer.id,
            location='Remote',
            job_type='full-time',
            skills_required='Python, Flask'
        )
        self.session.add(job)
        self.session.commit()

        self.assertIsNotNone(job.id)
        self.assertEqual(job.employer_id, employer.id)

    def test_application_creation(self):
        user = User(
            username='jobseeker',
            password='password',
            email='jobseeker@example.com',
            role='job_seeker',
            phone_number='1234567890'
        )
        user.set_password('password')
        self.session.add(user)
        self.session.commit()

        employer = User(
            username='employer',
            password='password',
            email='employer@example.com',
            role='employer',
            phone_number='1234567890',
            company_name='Test Company',
            website='https://example.com'
        )
        employer.set_password('password')
        self.session.add(employer)
        self.session.commit()

        job = Job(
            title='Software Engineer',
            description='Develop software applications.',
            requirements='Experience in Python.',
            employer_id=employer.id,
            location='Remote',
            job_type='full-time',
            skills_required='Python, Flask'
        )
        self.session.add(job)
        self.session.commit()

        application = Application(
            job_id=job.id,
            employer_id=employer.id,
            user_id=user.id,
            resume='resume.pdf',
            cover_letter='cover_letter.pdf',
            status='submitted',
            name='John Doe',
            school_name='Test University',
            portfolio='https://portfolio.com',
            skills='Python, Flask',
            years_of_experience=3
        )
        self.session.add(application)
        self.session.commit()

        self.assertIsNotNone(application.id)
        self.assertEqual(application.job_id, job.id)
        self.assertEqual(application.user_id, user.id)
        self.assertEqual(application.employer_id, employer.id)

    def test_duplicate_email(self):
        user1 = User(
            username='user1',
            password='password',
            email='duplicate@example.com',
            role='job_seeker',
            phone_number='1234567890'
        )
        user1.set_password('password')
        self.session.add(user1)
        self.session.commit()

        user2 = User(
            username='user2',
            password='password',
            email='duplicate@example.com',
            role='job_seeker',
            phone_number='0987654321'
        )
        user2.set_password('password')
        self.session.add(user2)
        with self.assertRaises(Exception):
            self.session.commit()


if __name__ == '__main__':
    unittest.main()
