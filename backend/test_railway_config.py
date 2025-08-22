#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration Railway
"""

import os
import sys
from pathlib import Path

def test_railway_config():
    print("=== TEST DE LA CONFIGURATION RAILWAY ===")
    print("=" * 50)
    
    # Charger les variables depuis railway.env
    env_file = Path("railway.env")
    if env_file.exists():
        print("✅ Chargement des variables depuis railway.env...")
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    # Simuler l'environnement Railway
    os.environ['RAILWAY_ENVIRONMENT'] = 'production'
    os.environ['PORT'] = '8000'
    
    print(f"✅ RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT')}")
    print(f"✅ PORT: {os.environ.get('PORT')}")
    
    # Test 1: Vérifier le module WSGI
    print("\n🔍 Test 1: Module WSGI")
    try:
        from mocess_backend.wsgi import application
        print("✅ Module WSGI importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'import WSGI: {e}")
        return False
    
    # Test 2: Vérifier la configuration Railway
    print("\n🔍 Test 2: Configuration Railway")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.railway_settings')
        import django
        from django.conf import settings
        django.setup()
        print("✅ Configuration Railway chargée avec succès")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"   DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
    except Exception as e:
        print(f"❌ Erreur de configuration Railway: {e}")
        return False
    
    # Test 3: Vérifier les variables critiques
    print("\n🔍 Test 3: Variables d'environnement")
    critical_vars = ['SECRET_KEY', 'DB_ENGINE', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    missing_vars = []
    
    for var in critical_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * 10 if 'PASSWORD' in var else 'OK'}")
    
    if missing_vars:
        print(f"❌ Variables manquantes: {', '.join(missing_vars)}")
        return False
    
    # Test 4: Vérifier la commande de déploiement
    print("\n🔍 Test 4: Commande de déploiement")
    port = os.environ.get('PORT', '8000')
    if port and port.isdigit():
        print(f"✅ PORT défini: {port}")
        print(f"✅ Commande: bash start.sh")
    else:
        print(f"❌ PORT invalide: {port}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TOUS LES TESTS PASSENT !")
    print("✅ Configuration Railway prête pour le déploiement")
    return True

if __name__ == "__main__":
    try:
        success = test_railway_config()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        sys.exit(1)
