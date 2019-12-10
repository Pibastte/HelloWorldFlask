from flask import Flask, session, escape, request, render_template, redirect, url_for, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret
app.secret_key = b'_kibze##hozeuhez9876sofih'

@app.route('/')
def index():
    username = None
    if 'username' in session:
        username = escape(session['username'])
    return render_template('index.html', username=username)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    username = ""
    if request.method == 'POST':
        username = request.form['username']
        print("POST request on login")
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error, username=username)

def valid_login(username, password):
    if username != '' and password != '':
        return True
        print("true")
    return False

def log_the_user_in(username):
    print("user %s is logged in" % username)
    session['username'] = username
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/fileupload', methods=['POST', 'GET'])
def fileupload():
    error = None
    if request.method == 'POST':
        if len(request.files) != 0:
            f = request.files['file']
            f.save('./db/file_uploaded.' + secure_filename(f.filename).split('.')[-1])
            return redirect('/')
        else:
            error = "No file uploaded"
            
    return render_template('fileUpload.html', error=error)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404