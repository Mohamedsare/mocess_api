#!/usr/bin/env python
"""
Script pour corriger l'encodage du fichier de sauvegarde
"""

import json
from pathlib import Path

def fix_encoding():
    """Corriger l'encodage du fichier de sauvegarde"""
    print("🔧 Correction de l'encodage du fichier de sauvegarde...")
    
    backup_file = Path("api_data.json")
    if not backup_file.exists():
        print("❌ Fichier de sauvegarde non trouvé")
        return False
    
    try:
        # Essayer de lire avec différents encodages
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                print(f"🔄 Tentative avec l'encodage: {encoding}")
                with open(backup_file, 'r', encoding=encoding) as f:
                    data = json.load(f)
                
                # Réécrire avec l'encodage UTF-8 correct
                with open("api_data_fixed.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ Encodage corrigé avec succès (encodage source: {encoding})")
                return True
                
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError as e:
                print(f"❌ Erreur JSON avec {encoding}: {e}")
                continue
        
        print("❌ Impossible de corriger l'encodage")
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

if __name__ == '__main__':
    if fix_encoding():
        print("\n📋 Prochaines étapes:")
        print("1. Exécuter: python manage.py loaddata api_data_fixed.json")
        print("2. Tester l'application")
    else:
        print("\n❌ Échec de la correction de l'encodage")
