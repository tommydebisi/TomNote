#!/usr/bin/env python3

from flask import render_template, request, session, redirect, url_for
from sqlalchemy.exc import InvalidRequestError
from views import app_notes
from auth.auth import AUTH


@app_notes.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """index method"""
    return render_template("login.html")


@app_notes.route("/login", methods=["POST"], strict_slashes=False)
def login() -> str:
    """index method"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session["email"] = email
        return redirect('/note/home')

    return render_template("login.html", error="Invalid username or password")


@app_notes.route("/register", methods=["GET"], strict_slashes=False)
def register() -> str:
    """register page"""
    return render_template("register.html")


@app_notes.route("/logout", methods=["GET"], strict_slashes=False)
def logout():
    """logout from home"""
    email = session.get("email")
    print(email)
    if email:
        session["email"] = None
    return redirect("/note")


@app_notes.route("/register", methods=["POST"], strict_slashes=False)
def check_and_register() -> str:
    """check and register user"""
    user_name = request.form.get("email")
    passwd = request.form.get("password")

    if not user_name or not passwd:
        return render_template(
            "register.html", user_error="Missing username or password"
        )
    try:
        AUTH.register_user(user_name, passwd)
    except ValueError:
        return render_template(
            "register.html", user_error="User already exists"
        )
    except InvalidRequestError:
        return render_template(
            "register.html", user_error="Something went wrong"
        )

    success = True
    return render_template("login.html", success=success)
