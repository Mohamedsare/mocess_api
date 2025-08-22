"""
Configuration Django spécifique pour Railway
Ce fichier étend les settings.py avec des configurations spécifiques à Railway
"""

import os
from .settings import *

# Configuration spécifique Railway
RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT', 'production')

# Gestion robuste du port
PORT = os.environ.get('PORT', '8000')
if not PORT.isdigit() or int(PORT) < 1 or int(PORT) > 65535:
    PORT = '8000'

print(f"🚀 Configuration Railway - Port: {PORT}")

# Configuration de la base de données Railway
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ['DATABASE_URL'],
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    
    # Forcer SSL pour Railway PostgreSQL
    if 'postgresql' in os.environ['DATABASE_URL']:
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require'
        }
        print("✅ Base de données PostgreSQL Railway configurée avec SSL")

# Configuration des domaines autorisés pour Railway
if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
    railway_domain = os.environ['RAILWAY_PUBLIC_DOMAIN']
    if railway_domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(railway_domain)
        print(f"✅ Domaine Railway ajouté: {railway_domain}")

if os.environ.get('RAILWAY_STATIC_URL'):
    railway_static = os.environ['RAILWAY_STATIC_URL'].replace('https://', '').replace('http://', '')
    if railway_static not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(railway_static)
        print(f"✅ Domaine statique Railway ajouté: {railway_static}")

# Configuration de sécurité pour Railway
if RAILWAY_ENVIRONMENT == 'production':
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    print("✅ Configuration de sécurité Railway activée")

# Configuration des fichiers statiques pour Railway
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Middleware WhiteNoise pour Railway
if not DEBUG:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    print("✅ WhiteNoise configuré pour Railway")

print(f"✅ Configuration Railway terminée - Environnement: {RAILWAY_ENVIRONMENT}")
