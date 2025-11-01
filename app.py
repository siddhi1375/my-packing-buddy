from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import re
from functools import wraps
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env
print("Loaded host:", os.getenv('MYSQL_HOST'))  # test line (temporary)

app = Flask(__name__)
app.secret_key = "6009c3ba565191435fac07e95589191f"

# ---------------------- MySQL CONFIG -------------------------------

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL==> Downloading cache...
==> Cloning from https://github.com/siddhi1375/my-packing-buddy
==> Checking out commit 9801ef9b08f4281f52e5dcf0a8a7ffefd35d3da3 in branch main
==> Transferred 63MB in 2s. Extraction took 1s.
==> Installing Python version 3.13.4...
==> Using Python version 3.13.4 (default)
==> Docs on specifying a Python version: https://render.com/docs/python-version
==> Using Poetry version 2.1.3 (default)
==> Docs on specifying a Poetry version: https://render.com/docs/poetry-version
==> Running build command 'pip install -r requirements.txt'...
Collecting Flask==2.3.2 (from -r requirements.txt (line 1))
  Using cached Flask-2.3.2-py3-none-any.whl.metadata (3.7 kB)
Collecting gunicorn==21.2.0 (from -r requirements.txt (line 2))
  Using cached gunicorn-21.2.0-py3-none-any.whl.metadata (4.1 kB)
Collecting requests==2.31.0 (from -r requirements.txt (line 3))
  Using cached requests-2.31.0-py3-none-any.whl.metadata (4.6 kB)
Collecting python-dotenv==1.0.0 (from -r requirements.txt (line 4))
  Using cached python_dotenv-1.0.0-py3-none-any.whl.metadata (21 kB)
Collecting flask-cors==6.0.1 (from -r requirements.txt (line 5))
  Using cached flask_cors-6.0.1-py3-none-any.whl.metadata (5.3 kB)
Collecting flask-mysqldb==1.0.1 (from -r requirements.txt (line 6))
  Using cached flask_mysqldb-1.0.1-py3-none-any.whl
Collecting Werkzeug>=2.3.3 (from Flask==2.3.2->-r requirements.txt (line 1))
  Using cached werkzeug-3.1.3-py3-none-any.whl.metadata (3.7 kB)
Collecting Jinja2>=3.1.2 (from Flask==2.3.2->-r requirements.txt (line 1))
  Using cached jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting itsdangerous>=2.1.2 (from Flask==2.3.2->-r requirements.txt (line 1))
  Using cached itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting click>=8.1.3 (from Flask==2.3.2->-r requirements.txt (line 1))
  Using cached click-8.3.0-py3-none-any.whl.metadata (2.6 kB)
Collecting blinker>=1.6.2 (from Flask==2.3.2->-r requirements.txt (line 1))
  Using cached blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
Collecting packaging (from gunicorn==21.2.0->-r requirements.txt (line 2))
  Using cached packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
Collecting charset-normalizer<4,>=2 (from requests==2.31.0->-r requirements.txt (line 3))
  Using cached charset_normalizer-3.4.4-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (37 kB)
Collecting idna<4,>=2.5 (from requests==2.31.0->-r requirements.txt (line 3))
  Using cached idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Collecting urllib3<3,>=1.21.1 (from requests==2.31.0->-r requirements.txt (line 3))
  Using cached urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests==2.31.0->-r requirements.txt (line 3))
  Using cached certifi-2025.10.5-py3-none-any.whl.metadata (2.5 kB)
Collecting mysqlclient>=1.3.7 (from flask-mysqldb==1.0.1->-r requirements.txt (line 6))
  Using cached mysqlclient-2.2.7-cp313-cp313-linux_x86_64.whl
Collecting MarkupSafe>=2.0 (from Jinja2>=3.1.2->Flask==2.3.2->-r requirements.txt (line 1))
  Using cached markupsafe-3.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Using cached Flask-2.3.2-py3-none-any.whl (96 kB)
