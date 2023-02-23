#!/usr/bin/env python3

from flask import Blueprint

app_notes = Blueprint(
    "app_notes",
    __name__,
)

from views.notes import *
from views.session import *
