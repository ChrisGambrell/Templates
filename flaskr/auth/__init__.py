#!/usr/bin/env python3

from cerberus import Validator
from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')
v = Validator(purge_unknown=True, require_all=True)

from . import login     # noqa: E402, F401
from . import register  # noqa: E402, F401
