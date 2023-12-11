from pymongo import MongoClient
from flask_login import LoginManager
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['bank']