Using cached gunicorn-21.2.0-py3-none-any.whl (80 kB)
Using cached requests-2.31.0-py3-none-any.whl (62 kB)
Using cached python_dotenv-1.0.0-py3-none-any.whl (19 kB)
Using cached flask_cors-6.0.1-py3-none-any.whl (13 kB)
Using cached charset_normalizer-3.4.4-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (153 kB)
Using cached idna-3.11-py3-none-any.whl (71 kB)
Using cached urllib3-2.5.0-py3-none-any.whl (129 kB)
Using cached blinker-1.9.0-py3-none-any.whl (8.5 kB)
Using cached certifi-2025.10.5-py3-none-any.whl (163 kB)
Using cached click-8.3.0-py3-none-any.whl (107 kB)
Using cached itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Using cached jinja2-3.1.6-py3-none-any.whl (134 kB)
Using cached markupsafe-3.0.3-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
Using cached werkzeug-3.1.3-py3-none-any.whl (224 kB)
Using cached packaging-25.0-py3-none-any.whl (66 kB)
Installing collected packages: urllib3, python-dotenv, packaging, mysqlclient, MarkupSafe, itsdangerous, idna, click, charset-normalizer, certifi, blinker, Werkzeug, requests, Jinja2, gunicorn, Flask, flask-mysqldb, flask-cors
Successfully installed Flask-2.3.2 Jinja2-3.1.6 MarkupSafe-3.0.3 Werkzeug-3.1.3 blinker-1.9.0 certifi-2025.10.5 charset-normalizer-3.4.4 click-8.3.0 flask-cors-6.0.1 flask-mysqldb-1.0.1 gunicorn-21.2.0 idna-3.11 itsdangerous-2.2.0 mysqlclient-2.2.7 packaging-25.0 python-dotenv-1.0.0 requests-2.31.0 urllib3-2.5.0
[notice] A new release of pip is available: 25.1.1 -> 25.3
[notice] To update, run: pip install --upgrade pip
==> Uploading build...
==> Uploaded in 10.1s. Compression took 2.8s
==> Build successful 🎉
==> Deploying...
==> Running 'gunicorn app:app'
[2025-11-01 08:15:21 +0000] [56] [INFO] Starting gunicorn 21.2.0
[2025-11-01 08:15:21 +0000] [56] [INFO] Listening at: http://0.0.0.0:10000 (56)
[2025-11-01 08:15:21 +0000] [56] [INFO] Using worker: sync
[2025-11-01 08:15:21 +0000] [57] [INFO] Booting worker with pid: 57
Loaded host: bdp9b506gpen6irxyh0q-mysql.services.clever-cloud.com
Loaded host: bdp9b506gpen6irxyh0q-mysql.services.clever-cloud.com
127.0.0.1 - - [01/Nov/2025:08:15:21 +0000] "HEAD / HTTP/1.1" 302 0 "-" "Go-http-client/1.1"
==> Your service is live 🎉
==> 
==> ///////////////////////////////////////////////////////////
==> 
==> Available at your primary URL https://my-packing-buddy.onrender.com
==> 
==> ///////////////////////////////////////////////////////////
127.0.0.1 - - [01/Nov/2025:08:15:24 +0000] "GET / HTTP/1.1" 302 199 "-" "Go-http-client/2.0"
127.0.0.1 - - [01/Nov/2025:08:15:24 +0000] "GET /login HTTP/1.1" 200 1956 "https://my-packing-buddy.onrender.com" "Go-http-client/2.0"
127.0.0.1 - - [01/Nov/2025:08:17:10 +0000] "GET / HTTP/1.1" 302 199 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:17:10 +0000] "GET /login HTTP/1.1" 200 1956 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:17:11 +0000] "GET /favicon.ico HTTP/1.1" 404 207 "https://my-packing-buddy.onrender.com/login" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:17:14 +0000] "GET /signup HTTP/1.1" 200 3215 "https://my-packing-buddy.onrender.com/login" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:18:40 +0000] "POST /signup HTTP/1.1" 302 199 "https://my-packing-buddy.onrender.com/signup" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:18:41 +0000] "GET /login HTTP/1.1" 200 2173 "https://my-packing-buddy.onrender.com/signup" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:18:44 +0000] "GET /login HTTP/1.1" 200 1956 "https://www.google.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:19:03 +0000] "POST /login HTTP/1.1" 302 197 "https://my-packing-buddy.onrender.com/login" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:19:03 +0000] "GET /home HTTP/1.1" 200 4321 "https://my-packing-buddy.onrender.com/login" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:19:04 +0000] "GET /static/home.jpg HTTP/1.1" 200 0 "https://my-packing-buddy.onrender.com/home" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:19:23 +0000] "GET /destination HTTP/1.1" 200 18638 "https://my-packing-buddy.onrender.com/home" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:19:24 +0000] "GET /static/wallpaper-doodle.png HTTP/1.1" 200 0 "https://my-packing-buddy.onrender.com/destination" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
==> Detected service running on port 10000
==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
[2025-11-01 08:20:29,131] ERROR in app: Exception on /books [GET]
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/render/project/src/app.py", line 34, in decorated_function
    return f(*args, **kwargs)
  File "/opt/render/project/src/app.py", line 157, in books
    return render_template('main/books.html')
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/jinja2/environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/jinja2/environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/jinja2/environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/jinja2/loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: main/books.html
127.0.0.1 - - [01/Nov/2025:08:20:29 +0000] "GET /books HTTP/1.1" 500 265 "https://my-packing-buddy.onrender.com/destination" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:34 +0000] "GET /saved_lists HTTP/1.1" 200 6408 "https://my-packing-buddy.onrender.com/destination" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:37 +0000] "GET /createcategory HTTP/1.1" 200 6201 "https://my-packing-buddy.onrender.com/saved_lists" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:39 +0000] "GET /about HTTP/1.1" 200 4851 "https://my-packing-buddy.onrender.com/createcategory" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:40 +0000] "GET /contact HTTP/1.1" 200 4567 "https://my-packing-buddy.onrender.com/about" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:44 +0000] "GET /logout HTTP/1.1" 302 199 "https://my-packing-buddy.onrender.com/contact" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:44 +0000] "GET /login HTTP/1.1" 200 2165 "https://my-packing-buddy.onrender.com/contact" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:49 +0000] "POST /login HTTP/1.1" 302 197 "https://my-packing-buddy.onrender.com/login" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:49 +0000] "GET /logout HTTP/1.1" 302 199 "https://www.google.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:49 +0000] "GET /home HTTP/1.1" 200 4321 "https://my-packing-buddy.onrender.com/login" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:49 +0000] "GET /login HTTP/1.1" 200 1956 "https://www.google.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:49 +0000] "GET /static/home.jpg HTTP/1.1" 304 0 "https://my-packing-buddy.onrender.com/home" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:54 +0000] "GET /destination HTTP/1.1" 200 18638 "https://my-packing-buddy.onrender.com/home" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
127.0.0.1 - - [01/Nov/2025:08:20:54 +0000] "GET /static/wallpaper-doodle.png HTTP/1.1" 304 0 "https://my-packing-buddy.onrender.com/destination" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
[2025-11-01 08:20:57,034] ERROR in app: Exception on /books [GET]
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/render/project/src/app.py", line 34, in decorated_function
    return f(*args, **kwargs)
  File "/opt/render/project/src/app.py", line 157, in books
    return render_template('main/books.html')
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/jinja2/environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/jinja2/environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/jinja2/environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/jinja2/loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.13/site-packages/flask/templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: main/books.html
127.0.0.1 - - [01/Nov/2025:08:20:57 +0000] "GET /books HTTP/1.1" 500 265 "https://my-packing-buddy.onrender.com/destination" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))

print("Loaded host:", os.getenv('MYSQL_HOST'))

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
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        app.logger.info(f"Received login form data: email={email}, password={'set' if password else 'not set'}")
        try:
            # Use DictCursor here
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
            account = cursor.fetchone()
            cursor.close()

            if account and check_password_hash(account['password'], password):
                session['user_id'] = account['id']
                session['username'] = account['name']
                return redirect(url_for('home'))
            else:
                flash("Incorrect email or password", "danger")

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
    return render_template('destination/books.html')

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









