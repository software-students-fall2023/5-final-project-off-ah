import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import webapp
from bson.decimal128 import Decimal128
from bson.objectid import ObjectId
from webapp.app import app
from decimal import Decimal  
from pymongo import MongoClient  


class FlaskAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['test_bank_app']  
        cls.transactions_collection = cls.db.transactions

        test_transaction = {
            "_id": ObjectId("65782b2d4fa8b2784bc9e8fa"),
            "description": "Test Transaction",
            "amount": Decimal128("50.0"),
            "date": "2023-01-01",
            "category": "Salary",
            "notes": "Test Notes",
            "transaction_type": "in"
        }
        cls.transactions_collection.insert_one(test_transaction)

    @classmethod
    def tearDownClass(cls):
        cls.transactions_collection.delete_one({"_id": ObjectId("65782b2d4fa8b2784bc9e8fa")})
        cls.client.close()

    def setUp(self):
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
        self.app = app.test_client()

    def authenticate_mock_user(self, mock_current_user):
        mock_current_user.is_authenticated.return_value = True
        mock_current_user.get_id.return_value = 'test_user_id'
        mock_current_user.username = 'test_username'

    @patch('webapp.app.current_user', create=True)
    def test_home_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        mock_transactions = [
            {'transaction_type': 'in', 'amount': 100.0},
            {'transaction_type': 'out', 'amount': 50.0}
        ]

    @patch('webapp.app.current_user', create=True)
    def test_report_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        mock_current_user.get_id.return_value = 'test_user_id'

        mock_transactions = [
            {'transaction_type': 'out', 'amount': MagicMock(to_decimal=MagicMock(return_value=30.0)), 'category': 'Food & Drink', 'date': '2023-01-01'},
            {'transaction_type': 'in', 'amount': MagicMock(to_decimal=MagicMock(return_value=100.0)), 'category': 'Salary', 'date': '2023-01-02'},
        ]
        with patch('webapp.app.transactions_collection.find', return_value=mock_transactions):
            response = self.app.get('/report')
            self.assertEqual(response.status_code, 200)


    @patch('webapp.app.current_user', create=True)
    def test_account_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        response = self.app.get('/account')
        self.assertEqual(response.status_code, 200)

    @patch('webapp.app.current_user', create=True)
    def test_contact_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)

    @patch('webapp.app.current_user', create=True)
    def test_transactions_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        with patch('webapp.app.transactions_collection.find') as mock_find:
            mock_find.return_value.sort.return_value = []  
            response = self.app.get('/transaction_log')
            self.assertEqual(response.status_code, 200)

    @patch('webapp.forms.TransactionForm')
    def test_transaction_in_route(self, mock_form):
        mock_form.return_value.validate_on_submit.return_value = True
        form_data = {
            'description': 'Test Expense',
            'amount': 50.0,
            'date': '2023-01-02',
            'category': 'Refund',
            'notes': 'Test Expense Notes'
        }
        with patch('webapp.app.current_user', create=True) as mock_current_user:
            self.authenticate_mock_user(mock_current_user)
            with patch('webapp.app.transactions_collection.insert_one') as mock_insert:
                response = self.app.post('/transaction_in', data=form_data)
                self.assertEqual(response.status_code, 302)


    @patch('webapp.forms.TransactionForm')
    def test_transaction_out_route(self, mock_form):
        mock_form.return_value.validate_on_submit.return_value = True
        form_data = {
            'description': 'Test Expense',
            'amount': 50.0,
            'date': '2023-01-02',
            'category': 'Food & Drink',
            'notes': 'Test Expense Notes'
        }
        with patch('webapp.app.current_user', create=True) as mock_current_user:
            self.authenticate_mock_user(mock_current_user)
            with patch('webapp.app.transactions_collection.insert_one') as mock_insert:
                response = self.app.post('/transaction_out', data=form_data)
                self.assertEqual(response.status_code, 302)

    @patch('webapp.app.current_user', create=True)
    def test_transaction_detail_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        oid = ObjectId('65782b2d4fa8b2784bc9e8fa')

        mock_transaction_detail = {
            '_id': oid,  
            'description': 'Test Transaction',
            'amount': 50.0,
            'date': '2023-01-01',
            'category': 'Salary',
            'notes': 'Test Notes',
            'transaction_type': 'in'
        }

        with patch('webapp.app.transactions_collection.insert_one', 
                 return_value={'inserted_id': mock_transaction_detail['_id']}):
            insert_result = webapp.app.transactions_collection.insert_one(mock_transaction_detail)
            inserted_id = insert_result['inserted_id']

            self.assertEqual(mock_transaction_detail['_id'], inserted_id)

        with patch('webapp.app.db.transactions.find_one', return_value=mock_transaction_detail):
            response = self.app.get('/transaction_detail/' + str(inserted_id))
            self.assertEqual(response.status_code, 200)

    @patch('webapp.app.current_user', create=True)
    def test_money_in_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        response = self.app.get('/money_in')
        self.assertEqual(response.status_code, 200)
        
    @patch('webapp.app.current_user', create=True)
    def test_money_out_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        response = self.app.get('/money_out')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
