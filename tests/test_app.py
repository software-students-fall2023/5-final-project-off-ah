import unittest
from unittest.mock import patch, MagicMock
from bson.decimal128 import Decimal128
from bson.objectid import ObjectId
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'webapp')))
from webapp.app import app, current_user  

from decimal import Decimal  

class FlaskAppTests(unittest.TestCase):
    @patch('pymongo.MongoClient')
    def setUp(self, mock_mongo_client):
        self.mock_db = MagicMock()
        mock_mongo_client.return_value = self.mock_db
        self.mock_transactions_collection = self.mock_db.test_bank_app.transactions
        self.mock_transactions_collection.insert_one.return_value.inserted_id = ObjectId("5f50c31e11b36bc153ca1550")

        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
        self.app = app.test_client()

        self.test_transaction = {
            "description": "Test Transaction",
            "amount": Decimal128("50.0"),
            "date": "2023-01-01",
            "category": "Salary",
            "notes": "Test Notes",
            "transaction_type": "in"
        }
        self.inserted_transaction = self.mock_transactions_collection.insert_one(self.test_transaction).inserted_id

    def authenticate_mock_user(self, mock_current_user):
        mock_current_user.is_authenticated = True
        mock_current_user.get_id.return_value = 'test_user_id'
        mock_current_user.username = 'test_username'

    @patch('webapp.app.current_user', create=True)
    def test_home_route(self, mock_current_user):
        with app.app_context():
            self.authenticate_mock_user(mock_current_user)

            test_transactions = [
                {"transaction_type": "in", "amount": Decimal128("100.0")},
                {"transaction_type": "out", "amount": Decimal128("50.0")}
            ]
            with patch('webapp.app.transactions_collection.find') as mock_find:
                mock_cursor = MagicMock()
                mock_cursor.sort.return_value = mock_cursor
                mock_cursor.limit.return_value = test_transactions
                mock_find.return_value = mock_cursor

                response = self.app.get('/')
                self.assertEqual(response.status_code, 200)
    
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

        with patch('webapp.app.transactions_collection.insert_one', return_value={'inserted_id': oid}):
            self.mock_transactions_collection.insert_one.return_value = mock_transaction_detail
            response = self.app.get('/transaction_detail/' + str(oid))
            self.assertEqual(response.status_code, 200)

        with patch('webapp.app.db.transactions.find_one', return_value=mock_transaction_detail):
            response = self.app.get('/transaction_detail/' + str(oid))
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

    @patch('webapp.app.current_user', create=True)
    def test_invalid_transaction_detail_route(self, mock_current_user):
        self.authenticate_mock_user(mock_current_user)
        invalid_id = ObjectId() 
        response = self.app.get(f'/transaction_detail/{invalid_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
