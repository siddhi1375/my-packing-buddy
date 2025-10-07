from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ---------------- MySQL Configuration ----------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypackingbuddy'
app.config['MYSQL_DB'] = 'my_packing_buddy'

mysql = MySQL(app)

# ---------------- Signup ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        account = cursor.fetchone()
        if account:
            flash('Email already registered! Please log in.', 'danger')
            return redirect(url_for('signup'))

        # Backend validation using regex
        import re
        if not re.match(r'^[A-Za-z0-9_]{3,20}$', username):
            flash('Username must be 3–20 chars long and contain only letters, numbers, or underscores.', 'danger')
            return redirect(url_for('signup'))

        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$', email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for('signup'))

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) \
           or not re.search(r'[0-9]', password) or not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",.<>\/\\|`~]', password):
            flash('Password must have 8+ chars with uppercase, lowercase, number, and special symbol.', 'danger')
            return redirect(url_for('signup'))

        if not age.isdigit() or not (1 <= int(age) <= 120):
            flash('Please enter a valid age between 1 and 120.', 'danger')
            return redirect(url_for('signup'))

        if gender not in ['Male', 'Female', 'Other']:
            flash('Please select a valid gender.', 'danger')
            return redirect(url_for('signup'))

        if not re.match(r'^(\+?\d{1,3}[- ]?)?\d{7,15}$', phone):
            flash('Invalid phone number format.', 'danger')
            return redirect(url_for('signup'))

        # Hash password
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)

        # Insert user
        cursor.execute("""
            INSERT INTO users (username, email, password, age, gender, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, email, hashed_password, age, gender, phone))
        mysql.connection.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    # Use correct path for template
    return render_template('auth/signup.html')
#-----------------login----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Check password
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash(f"Welcome back, {user['username']}!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password!", "danger")
                return redirect(url_for('login'))
        else:
            flash("Email not registered!", "danger")
            return redirect(url_for('login'))

    # GET request
    return render_template('auth/login.html')
#-----------------logout-------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))
#------------------home---------------------------
@app.route('/')
def index():
    # This will show the home page when user visits '/'
    return render_template('destination/home.html')

@app.route('/home')
def home():
    # Optional: another route if you want '/home' to work too
    return render_template('destination/home.html')
# ---------------- Books Pages --------------------
@app.route('/books')
def books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/books.html')

@app.route('/beach_books')
def beach_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/beach_books.html')

@app.route('/forest_books')
def forest_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/forest_books.html')

@app.route('/desert_books')
def desert_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/desert_books.html')

@app.route('/snowvalley_books')
def snowvalley_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/snowvalley_books.html')

@app.route('/lake_river_books')
def lake_river_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/lake_river_books.html')

@app.route('/mountain_books')
def mountain_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/mountain_books.html')

@app.route('/general_books')
def general_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/general_books.html')

# ---------------- About Page ----------------
@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/about.html')

# ---------------- User Trips ----------------
@app.route('/user_trips', methods=['GET', 'POST'])
def user_trips():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and request.form.get('action') == 'add':
        username = request.form['username']
        experience = request.form['experience']
        cursor.execute(
            "INSERT INTO user_trips (user_id, username, experience) VALUES (%s, %s, %s)",
            (session['user_id'], username, experience)
        )
        mysql.connection.commit()
        flash("Review added successfully!", "success")

    if request.method == 'POST' and request.form.get('action') == 'edit':
        review_id = request.form['review_id']
        new_experience = request.form['experience']
        cursor.execute(
            "UPDATE user_trips SET experience=%s WHERE id=%s AND user_id=%s",
            (new_experience, review_id, session['user_id'])
        )
        mysql.connection.commit()
        flash("Review updated successfully!", "success")

    if request.method == 'POST' and request.form.get('action') == 'delete':
        review_id = request.form['review_id']
        cursor.execute(
            "DELETE FROM user_trips WHERE id=%s AND user_id=%s",
            (review_id, session['user_id'])
        )
        mysql.connection.commit()
        flash("Review deleted successfully!", "success")

    cursor.execute("SELECT id, user_id, username, experience FROM user_trips ORDER BY id DESC")
    reviews = cursor.fetchall()
    cursor.close()

    return render_template("main/usertrips.html", reviews=reviews, current_user_id=session['user_id'])

# ---------------- Destination Page ----------------
@app.route('/destination')
def destination():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usercategorys WHERE user_id=%s", (session['user_id'],))
    user_categories = cursor.fetchall() or []
    cursor.close()

    for cat in user_categories:
        items_val = cat.get('items')
        if items_val and isinstance(items_val, str):
            cat['item_list'] = [item.strip() for item in items_val.split(',') if item.strip()]
        else:
            cat['item_list'] = []

    destinations = [
        {"name": "Beach", "img": url_for('static', filename='beach.jpg')},
        {"name": "Forest", "img": url_for('static', filename='forest.jpg')},
        {"name": "Desert", "img": url_for('static', filename='desert.jpeg')},
        {"name": "Snow Valley", "img": url_for('static', filename='snowvalley.jpg')},
        {"name": "Lake & River", "img": url_for('static', filename='lake.jpg')},
        {"name": "Mountain", "img": url_for('static', filename='mountain.jpg')},
        {"name": "In General", "img": url_for('static', filename='ingeneral.jpg')}
    ]

    return render_template("destination/destination.html",
                           user_categories=user_categories,
                           destinations=destinations)

# ---------------- Create / Edit Category ----------------
@app.route('/create_category', methods=['GET', 'POST'])
def create_category():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and request.form.get('action') == 'create':
        name = request.form['category_name']
        items = request.form['items']
        cursor.execute(
            "INSERT INTO usercategorys (user_id, category_name, items) VALUES (%s, %s, %s)",
            (session['user_id'], name, items)
        )
        mysql.connection.commit()
        flash("Category created successfully!", "success")
        return redirect(url_for('create_category'))

    if request.method == 'POST' and request.form.get('action') == 'edit':
        cat_id = request.form['category_id']
        new_name = request.form['category_name']
        new_items = request.form['items']
        cursor.execute(
            "UPDATE usercategorys SET category_name=%s, items=%s WHERE id=%s AND user_id=%s",
            (new_name, new_items, cat_id, session['user_id'])
        )
        mysql.connection.commit()
        flash("Category updated successfully!", "success")
        return redirect(url_for('create_category'))

    cursor.execute("SELECT * FROM usercategorys WHERE user_id=%s", (session['user_id'],))
    categories = cursor.fetchall()
    cursor.close()

    return render_template('destination/createcategory.html', categories=categories)
#-----------------contact us-----------------------
@app.route('/contact')
def contact():
    return render_template('contact.html')  

# ---------------- Delete Category ----------------
@app.route('/delete_category/<int:category_id>', methods=['GET'])
def delete_category(category_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute(
        "DELETE FROM usercategorys WHERE id=%s AND user_id=%s",
        (category_id, session['user_id'])
    )
    mysql.connection.commit()
    cursor.close()
    flash("Category deleted successfully!", "success")
    return redirect(url_for('create_category'))

# ---------------- Packing List ----------------
@app.route('/packinglist')
def packinglist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('destination/packinglist.html')

# ---------------- Profile ----------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        age = int(request.form.get('age'))

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE user SET username=%s, email=%s, age=%s WHERE id=%s
        """, (username, email, age, session['user_id']))
        mysql.connection.commit()
        cursor.close()

        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()

    return render_template('main/profile.html', user=user)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ---------------- MySQL Configuration ----------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypackingbuddy'
