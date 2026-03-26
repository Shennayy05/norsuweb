from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create/reset superadmin user'

    def handle(self, *args, **options):
        # Create/update superadmin user
        try:
            user = User.objects.get(username='superadmin')
            user.set_password('admin123')
            user.is_superuser = True
            user.is_staff = True
            user.email = 'superadmin@norsu.edu.ph'
            user.save()
            self.stdout.write(self.style.SUCCESS('✓ Superadmin password reset successfully!'))
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username='superadmin',
                email='superadmin@norsu.edu.ph',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superadmin created successfully!'))
        
        self.stdout.write(self.style.SUCCESS('Username: superadmin'))
        self.stdout.write(self.style.SUCCESS('Password: admin123'))
        
        # Also create/update admin user
        try:
            user2 = User.objects.get(username='admin')
            user2.set_password('admin123')
            user2.is_superuser = True
            user2.is_staff = True
            user2.save()
            self.stdout.write(self.style.SUCCESS('✓ Admin password also reset!'))
        except User.DoesNotExist:
            user2 = User.objects.create_superuser(
                username='admin',
                email='admin@norsu.edu.ph',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin user also created!'))
