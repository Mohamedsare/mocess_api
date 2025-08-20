# Guide de Migration SQLite vers PostgreSQL - SiteMocess

## Étape 1: Configuration PostgreSQL

### 1.1 Vérifier que PostgreSQL est installé et en cours d'exécution

```powershell
# Vérifier le service PostgreSQL
Get-Service -Name "*postgres*"
```

### 1.2 Créer la base de données et l'utilisateur PostgreSQL

Ouvrez pgAdmin ou utilisez la ligne de commande :

```sql
-- Se connecter à PostgreSQL en tant que superutilisateur
-- Créer l'utilisateur
CREATE USER mocess_user WITH PASSWORD '@Basbedo@123';

-- Créer la base de données
CREATE DATABASE mocess_db OWNER mocess_user;

-- Donner les privilèges
GRANT ALL PRIVILEGES ON DATABASE mocess_db TO mocess_user;
ALTER DATABASE mocess_db OWNER TO mocess_user;
```

### 1.3 Vérifier la configuration Django

Le fichier `env` doit contenir :

```env
DB_ENGINE=postgresql
DB_NAME=mocess_db
DB_USER=mocess_user
DB_PASSWORD=@Basbedo@123
DB_HOST=localhost
DB_PORT=5432
```

## Étape 2: Migration des données

### 2.1 Sauvegarder les données SQLite

```bash
python migrate_direct.py
```

Ce script va :
1. Sauvegarder toutes les données SQLite dans `sqlite_backup.json`
2. Tester la connexion PostgreSQL
3. Migrer le schéma vers PostgreSQL
4. Restaurer les données depuis la sauvegarde
5. Vérifier la migration

### 2.2 Vérifier la migration

```bash
# Tester l'application
python manage.py runserver

# Vérifier les données dans l'admin Django
# http://localhost:8000/admin/
```

## Étape 3: Tests post-migration

### 3.1 Tester l'interface d'administration
- Se connecter à l'admin Django
- Vérifier que tous les modèles sont visibles
- Tester la création/modification d'objets

### 3.2 Tester les API endpoints
- Tester les endpoints de l'API
- Vérifier que les données sont correctement retournées

### 3.3 Tester les fonctionnalités principales
- Navigation sur le site
- Recherche et filtres
- Upload de fichiers

## Étape 4: Nettoyage

Une fois que tout fonctionne :

1. Sauvegarder le fichier `sqlite_backup.json`
2. Supprimer le fichier `db.sqlite3`
3. Mettre à jour la documentation

## Dépannage

### Problème de connexion PostgreSQL

```bash
# Vérifier que PostgreSQL fonctionne
Get-Service -Name "postgresql-x64-17"

# Redémarrer le service si nécessaire
Restart-Service -Name "postgresql-x64-17"
```

### Problème de permissions

```sql
-- Dans PostgreSQL, donner tous les privilèges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mocess_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mocess_user;
```

### Problème de migration

```bash
# Réinitialiser les migrations si nécessaire
python manage.py migrate api zero
python manage.py makemigrations
python manage.py migrate
```

## Rollback (si nécessaire)

Si vous devez revenir à SQLite :

1. Modifier le fichier `env` :
   ```env
   DB_ENGINE=sqlite3
   ```

2. Restaurer les données depuis la sauvegarde :
   ```bash
   python restore_from_backup.py
   ```

## Notes importantes

- Gardez toujours une copie du fichier `sqlite_backup.json`
- Testez en environnement de développement avant la production
- Surveillez les performances PostgreSQL après la migration
- Mettez en place des sauvegardes automatiques
