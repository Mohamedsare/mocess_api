# Backend Mocess

Backend Django pour l'application Mocess, configuré pour le déploiement sur Railway.

## Structure du Projet

```
backend/
├── api/                    # API Django REST Framework
├── mocess_backend/         # Configuration principale Django
├── templates/              # Templates HTML
├── static/                 # Fichiers statiques
├── media/                  # Fichiers média uploadés
├── logs/                   # Fichiers de logs
├── scripts/                # Scripts utilitaires
├── venv/                   # Environnement virtuel Python
├── check_production.py     # Script de vérification complète
├── check_quick.py          # Script de vérification rapide
├── railway.env.example     # Exemple de variables d'environnement
├── railway.env             # Variables d'environnement Railway (à créer)
├── railway.json            # Configuration Railway
├── Procfile                # Configuration de déploiement
├── requirements.txt        # Dépendances Python
├── manage.py               # Gestionnaire Django
└── .gitignore             # Fichiers à ignorer par Git
```

## Prérequis

- Python 3.8+
- PostgreSQL (pour la production)
- Railway CLI (pour le déploiement)

## Installation

1. **Cloner le projet et accéder au dossier backend :**
   ```bash
   cd backend
   ```

2. **Créer un environnement virtuel :**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel :**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurer les variables d'environnement :**
   ```bash
   # Copier le fichier d'exemple
   copy railway.env.example railway.env
   
   # Modifier les valeurs dans railway.env selon votre configuration
   ```

## Développement Local

1. **Démarrer le serveur de développement :**
   ```bash
   python manage.py runserver
   ```

2. **Créer et appliquer les migrations :**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Créer un superutilisateur :**
   ```bash
   python manage.py createsuperuser
   ```

## Vérification de la Configuration

### Vérification Complète
```bash
python check_production.py
```

### Vérification Rapide
```bash
python check_quick.py
```

## Déploiement sur Railway

1. **Vérifier la configuration :**
   ```bash
   python check_production.py
   ```

2. **Déployer :**
   ```bash
   railway up
   ```

## Configuration de Production

Le projet est configuré pour la production avec :
- Base de données PostgreSQL
- Variables d'environnement sécurisées
- Paramètres de sécurité activés (HTTPS, HSTS, etc.)
- Configuration Railway optimisée

## Support

Pour plus d'informations sur la vérification de la configuration, consultez [README_VERIFICATION.md](README_VERIFICATION.md).

## Notes Importantes

- **Ne jamais commiter** le fichier `railway.env` dans Git (il contient des secrets)
- Le fichier `db.sqlite3` est automatiquement créé par Django en développement local
- Utilisez `railway.env.example` comme modèle pour créer votre propre `railway.env`
