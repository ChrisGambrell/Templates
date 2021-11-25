#!/usr/bin/env python3

from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

from . import login     # noqa: E402, F401
from . import register  # noqa: E402, F401
