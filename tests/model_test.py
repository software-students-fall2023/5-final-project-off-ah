import unittest
from models import db, MONGO_URI

class TestModels(unittest.TestCase):
    def test_db_connection(self):
        self.assertIsNotNone(db)
        self.assertEqual(db.name, 'bank')
        self.assertIn('bank', MONGO_URI)

if __name__ == '__main__':
    unittest.main()
