#!/usr/bin/env python3
"""
    app module
"""
from flask import Flask
from flask_cors import CORS
# from auth.auth import Auth
from views import app_notes
import models


app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = "secret"
CORS(app, resources={r"*": {"origins": "*"}})
# AUTH = Auth()
app.register_blueprint(app_notes)


@app.teardown_appcontext
def teardown(exception):
    """teardown"""
    models.storage.close()


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
