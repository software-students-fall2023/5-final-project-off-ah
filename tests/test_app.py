import unittest
from bson.objectid import ObjectId
from unittest.mock import patch
from flask import template_rendered  # Import to capture template renderings
from contextlib import contextmanager
import sys
import os
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_dir, 'webapp'))
from app import app as flask_app
from auth import auth, User
from werkzeug.security import generate_password_hash
from unittest.mock import patch, MagicMock
from flask_login import current_user

@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

class FlaskAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.test_client()
        flask_app.config['TESTING'] = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        # flask_app.register_blueprint(auth)

    def test_register_page_loads(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    @patch('app.db.users.find_one')
    @patch('app.db.users.insert_one')
    def test_successful_registration(self, mock_insert_one, mock_find_one):
        mock_find_one.return_value = None
        response = self.app.post('/auth/register', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertIn(b'Login', response.data)
        mock_insert_one.assert_called_once()

    @patch('app.db.users.find_one')
    def test_registration_with_existing_username(self, mock_find_one):
        mock_find_one.return_value = {
            '_id': ObjectId(),
            'username': 'existinguser',
            'email': 'existinguser@example.com',
            'password_hash': generate_password_hash('password')
        }
        response = self.app.post('/register', data=dict(
            username='existinguser',
            email='existinguser@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'Username already exists', response.data)

    @patch('app.db.users.find_one')
    def test_successful_login(self, mock_find_one):
        # Correct use of ObjectId
        mock_find_one.return_value = {
            '_id': ObjectId(),
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': generate_password_hash('password')
        }
        with flask_app.test_request_context(), captured_templates(flask_app) as templates:
            response = self.app.post('/login', data={
                'username': 'testuser',
                'password': 'password'
            }, follow_redirects=True)
            # Check if a template was rendered (if your login redirects to a page that renders a template)
            self.assertEqual(len(templates), 1)
            self.assertTrue(current_user.is_authenticated)
            template, context = templates[0]
            self.assertIn('home', template.name)

    @patch('app.db.users.find_one')
    def test_unsuccessful_login(self, mock_find_one):
        # Simulate a user that does not exist in the database
        mock_find_one.return_value = None
        with flask_app.test_request_context():
            response = self.app.post('/login', data={
                'username': 'testuser',
                'password': 'wrongpassword'
            }, follow_redirects=True)
            # Check if the flash message 'Invalid credentials' was flashed
            self.assertIn(b'Invalid credentials', response.data)
            # Check if the user is not authenticated
            self.assertFalse(current_user.is_authenticated)

    # ... other tests

if __name__ == '__main__':
    unittest.main()
