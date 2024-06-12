import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "budget_tracker.settings")
application = get_wsgi_application()

with open("dump_data/data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", "planner", "auth", indent=4, stdout=f)
