from app import db
from flask_login import UserMixin

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True)
    email = db.StringField(unique=True, required=True)
    password_hash = db.StringField(required=True)

class Transaction(db.Document):
    user_id = db.ReferenceField(User)
    type = db.StringField(required=True)  # 'income' or 'expense'
    amount = db.DecimalField(required=True)
    date = db.DateTimeField(required=True)
    category = db.StringField()
    notes = db.StringField()

