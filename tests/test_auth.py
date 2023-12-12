import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_login import LoginManager  # Import LoginManager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'webapp')))
from auth import auth, User

# Mock url_for to prevent application context errors
with patch('flask.url_for', MagicMock(return_value='/')):
    from webapp.auth import login_user

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        @self.app.route('/home')
        def home():
            return 'Home Page'
        
        # Initialize the login manager and attach it to the test app
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        
        # Set the user loader callback for Flask-Login
        @self.login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)
        
        self.app.register_blueprint(auth)
        self.client = self.app.test_client()

    @patch('webapp.auth.db', MagicMock())
    @patch('webapp.auth.check_password_hash', MagicMock(return_value=True))
    @patch('webapp.auth.login_user', MagicMock(return_value=True))
    @patch('flask.url_for', MagicMock(side_effect=lambda endpoint, **values: f"/mock-{endpoint}"))
    def test_login(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)


    @patch('webapp.auth.db', MagicMock())
    def test_register(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)


    # Add more tests as needed for logout and other auth routes

if __name__ == '__main__':
    unittest.main()
