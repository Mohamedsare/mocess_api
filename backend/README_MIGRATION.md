# 🚀 Migration SQLite vers PostgreSQL

Ce guide vous accompagne dans la migration de votre base de données SQLite vers PostgreSQL pour la production.

## 📋 Fichiers créés pour la migration

- `migrate_to_postgresql.py` - Script principal de migration
- `verify_migration.py` - Script de vérification post-migration
- `restore_from_backup.py` - Script de restauration (rollback)
- `migrate_to_postgresql.bat` - Script Windows automatisé
- `migrate_to_postgresql.sh` - Script Linux/Mac automatisé
- `GUIDE_MIGRATION_POSTGRESQL.md` - Guide détaillé complet
- `env_example.txt` - Exemple de configuration

## ⚡ Migration Rapide (Windows)

### 1. Installer PostgreSQL

```bash
# Télécharger depuis https://www.postgresql.org/download/windows/
# Ou utiliser Chocolatey :
choco install postgresql
```

### 2. Créer la base de données

```bash
# Ouvrir pgAdmin ou utiliser psql
# Créer l'utilisateur et la base de données :
CREATE USER mocess_user WITH PASSWORD 'your-secure-password';
CREATE DATABASE mocess_db OWNER mocess_user;
GRANT ALL PRIVILEGES ON DATABASE mocess_db TO mocess_user;
```

### 3. Configurer l'environnement

Créez ou modifiez votre fichier `.env` dans le dossier `backend/` :

```bash
# Configuration Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration PostgreSQL
DB_ENGINE=postgresql
DB_NAME=mocess_db
DB_USER=mocess_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Exécuter la migration

```bash
# Aller dans le dossier backend
cd SiteMocess/backend

# Exécuter le script automatisé
migrate_to_postgresql.bat
```

## ⚡ Migration Rapide (Linux/Mac)

### 1. Installer PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
brew services start postgresql
```

### 2. Créer la base de données

```bash
sudo -u postgres psql

CREATE USER mocess_user WITH PASSWORD 'your-secure-password';
CREATE DATABASE mocess_db OWNER mocess_user;
GRANT ALL PRIVILEGES ON DATABASE mocess_db TO mocess_user;
\q
```

### 3. Configurer l'environnement

Créez ou modifiez votre fichier `.env` dans le dossier `backend/` :

```bash
# Configuration Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration PostgreSQL
DB_ENGINE=postgresql
DB_NAME=mocess_db
DB_USER=mocess_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Exécuter la migration

```bash
# Aller dans le dossier backend
cd SiteMocess/backend

# Rendre le script exécutable
chmod +x migrate_to_postgresql.sh

# Exécuter le script automatisé
./migrate_to_postgresql.sh
```

## 🔍 Vérification Post-Migration

Après la migration, vérifiez que tout fonctionne :

```bash
# Vérifier la migration
python verify_migration.py

# Tester l'application
python manage.py runserver

# Vérifier l'admin Django
# Ouvrir http://localhost:8000/admin/
```

## 🛠️ Dépannage

### Problème de connexion PostgreSQL

```bash
# Vérifier que PostgreSQL fonctionne
# Windows : Services > PostgreSQL
# Linux : sudo systemctl status postgresql
# macOS : brew services list | grep postgresql
```

### Problème de permissions

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Donner les permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mocess_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mocess_user;
\q
```

### Problème de migration

```bash
# Vérifier le fichier de sauvegarde
cat sqlite_backup.json

# Relancer la migration
python migrate_to_postgresql.py
```

## 🔄 Rollback (si nécessaire)

Si vous devez revenir à SQLite :

```bash
# 1. Modifier le fichier .env
DB_ENGINE=sqlite3

# 2. Restaurer les données
python restore_from_backup.py
```

## 📊 Optimisations PostgreSQL

### Configuration de performance

```sql
-- Dans psql
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Redémarrer PostgreSQL
```

### Index pour les performances

```bash
python manage.py shell

# Dans le shell Python :
from django.db import connection
cursor = connection.cursor()

# Index sur les champs de recherche
cursor.execute("CREATE INDEX idx_project_title ON api_project(title);")
cursor.execute("CREATE INDEX idx_news_title ON api_news(title);")
cursor.execute("CREATE INDEX idx_publication_title ON api_publication(title);")
```

## 🔒 Sécurité

### Configuration de sécurité

```sql
-- Limiter les connexions
ALTER SYSTEM SET max_connections = 100;

-- Activer SSL
ALTER SYSTEM SET ssl = on;

-- Redémarrer PostgreSQL
```

### Sauvegarde automatique

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

## 📝 Checklist de Migration

- [ ] PostgreSQL installé et configuré
- [ ] Base de données créée
- [ ] Utilisateur PostgreSQL créé avec permissions
- [ ] Fichier .env configuré pour PostgreSQL
- [ ] Script de migration exécuté avec succès
- [ ] Vérification post-migration réussie
- [ ] Application testée et fonctionnelle
- [ ] Sauvegarde SQLite conservée
- [ ] Optimisations PostgreSQL appliquées
- [ ] Sauvegarde automatique configurée

## 🆘 Support

En cas de problème :

1. Vérifiez les logs Django : `python manage.py runserver --verbosity=2`
2. Vérifiez les logs PostgreSQL
3. Consultez le guide détaillé : `GUIDE_MIGRATION_POSTGRESQL.md`
4. Vérifiez que tous les fichiers de migration sont présents

## 🎯 Avantages de PostgreSQL

- **Performance** : Meilleure performance pour les requêtes complexes
- **Concurrence** : Gestion avancée de la concurrence
- **Fiabilité** : ACID compliance et récupération après panne
- **Extensibilité** : Support des types de données avancés
- **Production** : Recommandé pour les environnements de production
