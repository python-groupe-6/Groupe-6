import os
import django
from django.contrib.auth import get_user_model

# Setup Django environment
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eduquiz_project.settings")
django.setup()

User = get_user_model()
username = "admin"
email = "admin@example.com"
password = "admin"

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    User.objects.create_superuser(username, email, password)
    print("Superuser created successfully.")
else:
    print(f"Superuser '{username}' already exists.")
