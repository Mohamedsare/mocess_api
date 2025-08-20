# 🚀 Guide d'Hébergement - SiteMocess

## 📋 Informations de Connexion

### 🔐 Identifiants d'Administration
- **URL d'administration** : http://localhost:8000/admin/
- **Nom d'utilisateur** : `DJIGUEMDE`
- **Email** : `n.djiguemde0012@uca.ac.ma`
- **Mot de passe** : mocess123456

### 🌐 Accès à l'Application
- **Interface d'administration** : http://localhost:8000/admin/
- **API Django REST** : http://localhost:8000/api/
- **Frontend React** : http://localhost:3000/

## 🏗️ Configuration Actuelle

### 📊 Base de Données PostgreSQL
```env
DB_ENGINE=postgresql
DB_NAME=mocess_db
DB_USER=mocess_user
DB_PASSWORD=@Basbedo@123
DB_HOST=localhost
DB_PORT=5432
```

### 📦 Données Migrées
- **74 objets** migrés avec succès de SQLite vers PostgreSQL
- **14 modèles** : Category, Project, ProjectImage, News, NewsImage, Publication, Resource, ContactForm, PartnershipForm, NewsletterSubscription, TeamMember, Partner, EventRegistration, ExternalLink

## 🌍 Options d'Hébergement

### 1. 🐳 Docker (Recommandé)

#### Configuration Docker
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_ENGINE=postgresql
      - DB_NAME=mocess_db
      - DB_USER=mocess_user
      - DB_PASSWORD=@Basbedo@123
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mocess_db
      - POSTGRES_USER=mocess_user
      - POSTGRES_PASSWORD=@Basbedo@123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 2. ☁️ Services Cloud

#### A. Heroku
```bash
# Installation Heroku CLI
# Créer un compte sur heroku.com

# Initialiser le projet
heroku create mocess-app

# Configurer les variables d'environnement
heroku config:set DB_ENGINE=postgresql
heroku config:set DB_NAME=mocess_db
heroku config:set DB_USER=mocess_user
heroku config:set DB_PASSWORD=@Basbedo@123
heroku config:set DB_HOST=localhost
heroku config:set DB_PORT=5432
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=.herokuapp.com

# Ajouter PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Déployer
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Appliquer les migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### B. Railway
```bash
# Installation Railway CLI
npm install -g @railway/cli

# Connexion
railway login

# Initialiser le projet
railway init

# Configurer les variables d'environnement
railway variables set DB_ENGINE=postgresql
railway variables set DB_NAME=mocess_db
railway variables set DB_USER=mocess_user
railway variables set DB_PASSWORD=@Basbedo@123
railway variables set DEBUG=False

# Déployer
railway up

# Appliquer les migrations
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

#### C. DigitalOcean App Platform
```yaml
# .do/app.yaml
name: mocess-app
services:
- name: web
  source_dir: /
  github:
    repo: votre-username/mocess
    branch: main
  run_command: python manage.py runserver 0.0.0.0:$PORT
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DB_ENGINE
    value: postgresql
  - key: DEBUG
    value: "False"
  - key: ALLOWED_HOSTS
    value: ".ondigitalocean.app"

databases:
- name: mocess-db
  engine: PG
  version: "15"
```

### 3. 🖥️ Serveur VPS (Ubuntu/Debian)

#### Installation des dépendances
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Python et pip
sudo apt install python3 python3-pip python3-venv -y

# Installer PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Installer Nginx
sudo apt install nginx -y

# Installer Git
sudo apt install git -y
```

#### Configuration PostgreSQL
```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer la base de données et l'utilisateur
CREATE DATABASE mocess_db;
CREATE USER mocess_user WITH PASSWORD '@Basbedo@123';
GRANT ALL PRIVILEGES ON DATABASE mocess_db TO mocess_user;
\q
```

#### Configuration de l'application
```bash
# Cloner le projet
git clone https://github.com/votre-username/mocess.git
cd mocess/backend

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
export DB_ENGINE=postgresql
export DB_NAME=mocess_db
export DB_USER=mocess_user
export DB_PASSWORD=@Basbedo@123
export DB_HOST=localhost
export DB_PORT=5432
export DEBUG=False
export ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Appliquer les migrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

#### Configuration Nginx
```nginx
# /etc/nginx/sites-available/mocess
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/mocess/backend;
    }

    location /media/ {
        root /var/www/mocess/backend;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/mocess.sock;
    }
}
```

#### Configuration Gunicorn
```bash
# Installer Gunicorn
pip install gunicorn

# Créer le service systemd
sudo nano /etc/systemd/system/mocess.service
```

```ini
[Unit]
Description=Mocess Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mocess/backend
Environment="PATH=/var/www/mocess/backend/venv/bin"
Environment="DB_ENGINE=postgresql"
Environment="DB_NAME=mocess_db"
Environment="DB_USER=mocess_user"
Environment="DB_PASSWORD=@Basbedo@123"
Environment="DB_HOST=localhost"
Environment="DB_PORT=5432"
Environment="DEBUG=False"
Environment="ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com"
ExecStart=/var/www/mocess/backend/venv/bin/gunicorn --workers 3 --bind unix:/run/mocess.sock mocess_backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Activer le service
sudo systemctl start mocess
sudo systemctl enable mocess

# Activer le site Nginx
sudo ln -s /etc/nginx/sites-available/mocess /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 4. 🔒 Configuration SSL (Let's Encrypt)
```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir le certificat SSL
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Renouvellement automatique
sudo crontab -e
# Ajouter : 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📁 Fichiers de Configuration

### requirements.txt (Production)
```txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-filter==23.3
psycopg2-binary==2.9.7
gunicorn==21.2.0
whitenoise==6.6.0
python-decouple==3.8
dj-database-url==2.1.0
```

### settings.py (Production)
```python
# Ajouter en production
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com', 'www.votre-domaine.com']

# Configuration de sécurité
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configuration des fichiers statiques
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## 🔧 Scripts de Déploiement

### deploy.sh
```bash
#!/bin/bash
echo "🚀 Déploiement de SiteMocess..."

# Mettre à jour le code
git pull origin main

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Redémarrer les services
sudo systemctl restart mocess
sudo systemctl restart nginx

echo "✅ Déploiement terminé!"
```

## 📊 Monitoring et Maintenance

### Logs
```bash
# Logs de l'application
sudo journalctl -u mocess -f

# Logs Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### Sauvegarde
```bash
# Script de sauvegarde automatique
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mocess"

# Sauvegarder la base de données
pg_dump mocess_db > $BACKUP_DIR/db_backup_$DATE.sql

# Sauvegarder les fichiers média
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz media/

# Supprimer les sauvegardes de plus de 30 jours
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## 🚨 Sécurité

### Variables d'environnement sensibles
```bash
# Changer ces valeurs en production
SECRET_KEY=votre-secret-key-tres-securisee
DB_PASSWORD=votre-mot-de-passe-securise
```

### Firewall
```bash
# Configuration UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 📞 Support

En cas de problème :
1. Vérifier les logs : `sudo journalctl -u mocess -f`
2. Tester la connexion PostgreSQL : `python manage.py dbshell`
3. Vérifier les permissions : `ls -la /var/www/mocess/`
4. Tester Nginx : `sudo nginx -t`

---

**🎉 Votre application SiteMocess est maintenant prête pour la production !**
