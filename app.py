from flask import Flask, render_template, request, redirect,jsonify, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import re
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# ---------------------- MySQL CONFIG ----------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'siddhi'
app.config['MYSQL_PASSWORD'] = 'mypackingbuddy'
app.config['MYSQL_DB'] = 'my_packing_buddy'

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

# ---------------------- LOGIN ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:

            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['name'] = user['name']
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))  # redirect to home instead of dashboard
            else:
                flash('Invalid password.', 'danger')
        else:
            flash('Invalid email.', 'danger')

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
        # Name: 3-50 characters
        if not re.match(r'^.{3,50}$', name):
            errors.append("Name must be 3-50 characters long.")

        # Email: simple regex
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$', email):
            errors.append("Email is invalid.")

        # Password: min 8 characters
        if not re.match(r'^.{8,}$', password):
            errors.append("Password must be at least 8 characters long.")

        # Age: 1-120
        try:
            age = int(age)
            if not (1 <= age <= 120):
                errors.append("Age must be between 1 and 120.")
        except ValueError:
            errors.append("Age must be a number.")

        # Gender validation

        if gender not in ['Male','Female','Other']:
            errors.append("Gender invalid.")
        if errors:
            return render_template('signup.html', errors=errors)
        
        # Hash the password

        hashed_password = generate_password_hash(password)
        # Insert user into database

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO user (name, email, password, age, gender) VALUES (%s, %s, %s, %s, %s)",
            (name, email, hashed_password, age, gender)
        )
        mysql.connection.commit()
        cursor.close()
        flash("Signup successful! Please login.", "success")
        return redirect(url_for('login'))
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

# ---------------------- DESTINATION ----------------------

@app.route('/destination')
@login_required
def destination():
    return render_template('destination/destination.html')

# ---------------------- BOOKS ----------------------
@app.route('/books')
@login_required
def books():
    return render_template('main/books.html')

# ---------------------- CREATE CATEGORY ----------------------

@app.route('/createcategory')
@login_required
def create_category():
    return render_template('destination/createcategory.html')
#------------------------USER TRIPS ----------------------
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

# ---------------------- SAVED LISTS ----------------------
@app.route('/saved_lists')
@login_required
def saved_lists():
    return render_template('main/usertrip.html')

# ---------------------- ABOUT ----------------------
@app.route('/about')
@login_required
def about():
    return render_template('main/about.html')

# ---------------------- CONTACT ----------------------
@app.route('/contact')
@login_required
def contact():
    return render_template('main/contact.html')

# ---------------------- RUN APP ----------------------
if __name__ == '__main__':
    app.run(debug=True, port=5003)


