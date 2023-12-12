from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, current_user
from bson.objectid import ObjectId
from auth import auth, User
from models import db  # Importing db from models.py
from forms import TransactionForm
import os
from bson.decimal128 import Decimal128
from collections import defaultdict
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


transactions_collection = db.transactions

@app.route('/')
@login_required  
def home():
    user_id = current_user.get_id()
    
    username = current_user.username

    total_balance = 0
    transactions = transactions_collection.find({"user_id": user_id})
    for transaction in transactions:
        if transaction['transaction_type'] == 'in':
            total_balance += float(transaction['amount'].to_decimal())
        else:
            total_balance -= float(transaction['amount'].to_decimal())

    recent_transactions = transactions_collection.find({"user_id": user_id}).sort("date", -1).limit(5)

    return render_template('index.html', total_balance=total_balance, recent_transactions=recent_transactions, username=username)


@app.route('/report')
@login_required  
def report():
    user_id = current_user.get_id()
    transactions = transactions_collection.find({"user_id": user_id})

    total_spent = 0
    total_received = 0
    category_sums_out = {}
    category_sums_in = {}

    monthly_income = defaultdict(float)
    monthly_outcome = defaultdict(float)

    for transaction in transactions:
        amount = float(transaction['amount'].to_decimal())
        category = transaction['category']
        transaction_date = transaction['date']
        month_year = datetime.strptime(transaction_date, '%Y-%m-%d').strftime('%Y-%m')

        if transaction['transaction_type'] == 'out':
            total_spent += amount
            category_sums_out[category] = category_sums_out.get(category, 0) + amount
            monthly_outcome[month_year] += amount
        else:
            total_received += amount
            category_sums_in[category] = category_sums_in.get(category, 0) + amount
            monthly_income[month_year] += amount

    categories_out, sums_out = zip(*category_sums_out.items()) if category_sums_out else ([], [])
    categories_in, sums_in = zip(*category_sums_in.items()) if category_sums_in else ([], [])
    
    months = sorted(set(monthly_income.keys()) | set(monthly_outcome.keys()))
    income_values = [monthly_income[month] for month in months]
    outcome_values = [monthly_outcome[month] for month in months]

    return render_template('report.html', total_spent=total_spent, total_received=total_received, category_sums_out=category_sums_out, category_sums_in=category_sums_in, categories_out=categories_out, sums_out=sums_out, categories_in=categories_in, sums_in=sums_in, months=months, income_values=income_values, outcome_values=outcome_values)

@app.route('/account')
@login_required  
def account():
    return render_template('account.html')

@app.route('/contact')
@login_required  
def contact():
    return render_template('contactus.html')

class Transaction:
    def __init__(self, user_id, description, amount, date, category, notes, transaction_type):
        self.user_id = user_id  
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
    search_query = request.args.get('search')
    user_id = current_user.get_id()  
    query = {"user_id": user_id}  
    if search_query:
        query["description"] = {"$regex": search_query, "$options": "i"}
    transaction_data = transactions_collection.find(query).sort([("date", -1), ("_id", -1)])
    transaction_list = list(transaction_data)
    return render_template('transaction_log.html', transactions=transaction_list)

@app.route('/transaction_in', methods=['POST'])
@login_required
def transaction_in():
    form = TransactionForm(request.form)
    user_id = current_user.get_id()
    transaction_data = Transaction(
            user_id,
            form.description.data,
            Decimal128(form.amount.data),
            form.date.data,
            form.category.data,
            form.notes.data,
            "in"
        )
    transaction_data.save()
    flash('Transaction added successfully!')
    return redirect(url_for('transactions'))

@app.route('/transaction_out', methods=['POST'])
@login_required
def transaction_out():
    form = TransactionForm(request.form)
    user_id = current_user.get_id()
    transaction_data = Transaction(
            user_id,
            form.description.data,
            Decimal128(form.amount.data),
            form.date.data,
            form.category.data,
            form.notes.data,
            "out"  
        )
    transaction_data.save()
    flash('Transaction added successfully!')
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



