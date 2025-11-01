# app.py — cleaned, safe, and ready for Render
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

# Load environment from .env when present (harmless on Render)
load_dotenv()

# App setup
app = Flask(__name__)
# Keep secret_key in env for production — fallback for local dev
app.secret_key = os.getenv('FLASK_SECRET_KEY', "6009c3ba565191435fac07e95589191f")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------- MySQL CONFIG -------------------------------
# Read env vars safely and provide sensible defaults where appropriate
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# Port might be missing in env; default to 3306 if not provided
try:
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
except ValueError:
    app.config['MYSQL_PORT'] = 3306

# Log the loaded config keys (do NOT print secrets)
logger.info(f"MYSQL_HOST loaded: {app.config['MYSQL_HOST']}")
logger.info(f"MYSQL_DB loaded: {app.config['MYSQL_DB']}")
logger.info(f"MYSQL_USER loaded: {'set' if app.config['MYSQL_USER'] else 'not set'}")

# Initialize MySQL (only once)
mysql = MySQL(app)

# ------------------- Helper: DB cursor context ---------------------
# Use context manager for safety
from contextlib import contextmanager

@contextmanager
def get_cursor(dict_cursor=True):
    """
    Yields a cursor, ensures close when done.
    Use: with get_cursor() as cur: cur.execute(...)
    """
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

# ------------------- DECORATOR FOR PROTECTED ROUTES -----------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------- Error handler (logs traceback) --------------
@app.errorhandler(500)
def internal_server_error(e):
    logger.error("Internal Server Error: %s", e)
    # Print traceback to logs for debugging
    traceback.print_exc()
    return "Internal Server Error. Check server logs.", 500

# ---------------------- Health route -------------------------------
@app.route('/ping')
def ping():
    return jsonify({'status': 'ok', 'service': 'my-packing-buddy'})

# ---------------------- INDEX REDIRECT ------------------------------
@app.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# ------------------------- LOGIN -----------------------------------
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

        except Exception as e:
            logger.exception("Login DB error")
            flash("Login error. Please try again.", "danger")

    return render_template('auth/login.html')

# ---------------------- SIGNUP -------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        age = request.form.get('age', '')
        gender = request.form.get('gender', '')
        errors = []

        # Basic validation
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

    return render_template('auth/signup.html')

# ---------------------- LOGOUT -------------------------------------
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# ---------------------- HOME ---------------------------------------
@app.route('/home')
@login_required
def home():
    return render_template('destination/home.html')

# ---------------------- OTHER ROUTES --------------------------------

@app.route('/destination')
@login_required
def destination():
    return render_template('destination/destination.html')

# Ensure this points to the actual template you have in templates/destination/
@app.route('/books')
@login_required
def books():
    # If you want to pass actual book data from DB, fetch here.
    # For now we just render the destination/books.html template.
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

@app.route('/about')
@login_required
def about():
    return render_template('main/about.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('main/contact.html')

# ---------------------- RUN APP ------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Debug True only for local development. On Render, gunicorn runs the app.
    app.run(debug=True, host='0.0.0.0', port=port)

