"""
Management command to set up 2FA for a user.
Usage: python manage.py setup_2fa <username>
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import base64

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up 2FA TOTP device for a user and display QR code'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to set up 2FA for')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" not found.'))
            return

        # Check if device already exists
        existing_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if existing_device:
            self.stdout.write(self.style.WARNING(
                f'User "{username}" already has a confirmed TOTP device named "{existing_device.name}".'
            ))
            self.stdout.write('To create a new device, delete the existing one first or use a different name.')
            return

        # Create new TOTP device
        device = TOTPDevice.objects.create(
            user=user,
            name='default',
            confirmed=False,
            key=random_hex(20)
        )

        # Generate QR code
        config_url = device.config_url
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(config_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_data = base64.b64encode(buffer.getvalue()).decode()

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('2FA Setup for user: ' + username))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
        
        self.stdout.write('1. Open Google Authenticator (or any TOTP app) on your phone')
        self.stdout.write('2. Tap "+" → "Scan QR code"')
        self.stdout.write('3. Scan the QR code below:\n')
        
        # Display QR code as ASCII art (simple version)
        self.stdout.write('QR Code URL (if you need to enter manually):')
        self.stdout.write(self.style.WARNING(config_url))
        self.stdout.write('\n')
        
        # Try to save QR code to file
        try:
            qr_path = f'qr_code_{username}.png'
            with open(qr_path, 'wb') as f:
                f.write(buffer.getvalue())
            self.stdout.write(self.style.SUCCESS(f'QR code saved to: {qr_path}'))
            self.stdout.write(f'  Open this file and scan it with Google Authenticator\n')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Could not save QR code file: {e}'))
        
        self.stdout.write('\n4. After scanning, go to: http://127.0.0.1:8000/admin/')
        self.stdout.write('5. Log in with your username and password')
        self.stdout.write('6. Enter the 6-digit code from Google Authenticator')
        self.stdout.write('7. The device will be confirmed automatically\n')
        
        self.stdout.write(self.style.SUCCESS('Setup complete! Your device is ready to use.\n'))
