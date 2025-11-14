# app.py — cleaned, final version
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import re
from functools import wraps
from dotenv import load_dotenv
import os
import logging
import traceback
from contextlib import contextmanager

# ---------------------- Load environment ------------------------------
load_dotenv()

# ---------------------- Flask App Setup -------------------------------
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', "fallback_secret_key")

# ---------------------- Logging Setup ---------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------- MySQL CONFIG ----------------------------------
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
try:
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
except ValueError:
    app.config['MYSQL_PORT'] = 3306

# Log loaded config safely
logger.info(f"MYSQL_HOST loaded: {app.config['MYSQL_HOST']}")
logger.info(f"MYSQL_DB loaded: {app.config['MYSQL_DB']}")
logger.info(f"MYSQL_USER loaded: {'set' if app.config['MYSQL_USER'] else 'not set'}")

# Initialize MySQL
mysql = MySQL(app)

# ---------------------- Helper: Cursor Context ------------------------
@contextmanager
def get_cursor(dict_cursor=True):
    cur = None
    try:
        if dict_cursor:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        else:
            cur = mysql.connection.cursor()
        yield cur
    finally:
        try:
            if cur:
                cur.close()
        except Exception:
            pass

# ---------------------- Login Required Decorator ----------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------- Error Handler ---------------------------------
@app.errorhandler(500)
def internal_server_error(e):
    logger.error("Internal Server Error: %s", e)
    traceback.print_exc()
    return "Internal Server Error. Check server logs.", 500

# ---------------------- Health Check ----------------------------------
@app.route('/ping')
def ping():
    return jsonify({'status': 'ok', 'service': 'my-packing-buddy'})

# ---------------------- index ----------------------------------------
@app.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# ---------------------- HOME ------------------------------------------
@app.route('/home')
@login_required
def home():
    return render_template('destination/home.html')

# ---------------------- LOGIN -----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        logger.info(f"Login attempt: email={'set' if email else 'not set'}")

        try:
            with get_cursor(dict_cursor=True) as cur:
                cur.execute("SELECT * FROM user WHERE email=%s", (email,))
                account = cur.fetchone()

            if account and check_password_hash(account['password'], password):
                session['user_id'] = account['id']
                session['username'] = account.get('name')
                flash("Logged in successfully.", "success")
                return redirect(url_for('home'))
            else:
                flash("Incorrect email or password", "danger")

        except Exception:
            logger.exception("Login DB error")
            flash("Login error. Please try again.", "danger")

    return render_template('auth/login.html')

# ---------------------- SIGNUP ----------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        age = request.form.get('age', '')
        gender = request.form.get('gender', '')
        errors = []

        if not re.match(r'^.{3,50}$', name):
            errors.append("Name must be 3-50 characters long.")
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$', email):
            errors.append("Email is invalid.")
        if not re.match(r'^.{8,}$', password):
            errors.append("Password must be at least 8 characters long.")
        try:
            age = int(age)
            if not (1 <= age <= 120):
                errors.append("Age must be between 1 and 120.")
        except Exception:
            errors.append("Age must be a number.")
        if gender not in ['Male', 'Female', 'Other']:
            errors.append("Gender invalid.")

        if errors:
            return render_template('auth/signup.html', errors=errors)

        try:
            hashed_password = generate_password_hash(password)
            with get_cursor(dict_cursor=False) as cur:
                cur.execute(
                    "INSERT INTO user (name, email, password, age, gender) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, hashed_password, age, gender)
                )
                mysql.connection.commit()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception:
            logger.exception("Signup DB error")
            flash("Signup error. Maybe email already exists.", "danger")

    return render_template('auth/signup.html')

# ---------------------- LOGOUT ----------------------------------------
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


# ---------------------- OTHER ROUTES ----------------------------------
@app.route('/destination')
@login_required
def destination():
    return render_template('destination/destination.html')

@app.route('/books')
@login_required
def books():
    return render_template('destination/books.html')

@app.route('/createcategory')
@login_required
def create_category():
    return render_template('destination/createcategory.html')

@app.route('/trips')
def trips():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM feedbacks ORDER BY created_at DESC")
            feedbacks = cur.fetchall()
    except Exception:
        logger.exception("Error fetching feedbacks")
        feedbacks = []
    return render_template('main/trips.html', feedbacks=feedbacks)

@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    trip_name = request.form.get('trip_name', '')
    feedback_text = request.form.get('feedback', '')
    try:
        with get_cursor(dict_cursor=False) as cur:
            cur.execute("INSERT INTO feedbacks (trip_name, feedback_text) VALUES (%s, %s)",
                        (trip_name, feedback_text))
            mysql.connection.commit()
        return jsonify({'status': 'success', 'trip': trip_name, 'feedback': feedback_text})
    except Exception:
        logger.exception("Failed to add feedback")
        return jsonify({'status': 'error'}), 500

@app.route('/saved_lists')
@login_required
def saved_lists():
    return render_template('main/usertrip.html')

@app.route('/save_list', methods=['POST'])
def save_list():
    try:
        category = request.form.get('category')
        list_items = request.form.get('list_items')

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO saved_lists (category, list_items) VALUES (%s, %s)",
            (category, list_items)
        )
        mysql.connection.commit()
        cursor.close()
        flash("Packing list saved successfully!", "success")
        return redirect(url_for('your_category'))
    except Exception as e:
        flash(f"Error saving list: {str(e)}", "danger")
        return redirect(url_for('your_category'))

@app.route('/delete_list/<int:id>', methods=['POST'])
def delete_list(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM saved_lists WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash("List deleted successfully!", "info")
    return redirect(url_for('your_category'))

@app.route('/about')
@login_required
def about():
    return render_template('main/about.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('main/contact.html')

# ---------------------- RUN APP (LOCAL ONLY) ---------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)



eutyfvhbjn
dghyjuu

4y54u6i78ik6ujtgfbdf
r3t435y4u6i7j5yrt
r3t4y5u6ii76jyrggf
t45y6ui86jyhrtgr
rt45y6u7i8o8k6ujthrgfd
y6u7i8o97ku6jyhtrg
rghtyjuk6j
svsvsvsvsvsvsvsvvsvs