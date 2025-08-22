#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def main():
    print("=== VERIFICATION DE LA CONFIGURATION DE PRODUCTION ===")
    print("=" * 60)
    
    # Charger les variables depuis railway.env
    env_file = Path("railway.env")
    if env_file.exists():
        print("Chargement des variables depuis railway.env...")
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print("Variables chargees avec succes")
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return False
    else:
        print("Fichier railway.env non trouve")
        return False
    
    # Verifier les variables critiques
    print("\nVerification des variables critiques...")
    critical_vars = ['SECRET_KEY', 'DEBUG', 'DB_ENGINE', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    issues = []
    
    for var in critical_vars:
        value = os.environ.get(var)
        if not value:
            issues.append(f"Variable {var} manquante")
            print(f"{var}: manquante")
        else:
            print(f"{var}: {'*' * len(value) if 'PASSWORD' in var else value}")
    
    # Verifier DEBUG
    debug_value = os.environ.get('DEBUG', 'True').lower()
    if debug_value == 'true':
        issues.append("DEBUG est active - DANGEREUX pour la production")
        print("DEBUG est active - DANGEREUX pour la production")
    else:
        print("DEBUG desactive")
    
    # Verifier la base de donnees
    db_engine = os.environ.get('DB_ENGINE', 'sqlite3')
    if db_engine == 'sqlite3':
        print("Utilisation de SQLite - PostgreSQL recommande pour la production")
    else:
        print("Base de donnees PostgreSQL configuree")
    
    # Verifier les fichiers de configuration
    print("\nVerification des fichiers de configuration...")
    config_files = ['railway.json', 'Procfile', 'requirements.txt']
    for file in config_files:
        if Path(file).exists():
            print(f"{file}: present")
        else:
            issues.append(f"{file} manquant")
            print(f"{file}: manquant")
    
    # Verifier la securite
    print("\nVerification de la securite...")
    security_vars = ['SECURE_SSL_REDIRECT', 'SECURE_HSTS_SECONDS', 'SECURE_CONTENT_TYPE_NOSNIFF', 'SECURE_BROWSER_XSS_FILTER']
    for var in security_vars:
        value = os.environ.get(var)
        if value:
            if var == 'SECURE_HSTS_SECONDS':
                try:
                    seconds = int(value)
                    if seconds > 0:
                        print(f"{var}: active ({seconds} secondes)")
                    else:
                        print(f"{var}: configure mais valeur invalide: {value}")
                except ValueError:
                    print(f"{var}: configure mais valeur non numerique: {value}")
            elif value.lower() == 'true':
                print(f"{var}: active")
            else:
                print(f"{var}: configure: {value}")
        else:
            print(f"{var}: non configure")
    
    # Resume
    print("\n" + "=" * 60)
    print("RESUME DE LA VERIFICATION")
    print("=" * 60)
    
    if issues:
        print(f"\nPROBLEMES CRITIQUES ({len(issues)}):")
        for issue in issues:
            print(f"  {issue}")
        print("\nConfiguration N'EST PAS prete pour la production!")
        return False
    else:
        print("\nConfiguration prete pour la production!")
        print("Pret pour le deploiement sur Railway!")
        return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)
