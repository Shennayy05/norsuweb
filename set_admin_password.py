import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'norsu_dashboard.settings')
django.setup()

from django.contrib.auth.models import User

# Get or create admin user
try:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Password set successfully for user 'admin'")
    print("Username: admin")
    print("Password: admin123")
except User.DoesNotExist:
    user = User.objects.create_superuser('admin', 'admin@norsu.edu.ph', 'admin123')
    print("Superuser created successfully!")
    print("Username: admin")
    print("Password: admin123")
