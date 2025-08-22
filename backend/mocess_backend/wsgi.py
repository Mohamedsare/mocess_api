"""
WSGI config for mocess_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Utiliser la configuration Railway en production
if os.environ.get('RAILWAY_ENVIRONMENT') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.railway_settings')
    print("🚀 Configuration Railway détectée")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.settings')
    print("🔧 Configuration locale détectée")

application = get_wsgi_application()
