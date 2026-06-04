import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Worker
from django.contrib.auth.models import User

Worker.objects.all().delete()
User.objects.filter(is_superuser=False).delete()
print("Cleared workers.")
