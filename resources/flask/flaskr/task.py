#!/usr/bin/env python3

from flask import Blueprint, request
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('task', __name__)