app.config['MYSQL_DB'] = 'my_packing_buddy'

mysql = MySQL(app)

# ---------------- Signup ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        account = cursor.fetchone()
        if account:
            flash('Email already registered! Please log in.', 'danger')
            return redirect(url_for('signup'))

        if not re.match(r'^[A-Za-z0-9_]{3,20}$', username):
            flash('Username must be 3–20 chars long and contain only letters, numbers, or underscores.', 'danger')
            return redirect(url_for('signup'))

        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$', email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for('signup'))

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) \
           or not re.search(r'[0-9]', password) or not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",.<>\/\\|`~]', password):
            flash('Password must have 8+ chars with uppercase, lowercase, number, and special symbol.', 'danger')
            return redirect(url_for('signup'))

        if not age.isdigit() or not (1 <= int(age) <= 120):
            flash('Please enter a valid age between 1 and 120.', 'danger')
            return redirect(url_for('signup'))

        if gender not in ['Male', 'Female', 'Other']:
            flash('Please select a valid gender.', 'danger')
            return redirect(url_for('signup'))

        if not re.match(r'^(\+?\d{1,3}[- ]?)?\d{7,15}$', phone):
            flash('Invalid phone number format.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (username, email, password, age, gender, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, email, hashed_password, age, gender, phone))
        mysql.connection.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/signup.html')

#-----------------login----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash(f"Welcome back, {user['username']}!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password!", "danger")
                return redirect(url_for('login'))
        else:
            flash("Email not registered!", "danger")
            return redirect(url_for('login'))
    return render_template('auth/login.html')

#-----------------logout-------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))

#------------------home---------------------------
@app.route('/')
def index():
    return render_template('destination/home.html')

@app.route('/home')
def home():
    return render_template('destination/home.html')

# ---------------- Books Pages --------------------
@app.route('/books')
def books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/books.html')

@app.route('/beach_books')
def beach_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/beach_books.html')

@app.route('/forest_books')
def forest_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/forest_books.html')

@app.route('/desert_books')
def desert_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/desert_books.html')

@app.route('/snowvalley_books')
def snowvalley_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/snowvalley_books.html')

@app.route('/lake_river_books')
def lake_river_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/lake_river_books.html')

@app.route('/mountain_books')
def mountain_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/mountain_books.html')

@app.route('/general_books')
def general_books():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/general_books.html')

# ---------------- About Page ----------------
@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main/about.html')

# ---------------- User Trips ----------------
@app.route('/user_trips', methods=['GET', 'POST'])
def user_trips():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and request.form.get('action') == 'add':
        username = request.form['username']
        experience = request.form['experience']
        cursor.execute(
            "INSERT INTO user_trips (user_id, username, experience) VALUES (%s, %s, %s)",
            (session['user_id'], username, experience)
        )
        mysql.connection.commit()
        flash("Review added successfully!", "success")

    if request.method == 'POST' and request.form.get('action') == 'edit':
        review_id = request.form['review_id']
        new_experience = request.form['experience']
        cursor.execute(
            "UPDATE user_trips SET experience=%s WHERE id=%s AND user_id=%s",
            (new_experience, review_id, session['user_id'])
        )
        mysql.connection.commit()
        flash("Review updated successfully!", "success")

    if request.method == 'POST' and request.form.get('action') == 'delete':
        review_id = request.form['review_id']
        cursor.execute(
            "DELETE FROM user_trips WHERE id=%s AND user_id=%s",
            (review_id, session['user_id'])
        )
        mysql.connection.commit()
        flash("Review deleted successfully!", "success")

    cursor.execute("SELECT id, user_id, username, experience FROM user_trips ORDER BY id DESC")
    reviews = cursor.fetchall()
    cursor.close()

    return render_template("main/usertrips.html", reviews=reviews, current_user_id=session['user_id'])

# ---------------- Destination Page ----------------
@app.route('/destination')
def destination():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usercategorys WHERE user_id=%s", (session['user_id'],))
    user_categories = cursor.fetchall() or []
    cursor.close()

    for cat in user_categories:
        items_val = cat.get('items')
        if items_val and isinstance(items_val, str):
            cat['item_list'] = [item.strip() for item in items_val.split(',') if item.strip()]
        else:
            cat['item_list'] = []

    destinations = [
        {"name": "Beach", "img": url_for('static', filename='beach.jpg')},
        {"name": "Forest", "img": url_for('static', filename='forest.jpg')},
        {"name": "Desert", "img": url_for('static', filename='desert.jpeg')},
        {"name": "Snow Valley", "img": url_for('static', filename='snowvalley.jpg')},
        {"name": "Lake & River", "img": url_for('static', filename='lake.jpg')},
        {"name": "Mountain", "img": url_for('static', filename='mountain.jpg')},
        {"name": "In General", "img": url_for('static', filename='ingeneral.jpg')}
    ]

    return render_template("destination/destination.html",
                           user_categories=user_categories,
                           destinations=destinations)

# ---------------- Weather Pages ----------------
@app.route('/male_weather')
def male_weather(): return render_template('destination/maleweather.html')
@app.route('/female_weather')
def female_weather(): return render_template('destination/femaleweather.html')
@app.route('/baby_weather')
def baby_weather(): return render_template('destination/babyweather.html')

# ---------------- Gender Selection Pages ----------------
@app.route('/beachgender')
def beachgender(): return render_template('destination/beachgender.html')
@app.route('/forestgender')
def forestgender(): return render_template('destination/forestgender.html')
@app.route('/desertgender')
def desertgender(): return render_template('destination/desertgender.html')
@app.route('/snowvalleygender')
def snowvalleygender(): return render_template('destination/snowvalleygender.html')
@app.route('/lakeandrivergender')
def lakeandrivergender(): return render_template('destination/lakeandrivergender.html')
@app.route('/mountaingender')
def mountaingender(): return render_template('destination/mountaingender.html')
@app.route('/ingeneralgender')
def ingeneralgender(): return render_template('destination/ingeneralgender.html')

# ---------------- Male Pages ----------------
@app.route('/malebeach')
def malebeach(): return render_template('destination/malebeach.html')
@app.route('/maleforest')
def maleforest(): return render_template('destination/maleforest.html')
@app.route('/maledesert')
def maledesert(): return render_template('destination/maledesert.html')
@app.route('/malesnowvalley')
def malesnowvalley(): return render_template('destination/malesnowvalley.html')
@app.route('/malelakeandriver')
def malelakeandriver(): return render_template('destination/malelakeandriver.html')
@app.route('/malemountain')
def malemountain(): return render_template('destination/malemountain.html')
@app.route('/maleingeneral')
def maleingeneral(): return render_template('destination/maleingeneral.html')

# ---------------- Female Pages ----------------
@app.route('/femalebeach')
def femalebeach(): return render_template('destination/femalebeach.html')
@app.route('/femaleforest')
def femaleforest(): return render_template('destination/femaleforest.html')
@app.route('/femaledesert')
def femaledesert(): return render_template('destination/femaledesert.html')
@app.route('/femalesnowvalley')
def femalesnowvalley(): return render_template('destination/femalesnowvalley.html')
@app.route('/femalelakeandriver')
def femalelakeandriver(): return render_template('destination/femalelakeandriver.html')
@app.route('/femalemountain')
def femalemountain(): return render_template('destination/femalemountain.html')
@app.route('/femaleingeneral')
def femaleingeneral(): return render_template('destination/femaleingeneral.html')

# ---------------- Infant Pages ----------------
@app.route('/infantbeach')
def infantbeach(): return render_template('destination/babybeach.html')
@app.route('/infantforest')
def infantforest(): return render_template('destination/babyforest.html')
@app.route('/infantdesert')
def infantdesert(): return render_template('destination/babydesert.html')
@app.route('/infantsnowvalley')
def infantsnowvalley(): return render_template('destination/babysnowvalley.html')
@app.route('/infantlakeandriver')
def infantlakeandriver(): return render_template('destination/babylakeandriver.html')
@app.route('/infantmountain')
def infantmountain(): return render_template('destination/babymountain.html')
@app.route('/infantingeneral')
def infantingeneral(): return render_template('destination/babyingeneral.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)

