from __future__ import absolute_import

import os

from dotenv import load_dotenv

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(PROJECT_BASE_DIR, ".env"))
