#!/usr/bin/env python3
"""
Script de test pour simuler le déploiement Railway
"""

import os
import sys
from pathlib import Path

def test_deployment():
    print("=== TEST DE DEPLOIEMENT RAILWAY ===")
    print("=" * 50)
    
    # Charger les variables d'environnement
    env_file = Path("railway.env")
    if env_file.exists():
        print("✅ Chargement des variables depuis railway.env...")
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    # Simuler la variable PORT de Railway
    os.environ['PORT'] = '8000'
    os.environ['RAILWAY_ENVIRONMENT'] = 'production'
    
    # Test 1: Vérifier le module WSGI
    print("\n🔍 Test 1: Module WSGI")
    try:
        from mocess_backend.wsgi import application
        print("✅ Module WSGI importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'import WSGI: {e}")
        return False
    
    # Test 2: Vérifier les settings Django
    print("\n🔍 Test 2: Configuration Django")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mocess_backend.settings')
        import django
        from django.conf import settings
        django.setup()
        print("✅ Django configuré avec succès")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"   DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False
    
    # Test 3: Vérifier les variables d'environnement critiques
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
        print(f"✅ Commande: gunicorn mocess_backend.wsgi:application --bind 0.0.0.0:{port}")
    else:
        print(f"❌ PORT invalide: {port}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TOUS LES TESTS PASSENT !")
    print("✅ Prêt pour le déploiement sur Railway")
    return True

if __name__ == "__main__":
    try:
        success = test_deployment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        sys.exit(1)
