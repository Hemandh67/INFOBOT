import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infobot.settings')
django.setup()

from django.contrib.auth.models import User

def create_users():
    users_to_add = [
        ('faculty1', 'faculty123', True), # username, password, is_staff
        ('faculty2', 'faculty123', True),
        ('student1', 'student123', False),
        ('student2', 'student123', False),
    ]

    for username, password, is_staff in users_to_add:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, f"{username}@example.com", password)
            user.is_staff = is_staff
            user.save()
            print(f"Created {'faculty' if is_staff else 'student'} user: {username}")
        else:
            u = User.objects.get(username=username)
            u.set_password(password)
            u.is_staff = is_staff
            u.save()
            print(f"Reset password for {username} to {password}")

if __name__ == '__main__':
    create_users()
