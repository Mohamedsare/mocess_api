#!/usr/bin/env python
"""
Script pour ajouter les données de test des statistiques dans le backend
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Statistic

def add_test_statistics():
    """Ajoute les données de test des statistiques"""
    
    # Supprimer les anciennes données de test si elles existent
    Statistic.objects.filter(title__in=[
        'Projets réalisés',
        'Chercheurs & experts impliqués', 
        'Partenaires nationaux & internationaux'
    ]).delete()
    
    # Données de test
    test_statistics = [
        {
            'title': 'Projets réalisés',
            'value': '5',
            'description': 'Projets de recherche en eau, agriculture, biodiversité',
            'icon': 'award',
            'color': 'blue',
            'is_active': True,
            'order': 1
        },
        {
            'title': 'Chercheurs & experts impliqués',
            'value': '40',
            'description': 'Collaborateurs académiques et techniques',
            'icon': 'users',
            'color': 'purple',
            'is_active': True,
            'order': 2
        },
        {
            'title': 'Partenaires nationaux & internationaux',
            'value': '20',
            'description': 'Institutions partenaires (universités, ONG, collectivités)',
            'icon': 'building',
            'color': 'orange',
            'is_active': True,
            'order': 3
        }
    ]
    
    # Créer les statistiques
    for stat_data in test_statistics:
        Statistic.objects.create(**stat_data)
        print(f"✅ Statistique ajoutée: {stat_data['title']} = {stat_data['value']}")
    
    print(f"\n🎉 {len(test_statistics)} statistiques de test ont été ajoutées dans le backend!")
    print("Vous pouvez maintenant les modifier depuis l'interface d'administration:")
    print("http://127.0.0.1:8000/admin/api/statistic/")

if __name__ == '__main__':
    add_test_statistics() 