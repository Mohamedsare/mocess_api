#!/usr/bin/env python3
"""
Script de test pour vérifier la gestion de la variable PORT
"""

import os
import sys

def test_port_handling():
    print("=== TEST DE GESTION DE LA VARIABLE PORT ===")
    print("=" * 50)
    
    # Test 1: Variable PORT non définie
    print("\n🔍 Test 1: PORT non définie")
    if 'PORT' in os.environ:
        del os.environ['PORT']
    
    port = os.environ.get('PORT', '8000')
    print(f"   PORT récupéré: {port}")
    
    # Test 2: Variable PORT définie avec une valeur valide
    print("\n🔍 Test 2: PORT valide")
    os.environ['PORT'] = '5000'
    port = os.environ.get('PORT', '8000')
    print(f"   PORT récupéré: {port}")
    
    # Test 3: Variable PORT définie avec une valeur invalide
    print("\n🔍 Test 3: PORT invalide")
    os.environ['PORT'] = 'invalid'
    port = os.environ.get('PORT', '8000')
    print(f"   PORT récupéré: {port}")
    
    # Test 4: Variable PORT définie avec une valeur hors limites
    print("\n🔍 Test 4: PORT hors limites")
    os.environ['PORT'] = '99999'
    port = os.environ.get('PORT', '8000')
    print(f"   PORT récupéré: {port}")
    
    # Test 5: Validation du port
    print("\n🔍 Test 5: Validation du port")
    def validate_port(port_str):
        try:
            port_int = int(port_str)
            if 1 <= port_int <= 65535:
                return True, port_int
            else:
                return False, port_int
        except ValueError:
            return False, None
    
    test_ports = ['8000', '5000', 'invalid', '99999', '0', '-1']
    for test_port in test_ports:
        is_valid, port_int = validate_port(test_port)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {test_port} -> {port_int}")
    
    print("\n" + "=" * 50)
    print("🎉 Test de gestion du port terminé !")
    return True

if __name__ == "__main__":
    try:
        success = test_port_handling()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        sys.exit(1)
