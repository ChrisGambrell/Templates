#!/usr/bin/env python3

from flask import Blueprint

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

from . import create_task       # noqa: E402, F401
from . import delete_task       # noqa: E402, F401
from . import edit_task         # noqa: E402, F401
from . import get_task_by_id    # noqa: E402, F401
from . import get_tasks         # noqa: E402, F401
