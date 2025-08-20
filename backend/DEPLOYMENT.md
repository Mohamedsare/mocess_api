# Guide de Déploiement - Mocess Backend

## Configuration PostgreSQL pour la Production

### 1. Variables d'environnement requises

Créez un fichier `.env` dans le répertoire `backend/` avec les variables suivantes :

```env
# Paramètres généraux
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# Configuration PostgreSQL
DB_ENGINE=postgresql
DB_NAME=mocess_db
DB_USER=your_db_user
DB_PASSWORD=your_secure_db_password
DB_HOST=localhost
DB_PORT=5432

# Paramètres de sécurité (optionnels)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

### 2. Installation de PostgreSQL

#### Sur Ubuntu/Debian :
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser --createdb your_db_user
sudo -u postgres createdb mocess_db --owner=your_db_user
```

#### Sur Windows :
1. Téléchargez PostgreSQL depuis https://www.postgresql.org/download/windows/
2. Installez et configurez PostgreSQL
3. Créez une base de données `mocess_db`

### 3. Configuration du projet

1. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

2. **Configurez les variables d'environnement :**
   - Copiez `.env.example` vers `.env`
   - Remplissez toutes les valeurs requises

3. **Appliquez les migrations :**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Collectez les fichiers statiques :**
```bash
python manage.py collectstatic
```

5. **Créez un superutilisateur :**
```bash
python manage.py createsuperuser
```

### 4. Mode Développement vs Production

- **Développement :** Par défaut, le projet utilise SQLite
- **Production :** Définissez `DB_ENGINE=postgresql` pour activer PostgreSQL

### 5. Sécurité en Production

Quand `DEBUG=False`, les paramètres suivants sont automatiquement activés :
- HTTPS obligatoire
- Cookies sécurisés
- Protection HSTS
- Protection XSS
- Logging des erreurs

### 6. Logging

Les logs sont automatiquement créés dans `backend/logs/django.log` en production.
Assurez-vous que le répertoire `logs/` existe :
```bash
mkdir -p logs
```

### 7. Sauvegarde de Base de Données

#### Créer une sauvegarde :
```bash
pg_dump -U your_db_user -h localhost mocess_db > backup.sql
```

#### Restaurer une sauvegarde :
```bash
psql -U your_db_user -h localhost mocess_db < backup.sql
```

### 8. Migration depuis SQLite

Si vous avez des données existantes dans SQLite :

1. **Sauvegardez vos données :**
```bash
python manage.py dumpdata > data_backup.json
```

2. **Configurez PostgreSQL et migrez :**
```bash
# Définissez les variables d'environnement pour PostgreSQL
export DB_ENGINE=postgresql
# ... autres variables

python manage.py migrate
python manage.py loaddata data_backup.json
```

### 9. Vérification de la Configuration

Testez votre configuration avec :
```bash
python manage.py check --deploy
```

Cette commande vérifie que votre configuration est prête pour la production.

## 🚀 Migration SQLite vers PostgreSQL pour l'hébergement

### 1. Sauvegarde des données existantes

Avant de migrer, sauvegardez vos données SQLite :
```bash
# Sauvegarder toutes les données
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data_backup.json

# Vérifier la sauvegarde
ls -la data_backup.json
```

### 2. Configuration PostgreSQL sur votre serveur

#### Variables d'environnement pour production :
```env
# Base de données
DB_ENGINE=postgresql
DB_NAME=mocess_production_db
DB_USER=mocess_user
DB_PASSWORD=votre_mot_de_passe_securise
DB_HOST=localhost
DB_PORT=5432

# Sécurité
DEBUG=False
SECRET_KEY=votre_cle_secrete_longue_et_aleatoire
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# HTTPS
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

#### Commandes pour créer la base PostgreSQL :
```bash
# Sur Ubuntu/Debian
sudo -u postgres createuser mocess_user --createdb
sudo -u postgres createdb mocess_production_db --owner=mocess_user
sudo -u postgres psql -c "ALTER USER mocess_user PASSWORD 'votre_mot_de_passe';"
```

### 3. Migration vers PostgreSQL

```bash
# 1. Configurer les variables d'environnement PostgreSQL
export DB_ENGINE=postgresql
export DB_NAME=mocess_production_db
# ... autres variables

# 2. Créer les tables PostgreSQL
python manage.py migrate

# 3. Importer les données sauvegardées
python manage.py loaddata data_backup.json

# 4. Créer un superutilisateur
python manage.py createsuperuser

# 5. Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

### 4. Hébergeurs populaires et leurs configurations

#### Heroku :
```bash
# Ajouter PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Variables automatiquement configurées :
# DATABASE_URL sera définie automatiquement
```

#### DigitalOcean App Platform :
```yaml
# app.yaml
databases:
- engine: PG
  name: mocess-db
  num_nodes: 1
  size: db-s-dev-database
  version: "13"
```

#### Railway :
```bash
# Ajouter PostgreSQL service dans le dashboard
# Variables automatiquement configurées
```

### 5. Vérification finale

```bash
# Vérifier la configuration
python manage.py check --deploy

# Tester la connexion
python manage.py dbshell
```
