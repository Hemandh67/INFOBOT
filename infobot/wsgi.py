import os

from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infobot.settings')

application = get_wsgi_application()

if 'VERCEL' in os.environ:
    # Run migrations when the serverless function starts
    # This prepares the in-memory SQLite database
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'createsuperuser', '--noinput', '--username', 'admin', '--email', 'admin@example.com'])
    # Need to set password for the auto-created superuser
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(username='admin')
        user.set_password('infobot123')
        user.save()
    except User.DoesNotExist:
        pass
