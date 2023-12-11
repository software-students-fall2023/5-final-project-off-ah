from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, UserMixin
from models import db
from bson.objectid import ObjectId

auth = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    @staticmethod
    def get(user_id):
        user_doc = db.users.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            return None
        return User(str(user_doc['_id']), user_doc['username'], user_doc['email'])

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = db.users.find_one({"username": username})
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        hash_pass = generate_password_hash(password, method='pbkdf2:sha256')
        db.users.insert_one({'username': username, 'email': email, 'password_hash': hash_pass})
        return redirect(url_for('auth.login'))
    return render_template('registration.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({"username": username})
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['_id'],user['username'], user['email'])
            login_user(user_obj)
            return redirect(url_for('home'))  
        flash('Invalid credentials')
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 