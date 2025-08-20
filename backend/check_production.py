#!/usr/bin/env python3
"""
Script de vérification de la configuration de production
Vérifie que tous les paramètres de sécurité sont correctement configurés
"""

import os
import sys
from pathlib import Path

def check_production_ready():
    """Vérifie si la configuration est prête pour la production"""
    print("🔍 Vérification de la configuration de production...")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Vérification des variables critiques
    critical_vars = [
        'SECRET_KEY',
        'DEBUG',
        'DB_ENGINE',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT'
    ]
    
    for var in critical_vars:
        value = os.environ.get(var)
        if not value:
            issues.append(f"❌ Variable {var} manquante")
        else:
            print(f"✅ {var}: {'*' * len(value) if 'PASSWORD' in var else value}")
    
    # Vérification de DEBUG
    debug_value = os.environ.get('DEBUG', 'True').lower()
    if debug_value == 'true':
        issues.append("❌ DEBUG est activé - DANGEREUX pour la production")
    else:
        print("✅ DEBUG désactivé")
    
    # Vérification de la base de données
    db_engine = os.environ.get('DB_ENGINE', 'sqlite3')
    if db_engine == 'sqlite3':
        warnings.append("⚠️ Utilisation de SQLite - PostgreSQL recommandé pour la production")
    else:
        print("✅ Base de données PostgreSQL configurée")
    
    # Vérification des fichiers de configuration
    config_files = [
        'railway.json',
        'Procfile',
        'requirements.txt'
    ]
    
    for file in config_files:
        if Path(file).exists():
            print(f"✅ {file} présent")
        else:
            issues.append(f"❌ {file} manquant")
    
    # Vérification de la sécurité
    security_vars = [
        'SECURE_SSL_REDIRECT',
        'SECURE_HSTS_SECONDS',
        'SECURE_CONTENT_TYPE_NOSNIFF',
        'SECURE_BROWSER_XSS_FILTER'
    ]
    
    for var in security_vars:
        value = os.environ.get(var)
        if value and value.lower() == 'true':
            print(f"✅ {var} activé")
        else:
            warnings.append(f"⚠️ {var} non configuré")
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 50)
    
    if issues:
        print(f"\n❌ PROBLÈMES CRITIQUES ({len(issues)}):")
        for issue in issues:
            print(f"  {issue}")
        print("\n🚨 La configuration N'EST PAS prête pour la production !")
        return False
    
    if warnings:
        print(f"\n⚠️ AVERTISSEMENTS ({len(warnings)}):")
        for warning in warnings:
            print(f"  {warning}")
        print("\n⚠️ La configuration peut être améliorée")
    
    if not issues and not warnings:
        print("\n🎉 Configuration 100% prête pour la production !")
    elif not issues:
        print("\n✅ Configuration prête pour la production avec quelques améliorations possibles")
    
    return len(issues) == 0

if __name__ == "__main__":
    try:
        # Charger les variables d'environnement depuis railway.env
        env_file = Path("railway.env")
        if env_file.exists():
            print("📁 Chargement des variables depuis railway.env...")
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print("✅ Variables d'environnement chargées")
        else:
            print("⚠️ Fichier railway.env non trouvé")
        
        # Vérifier la configuration
        is_ready = check_production_ready()
        
        if is_ready:
            print("\n🚀 Prêt pour le déploiement sur Railway !")
            sys.exit(0)
        else:
            print("\n🔧 Veuillez corriger les problèmes avant le déploiement")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        sys.exit(1)
