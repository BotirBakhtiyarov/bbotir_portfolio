"""
Custom admin site with improved 2FA flow:
1. Username/password login
2. If first time: show QR code for setup
3. If not first time: ask for 6-digit OTP code
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
import qrcode
from io import BytesIO
import base64


class CustomOTPAdminSite(OTPAdminSite):
    """Custom admin site with improved 2FA flow."""
    
    login_template = 'admin/custom_login.html'
    
    def get_urls(self):
        """Add custom URLs for 2FA setup and verification."""
        from django.urls import path
        urls = super().get_urls()
        
        custom_urls = [
            path('setup-2fa/', self.setup_2fa_view, name='setup_2fa'),
            path('verify-otp/', self.verify_otp_view, name='verify_otp'),
        ]
        return custom_urls + urls
    
    @method_decorator(never_cache)
    def login(self, request, extra_context=None):
        """
        Custom login view:
        1. Show username/password form
        2. After login, check if user has confirmed TOTP device
        3. If no device: show QR code setup
        4. If device exists: show OTP verification
        """
        if request.method == 'GET':
            # If already logged in and verified, redirect to admin
            if request.user.is_authenticated and request.user.is_verified():
                return redirect(self.index(request))
            # Show login form
            return super().login(request, extra_context)
        
        # POST: handle login
        # Call parent login to authenticate user
        response = super().login(request, extra_context)
        
        # After successful login, check for 2FA
        # The user should be authenticated at this point if login succeeded
        if request.user.is_authenticated:
            # Check if user has confirmed TOTP device
            has_confirmed_device = TOTPDevice.objects.filter(
                user=request.user,
                confirmed=True
            ).exists()
            
            if not has_confirmed_device:
                # First time: redirect to QR code setup
                return redirect('admin:setup_2fa')
            else:
                # Not first time: redirect to OTP verification
                return redirect('admin:verify_otp')
        
        # If login failed, return the response (which will show errors)
        return response
    
    def get_urls(self):
        """Add custom URLs for 2FA setup and verification."""
        urls = super().get_urls()
        from django.urls import path
        
        custom_urls = [
            path('setup-2fa/', self.setup_2fa_view, name='setup_2fa'),
            path('verify-otp/', self.verify_otp_view, name='verify_otp'),
        ]
        return custom_urls + urls
    
    @method_decorator(staff_member_required)
    @method_decorator(never_cache)
    def setup_2fa_view(self, request):
        """Show QR code for first-time 2FA setup."""
        # Check if already has confirmed device
        has_confirmed = TOTPDevice.objects.filter(
            user=request.user,
            confirmed=True
        ).exists()
        
        if has_confirmed:
            return redirect('admin:verify_otp')
        
        # Get or create TOTP device
        device, created = TOTPDevice.objects.get_or_create(
            user=request.user,
            name='default',
            defaults={'key': random_hex(20), 'confirmed': False}
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
        
        if request.method == 'POST':
            # Verify the code
            token = request.POST.get('token', '')
            if device.verify_token(token):
                device.confirmed = True
                device.save()
                return redirect(self.index(request))
            else:
                error = 'Invalid code. Please try again.'
        else:
            error = None
        
        context = {
            **self.each_context(request),
            'title': 'Set up Two-Factor Authentication',
            'device': device,
            'qr_data': qr_data,
            'config_url': config_url,
            'error': error,
        }
        return render(request, 'admin/setup_2fa.html', context)
    
    @method_decorator(staff_member_required)
    @method_decorator(never_cache)
    def verify_otp_view(self, request):
        """Verify OTP code for existing users."""
        # Check if user has confirmed device
        device = TOTPDevice.objects.filter(
            user=request.user,
            confirmed=True
        ).first()
        
        if not device:
            return redirect('admin:setup_2fa')
        
        # If already verified, redirect to admin
        if request.user.is_verified():
            return redirect(self.index(request))
        
        error = None
        if request.method == 'POST':
            token = request.POST.get('token', '')
            if device.verify_token(token):
                # Device verification handled by middleware
                return redirect(self.index(request))
            else:
                error = 'Invalid code. Please try again.'
        
        context = {
            **self.each_context(request),
            'title': 'Two-Factor Authentication',
            'device': device,
            'error': error,
        }
        return render(request, 'admin/verify_otp.html', context)


# Create custom admin site instance
admin_site = CustomOTPAdminSite(name='admin')
admin_site.site_header = 'bbotir.xyz Admin'
admin_site.site_title = 'Portfolio Admin'
