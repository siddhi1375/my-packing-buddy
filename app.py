from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import re
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# ---------------------- MySQL CONFIG -------------------------------
app.config['MYSQL_HOST'] = 'sql100.infinityfree.com'
app.config['MYSQL_USER'] = 'if0_40246577'
app.config['MYSQL_PASSWORD'] = '13SvserA1P'
app.config['MYSQL_DB'] = 'if0_40246577_mypackingbuddy'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ------------------- DECORATOR FOR PROTECTED ROUTES -----------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------- INDEX REDIRECT ----------------------
@app.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('home'))
    return redirect(url_for('login'))
#------------------------- LOGIN----------------------------------
import logging

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        app.logger.info(f"Received login form data: email={email}, password={'set' if password else 'not set'}")
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
            account = cursor.fetchone()
            cursor.close()
            if account and check_password_hash(account['password'], password):
                session['user_id'] = account['id']
                session['username'] = account['name']
                return redirect(url_for('home'))   
            else:
                flash("Incorrect email/password", "danger")
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            flash(f"Login error: {str(e)}", "danger")
    return render_template('auth/login.html')


# ---------------------- SIGNUP ----------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        age = request.form.get('age', '')
        gender = request.form.get('gender', '')
        errors = []

        # Validate name
        if not re.match(r'^.{3,50}$', name):
            errors.append("Name must be 3-50 characters long.")
        # Validate email
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$', email):
            errors.append("Email is invalid.")
        # Validate password
        if not re.match(r'^.{8,}$', password):
            errors.append("Password must be at least 8 characters long.")
        # Validate age
        try:
            age = int(age)
            if not (1 <= age <= 120):
                errors.append("Age must be between 1 and 120.")
        except ValueError:
            errors.append("Age must be a number.")
        # Validate gender
        if gender not in ['Male', 'Female', 'Other']:
            errors.append("Gender invalid.")

        if errors:
            return render_template('auth/signup.html', errors=errors)

        try:
            hashed_password = generate_password_hash(password)
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO user (name, email, password, age, gender) VALUES (%s, %s, %s, %s, %s)",
                (name, email, hashed_password, age, gender)
            )
            mysql.connection.commit()
            cursor.close()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            app.logger.error(f"Signup DB error: {str(e)}")
            flash(f"Signup error: {str(e)}", "danger")
            return render_template('auth/signup.html')

    return render_template('auth/signup.html')

# ---------------------- LOGOUT ----------------------
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# ---------------------- HOME ----------------------
@app.route('/home')
@login_required
def home():
    return render_template('destination/home.html')

# ---------------------- OTHER ROUTES ----------------------
@app.route('/destination')
@login_required
def destination():
    return render_template('destination/destination.html')

@app.route('/books')
@login_required
def books():
    return render_template('main/books.html')

@app.route('/createcategory')
@login_required
def create_category():
    return render_template('destination/createcategory.html')

@app.route('/trips')
def trips():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM feedbacks ORDER BY created_at DESC")
    feedbacks = cur.fetchall()
    cur.close()
    return render_template('main/trips.html', feedbacks=feedbacks)

@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    trip_name = request.form['trip_name']
    feedback_text = request.form['feedback']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO feedbacks (trip_name, feedback_text) VALUES (%s, %s)",(trip_name,feedback_text))
    mysql.connection.commit()
    cur.close()
    return jsonify({'status': 'success', 'trip': trip_name, 'feedback': feedback_text})

@app.route('/saved_lists')
@login_required
def saved_lists():
    return render_template('main/usertrip.html')

@app.route('/about')
@login_required
def about():
    return render_template('main/about.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('main/contact.html')

# ---------------------- RUN APP ----------------------
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT env var or 5000 default
    app.run(debug=True, host='0.0.0.0', port=port)









