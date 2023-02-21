#!/usr/bin/env python3
"""
    models module
"""
from models.engine.db import DB

storage = DB()
storage.reload()
