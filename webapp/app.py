from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required
from bson.objectid import ObjectId
from auth import auth, User
from models import db  # Importing db from models.py
from forms import TransactionForm
import os
from bson.decimal128 import Decimal128

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


transactions_collection = db.transactions

@app.route('/')
@login_required  
def home():
    return render_template('index.html')

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

class Transaction:
    def __init__(self, description, amount, date, category, notes, transaction_type):
        self.description = description
        self.amount = amount
        self.date = date
        self.category = category
        self.notes = notes
        self.transaction_type = transaction_type

    def save(self):
        result = transactions_collection.insert_one(self.__dict__)
        print("Transaction saved with ID:", result.inserted_id)

@app.route('/transaction_log')
@login_required
def transactions():
    transaction_data = transactions_collection.find()
    transaction_list = list(transaction_data)  
    print("Fetched transactions:", transaction_list)  
    return render_template('transaction_log.html', transactions=transaction_list)


@app.route('/transaction_in', methods=['POST'])
@login_required
def transaction_in():
    form = TransactionForm(request.form)
    # if form.validate_on_submit():
    transaction_data = Transaction(
            form.description.data,
            Decimal128(form.amount.data),
            form.date.data,
            form.category.data,
            form.notes.data,
            "in"
        )
    transaction_data.save()
    flash('Transaction added successfully!')
    # else:
    #     flash('Error in transaction form.')
    
    return redirect(url_for('transactions'))


@app.route('/transaction_out', methods=['POST'])
@login_required
def transaction_out():
    form = TransactionForm(request.form)
    # if form.validate_on_submit():
    transaction_data = Transaction(
            form.description.data,
            Decimal128(form.amount.data),
            form.date.data,
            form.category.data,
            form.notes.data,
            "out"  
        )
    transaction_data.save()
    flash('Transaction added successfully!')
    # else:
    #     flash('Error in transaction form.')
    return redirect(url_for('transactions'))

    
@app.route('/transaction_detail/<id>')
@login_required
def transaction_detail(id):
    transaction = db.transactions.find_one({'_id': ObjectId(id)})
    if transaction:
        return render_template('transaction_detail.html', transaction=transaction)
    else:
        return "Transaction not found", 404


@app.route('/money_in')
@login_required
def money_in():
    return render_template('money_in.html')

@app.route('/money_out')
@login_required
def money_out():
    return render_template('money_out.html')


@login_manager.user_loader
def load_user(user_id):
    u = db.users.find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    return User(str(u['_id']), u['username'], u['email'])


app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True, port=4000)



