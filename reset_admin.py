#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'norsu_dashboard.settings')
    
    import django
    django.setup()
    
    from django.contrib.auth.models import User
    
    try:
        # Try to get existing admin user
        user = User.objects.get(username='admin')
        user.set_password('admin123')
        user.is_superuser = True
        user.is_staff = True
        user.email = 'admin@norsu.edu.ph'
        user.save()
        print("✓ Password reset successfully!")
        print("Username: admin")
        print("Password: admin123")
    except User.DoesNotExist:
        # Create new admin user
        user = User.objects.create_superuser(
            username='admin',
            email='admin@norsu.edu.ph',
            password='admin123'
        )
        print("✓ Superuser created successfully!")
        print("Username: admin")
        print("Password: admin123")
