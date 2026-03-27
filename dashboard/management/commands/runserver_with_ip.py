import socket
import subprocess
import platform
from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line


class Command(BaseCommand):
    help = 'Run development server and display network access information'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noreload',
            action='store_false',
            dest='use_reloader',
            default=True,
            help='Tells Django to NOT use the auto-reloader.',
        )

    def handle(self, *args, **options):
        # Get and display network information
        self.get_network_info()
        
        # Start the development server
        use_reloader = options['use_reloader']
        
        # Execute the original runserver command
        runserver_args = ['runserver', '0.0.0.0:8000']
        if not use_reloader:
            runserver_args.append('--noreload')
        
        # Execute the original runserver command
        execute_from_command_line(['manage.py'] + runserver_args)

    def get_network_info(self):
        """Display network access information"""
        try:
            # Get local IP address
            local_ip = self.get_local_ip()
            
            # Display information
            self.stdout.write(self.style.SUCCESS('🌐 NORSU Development Server Started'))
            self.stdout.write(self.style.SUCCESS('=' * 50))
            self.stdout.write(self.style.SUCCESS(f'📱 Local Access: http://127.0.0.1:8000'))
            self.stdout.write(self.style.SUCCESS(f'🌍 Network Access: http://{local_ip}:8000'))
            self.stdout.write(self.style.SUCCESS('=' * 50))
            self.stdout.write(self.style.WARNING('📝 Other devices on same network can use the Network Access URL'))
            self.stdout.write(self.style.WARNING('💡 Your laptop can always use Local Access URL'))
            self.stdout.write('')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Could not determine network info: {e}'))
            self.stdout.write(self.style.WARNING('Falling back to: http://127.0.0.1:8000'))

    def get_local_ip(self):
        """Get the local IP address"""
        try:
            # Method 1: Connect to external address (most reliable)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            
            # Verify it's a local network IP
            if local_ip.startswith('192.168.') or local_ip.startswith('10.') or local_ip.startswith('172.'):
                return local_ip
                
        except:
            pass
        
        try:
            # Method 2: Get hostname and resolve (fallback)
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            if not local_ip.startswith('127.') and not local_ip.startswith('169.254'):
                return local_ip
                
        except:
            pass
        
        # Method 3: Use ipconfig command (Windows fallback)
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'IPv4 Address' in line and '192.168.' in line:
                        ip = line.split(':')[-1].strip()
                        return ip
        except:
            pass
        
        return '127.0.0.1'  # Ultimate fallback
