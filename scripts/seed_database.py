from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128 
from werkzeug.security import generate_password_hash

client = MongoClient('mongodb://localhost:27018/')
db = client['bank']

users = db['users']
transactions = db['transactions']

test_user = {
    "username": "testuser",
    "password_hash": generate_password_hash("testpass"),
    "email": "test@example.com"
}
users.insert_one(test_user)

test_transaction = {
    "_id": ObjectId("65782b2d4fa8b2784bc9e8fa"),
    "description": "Test Transaction",
    "amount": Decimal128("50.0"),
    "date": "2023-01-01",
    "category": "Salary",
    "notes": "Test Notes",
    "transaction_type": "in"
}
transactions.insert_one(test_transaction)
