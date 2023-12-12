import unittest
from flask import Flask
from webapp.app import app
from webapp.forms import LoginForm, RegisterForm, TransactionForm

class FormTestCase(unittest.TestCase):

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_login_form(self):
        with app.test_request_context():
            form = LoginForm(data={'username': 'testuser', 'password': 'testpass'})
            if not form.validate():
                print("Login Form Errors:", form.errors)
            self.assertTrue(form.validate(), msg="Login form validation failed")

    def test_register_form(self):
        with app.test_request_context():
            form = RegisterForm(data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass',
                'confirm_password': 'testpass'
            })
            if not form.validate():
                print("Register Form Errors:", form.errors)
            self.assertTrue(form.validate(), msg="Register form validation failed")

    def test_transaction_form(self):
        with app.test_request_context():
            form = TransactionForm(data={
                'description': 'Test Transaction',
                'amount': 100.00,
                'date': '2023-01-01',
                'category': 'Test Category',
                'notes': 'Test Notes'
            })
            if not form.validate():
                print("Transaction Form Errors:", form.errors)
            self.assertTrue(form.validate(), msg="Transaction form validation failed")

if __name__ == '__main__':
    unittest.main()
