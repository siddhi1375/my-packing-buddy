from flask import Flask, render_template, request, redirect, url_for, session, flash
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

# ---------------------- DECORATOR FOR PROTECTED ROUTES ----------------------
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
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email'); password=request.form.get('password')
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor); cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user=cursor.fetchone(); cursor.close()
        if user:
            if check_password_hash(user['password'],password):
                session['user_id']=user['id']; session['username']=user['username']
                flash('Logged in successfully!','success'); return redirect(url_for('dashboard'))
            else: flash('Invalid password.','danger')
        else: flash('Invalid email.','danger')
    return render_template('auth/login.html')


# ---------------------- SIGNUP ----------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        age = request.form.get('age', '')
        gender = request.form.get('gender', '')
        phone = request.form.get('phone', '').strip()

        errors = []

        # Backend validation
        if not re.match(r'^[A-Za-z0-9_]{3,20}$', username):
            errors.append("Username invalid")
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$', email):
            errors.append("Email invalid")
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",.<>\/\\|`~]).{8,}$', password):
            errors.append("Password invalid")
        try:
            age = int(age)
            if not (1 <= age <= 120):
                errors.append("Age invalid")
        except:
            errors.append("Age invalid")
        if gender not in ['Male', 'Female', 'Other']:
            errors.append("Gender invalid")
        if not re.match(r'^(\+?\d{1,3}[- ]?)?\d{7,15}$', phone):
            errors.append("Phone invalid")

        if errors:
            return render_template('auth/signup.html', errors=errors)

        # Hash password
        hashed_password = generate_password_hash(password)

        # Save to database
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password, age, gender, phone) VALUES (%s,%s,%s,%s,%s,%s)",
            (username, email, hashed_password, age, gender, phone)
        )
        mysql.connection.commit()
        last_id = cursor.lastrowid
        cursor.close()

        session['user_id'] = last_id
        session['username'] = username
        flash('Signup successful!', 'success')
        return redirect(url_for('home'))

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
    app.run(debug=True, port=5001)
