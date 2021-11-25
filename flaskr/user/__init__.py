#!/usr/bin/env python3

from cerberus import Validator
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')
v = Validator(purge_unknown=True)

from . import delete_user       # noqa: E402, F401
from . import edit_user         # noqa: E402, F401
from . import get_user_by_id    # noqa: E402, F401
from . import get_user          # noqa: E402, F401
