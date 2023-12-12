import unittest
from webapp.forms import LoginForm, RegisterForm, TransactionForm

class TestForms(unittest.TestCase):
    def test_login_form(self):
        form = LoginForm(data={'username': 'testuser', 'password': 'testpass'})
        self.assertTrue(form.validate())

    def test_register_form(self):
        form = RegisterForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass',
            'confirm_password': 'testpass'
        })
        self.assertTrue(form.validate())

    def test_transaction_form(self):
        form = TransactionForm(data={
            'description': 'test transaction',
            'amount': 100.0,
            'date': '2023-01-01',
            'category': 'Test Category',
            'notes': 'Test Note'
        })
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
