from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient
from flask_login import LoginManager, login_required
from bson.objectid import ObjectId
from auth import auth, User
from models import db

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@app.route('/')
@login_required  
def home():
    return render_template('index.html')

@app.route('/transaction_log')
@login_required  
def transactions():
    return render_template('transaction_log.html')

@app.route('/report')
@login_required  
def report():
    return render_template('report.html')

@app.route('/account')
@login_required  
def account():
    return render_template('account.html')

@app.route('/contact')
@login_required  
def contact():
    return render_template('contactus.html')



@login_manager.user_loader
def load_user(user_id):
    u = db.users.find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    return User(str(u['_id']), u['username'], u['email'])


app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True, port=4000)

