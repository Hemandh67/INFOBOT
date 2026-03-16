import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infobot.settings')
django.setup()

from django.contrib.auth.models import User

users = User.objects.all()
for u in users:
    print(f"User: {u.username}, is_superuser: {u.is_superuser}")

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Created superuser admin with password admin")
else:
    u = User.objects.get(username='admin')
    u.set_password('admin')
    u.save()
    print("Reset password for superuser admin to 'admin'")
