"""
Context processors for global template context (e.g. SEO / site info).
"""
from django.conf import settings


def site_meta(request):
    return {
        'site_name': getattr(settings, 'SITE_NAME', 'Botir Bakhtiyarov'),
        'site_domain': getattr(settings, 'SITE_DOMAIN', 'bbotir.xyz'),
        'site_description': getattr(settings, 'SITE_DESCRIPTION', 'Backend Engineer | Django • APIs • AI-Powered Systems'),
    }
