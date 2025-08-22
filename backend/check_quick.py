#!/usr/bin/env python3
import os
import sys
from pathlib import Path

print("=== VERIFICATION RAPIDE DE LA CONFIGURATION ===")

# Charger les variables
env_file = Path("railway.env")
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Verifier les elements critiques
issues = []
critical_vars = ['SECRET_KEY', 'DEBUG', 'DB_ENGINE', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']

for var in critical_vars:
    if not os.environ.get(var):
        issues.append(f"Variable {var} manquante")

# Verifier DEBUG
if os.environ.get('DEBUG', 'True').lower() == 'true':
    issues.append("DEBUG est active - DANGEREUX pour la production")

# Verifier les fichiers
config_files = ['railway.json', 'Procfile', 'requirements.txt']
for file in config_files:
    if not Path(file).exists():
        issues.append(f"{file} manquant")

# Resume
if issues:
    print(f"\nPROBLEMES CRITIQUES ({len(issues)}):")
    for issue in issues:
        print(f"  {issue}")
    print("\nConfiguration N'EST PAS prete pour la production!")
    sys.exit(1)
else:
    print("\nConfiguration 100% prete pour la production!")
    print("Pret pour le deploiement sur Railway!")
    sys.exit(0)
