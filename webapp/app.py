from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/transaction_log')
def transactions():
    return render_template('transaction_log.html')

@app.route('/report')
def report():
    return render_template('report.html')
    
@app.route('/account')
def account():
    return render_template('account.html')
    
@app.route('/contact')
def contact():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True, port = 4000)
