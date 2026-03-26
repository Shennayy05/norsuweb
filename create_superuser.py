import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'norsu_dashboard.settings')
django.setup()

from django.contrib.auth.models import User

# Delete existing users if they exist
User.objects.filter(username='superadmin').delete()
User.objects.filter(username='admin').delete()

# Create superadmin
superadmin = User.objects.create_user(
    username='superadmin',
    email='superadmin@norsu.edu.ph',
    password='admin123'
)
superadmin.is_superuser = True
superadmin.is_staff = True
superadmin.save()

# Create admin
admin = User.objects.create_user(
    username='admin',
    email='admin@norsu.edu.ph',
    password='admin123'
)
admin.is_superuser = True
admin.is_staff = True
admin.save()

print("=" * 50)
print("✓ Users created successfully!")
print("=" * 50)
print("Username: superadmin | Password: admin123")
print("Username: admin      | Password: admin123")
print("=" * 50)
print("You can now login at http://127.0.0.1:8000/super-admin-login/")
