import unittest
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27018/')
DB_NAME = os.getenv('DB_NAME', 'bank')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

class TestModels(unittest.TestCase):
    def test_db_connection(self):
        self.assertIsNotNone(db)
        self.assertEqual(db.name, DB_NAME)
        self.assertEqual(DB_NAME, 'bank')

if __name__ == '__main__':
    unittest.main()
