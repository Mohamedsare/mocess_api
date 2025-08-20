# Guide de Migration SQLite vers PostgreSQL

Ce guide vous accompagne dans la migration de votre base de données SQLite vers PostgreSQL pour la production.

## 📋 Prérequis

### 1. Installation de PostgreSQL

#### Sur Windows :
```bash
# Télécharger et installer depuis https://www.postgresql.org/download/windows/
# Ou utiliser Chocolatey :
choco install postgresql
```

#### Sur macOS :
```bash
# Avec Homebrew
brew install postgresql
brew services start postgresql
```

#### Sur Ubuntu/Debian :
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Création de la base de données PostgreSQL

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer l'utilisateur et la base de données
CREATE USER mocess_user WITH PASSWORD 'your-secure-password';
CREATE DATABASE mocess_db OWNER mocess_user;
GRANT ALL PRIVILEGES ON DATABASE mocess_db TO mocess_user;
\q
```

## 🔧 Configuration

### 1. Mettre à jour le fichier .env

Copiez le contenu de `env_example.txt` vers votre fichier `.env` et modifiez :

```bash
# Pour PostgreSQL
DB_ENGINE=postgresql
DB_NAME=mocess_db
DB_USER=mocess_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
```

### 2. Vérifier les dépendances

Assurez-vous que `psycopg2-binary` est installé :

```bash
pip install psycopg2-binary
```

## 🚀 Processus de Migration

### Étape 1 : Sauvegarde des données SQLite

```bash
# Aller dans le dossier backend
cd SiteMocess/backend

# Activer l'environnement virtuel
# Windows :
venv\Scripts\activate
# Linux/Mac :
source venv/bin/activate

# Exécuter le script de migration
python migrate_to_postgresql.py
```

### Étape 2 : Vérification de la migration

```bash
# Tester la connexion PostgreSQL
python manage.py dbshell

# Dans le shell PostgreSQL, vérifier les tables :
\dt

# Quitter le shell
\q
```

### Étape 3 : Test de l'application

```bash
# Démarrer le serveur de développement
python manage.py runserver

# Tester les fonctionnalités principales :
# - Accès à l'admin Django
# - API endpoints
# - Fonctionnalités de l'application
```

## 🔍 Vérifications Post-Migration

### 1. Vérifier les données

```bash
# Compter les enregistrements dans chaque modèle
python manage.py shell

# Dans le shell Python :
from api.models import *
print(f"Categories: {Category.objects.count()}")
print(f"Projects: {Project.objects.count()}")
print(f"News: {News.objects.count()}")
print(f"Team Members: {TeamMember.objects.count()}")
# ... etc pour tous les modèles
```

### 2. Vérifier les fichiers média

```bash
# S'assurer que tous les fichiers sont accessibles
python manage.py collectstatic
```

### 3. Test des fonctionnalités

- [ ] Accès à l'interface d'administration
- [ ] Création/modification d'objets
- [ ] Upload de fichiers
- [ ] API endpoints
- [ ] Recherche et filtres

## 🛠️ Dépannage

### Problème de connexion PostgreSQL

```bash
# Vérifier que PostgreSQL fonctionne
sudo systemctl status postgresql

# Vérifier les logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### Problème de permissions

```bash
# Donner les permissions nécessaires
sudo -u postgres psql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mocess_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mocess_user;
\q
```

### Problème de migration des données

```bash
# Vérifier le fichier de sauvegarde
cat sqlite_backup.json

# Relancer la migration si nécessaire
python migrate_to_postgresql.py
```

## 🔄 Rollback (si nécessaire)

Si vous devez revenir à SQLite :

```bash
# 1. Modifier le fichier .env
DB_ENGINE=sqlite3

# 2. Supprimer les migrations PostgreSQL
python manage.py migrate api zero

# 3. Recréer les migrations SQLite
python manage.py makemigrations
python manage.py migrate

# 4. Restaurer les données depuis la sauvegarde
python restore_from_backup.py
```

## 📊 Optimisations PostgreSQL

### 1. Configuration de performance

```sql
-- Dans psql, optimiser les performances
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Redémarrer PostgreSQL
sudo systemctl restart postgresql
```

### 2. Index pour les performances

```bash
# Créer des index sur les champs fréquemment recherchés
python manage.py shell

# Dans le shell :
from django.db import connection
cursor = connection.cursor()

# Index sur les champs de recherche
cursor.execute("CREATE INDEX idx_project_title ON api_project(title);")
cursor.execute("CREATE INDEX idx_news_title ON api_news(title);")
cursor.execute("CREATE INDEX idx_publication_title ON api_publication(title);")
```

## 🔒 Sécurité

### 1. Configuration de sécurité PostgreSQL

```sql
-- Limiter les connexions
ALTER SYSTEM SET max_connections = 100;

-- Activer SSL
ALTER SYSTEM SET ssl = on;

-- Redémarrer PostgreSQL
sudo systemctl restart postgresql
```

### 2. Sauvegarde automatique

```bash
# Créer un script de sauvegarde
cat > backup_postgresql.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U mocess_user -h localhost mocess_db > backup_$DATE.sql
gzip backup_$DATE.sql
EOF

chmod +x backup_postgresql.sh

# Ajouter au cron pour une sauvegarde quotidienne
crontab -e
# Ajouter : 0 2 * * * /path/to/backup_postgresql.sh
```

## 📝 Notes importantes

1. **Sauvegarde** : Gardez toujours une copie du fichier `sqlite_backup.json`
2. **Test** : Testez toujours en environnement de développement avant la production
3. **Monitoring** : Surveillez les performances PostgreSQL après la migration
4. **Backup** : Mettez en place des sauvegardes automatiques

## 🆘 Support

En cas de problème :

1. Vérifiez les logs Django : `python manage.py runserver --verbosity=2`
2. Vérifiez les logs PostgreSQL : `sudo tail -f /var/log/postgresql/postgresql-*.log`
3. Consultez la documentation Django : https://docs.djangoproject.com/en/4.2/ref/databases/
4. Consultez la documentation PostgreSQL : https://www.postgresql.org/docs/
