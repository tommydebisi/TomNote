#!/usr/bin/env python3
"""
    app module
"""
from flask import Flask, render_template, request, session, redirect, url_for
from flask_cors import CORS
from auth.auth import Auth
from models.user import User
import models


app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = "secret"
CORS(app, resources={r"*": {"origins": "*"}})
AUTH = Auth()


@app.teardown_appcontext
def teardown(exception):
    """ teardown """
    models.storage.close()

@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ index method """
    return render_template('login.html')


@app.route('/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ index method """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session['email'] = email
        return redirect('/home')

    return render_template('login.html', error="Invalid username or password")


@app.route('/register', methods=['GET'], strict_slashes=False)
def register() -> str:
    """ register page """
    return render_template('register.html')


@app.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """ logout from home """
    return redirect('/')


@app.route('/register', methods=['POST'], strict_slashes=False)
def check_and_register() -> str:
    """ check and register user """
    user_name = request.form.get('email')
    passwd = request.form.get('password')

    if not user_name or not passwd:
        return render_template('register.html', user_error="Missing username or password")
    try:
        AUTH.register_user(user_name, passwd)
    except ValueError:
        return render_template('register.html', user_error="User already exists")
    except Exception:
        return render_template('register.html', user_error="Something went wrong")

    success = True
    return render_template('login.html', success=success)


@app.route('/home', methods=['GET', 'POST'], strict_slashes=False)
def home() -> str:
    """ home page """
    if request.method == 'GET':
        if 'email' not in session:
            return redirect('/')

        user = AUTH.get_user_from_email(session['email'])
        return render_template('home.html', user=user, notes=user.notes)
    if request.method == 'POST':
        if 'email' not in session:
            return redirect('/')

        user = AUTH.get_user_from_email(session['email'])
        title = request.form.get('title')
        content = request.form.get('content')

        if not session.get('note_id'):
            AUTH.create_and_save_note(user, title, content)
        else:
            AUTH.update_and_save_note(user, session['note_id'], title, content)
            session['note_id'] = None

        return render_template('home.html', user=user, notes=user.notes)


@app.route('/delete/<note_id>', methods=['GET'], strict_slashes=False)
def delete(note_id) -> str:
    """ delete note """
    if 'email' not in session:
        return redirect('/')

    user = AUTH.get_user_from_email(session['email'])

    AUTH.delete_note_by_id(user, note_id)

    return redirect(url_for('home'))


@app.route('/update/<note_id>', methods=['GET'], strict_slashes=False)
def update(note_id) -> str:
    """ update note """
    if 'email' not in session:
        return redirect('/')

    user = AUTH.get_user_from_email(session['email'])

    note = AUTH.get_note_by_id(user, note_id)
    session['note_id'] = note_id

    return render_template('home.html', user=user, notes=user.notes,
                           title=note.title, content=note.content, update=True)


if __name__ == "__main__":
    app.run('0.0.0.0', 5000)
