# Guide de Déploiement sur Railway

## 🚀 Préparation du Projet

Votre projet est maintenant **prêt pour Railway** ! Les modifications apportées au `settings.py` permettent une configuration automatique pour l'environnement Railway.

## 📋 Étapes de Déploiement

### 1. Créer un compte Railway
- Aller sur [railway.app](https://railway.app)
- Se connecter avec GitHub
- Créer un nouveau projet

### 2. Connecter le Repository
- Cliquer sur "Deploy from GitHub repo"
- Sélectionner votre repository `SiteMocess20`
- Choisir le dossier `backend/`

### 3. Configuration Automatique
Railway détectera automatiquement :
- ✅ **Python/Django** (via `requirements.txt`)
- ✅ **Base de données PostgreSQL** (créée automatiquement)
- ✅ **Variables d'environnement** (ajoutées automatiquement)

### 4. Variables d'Environnement à Configurer

Dans l'onglet "Variables" de Railway, ajouter :

```bash
# Configuration Django
SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
DEBUG=False

# Configuration des domaines (ajoutée automatiquement par Railway)
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration de sécurité
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### 5. Déploiement
- Railway utilisera automatiquement le `Procfile`
- Les migrations s'exécuteront automatiquement
- Les fichiers statiques seront collectés

## 🔧 Configuration Automatique

Votre `settings.py` gère automatiquement :

### Domaine Railway
```python
# Ajout automatique des domaines Railway
if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
    ALLOWED_HOSTS.append(os.environ.get('RAILWAY_PUBLIC_DOMAIN'))
```

### Base de Données
```python
# Configuration automatique PostgreSQL avec SSL
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
    if 'postgresql' in DATABASE_URL:
        DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
```

### CORS
```python
# Ajout automatique des domaines Railway pour CORS
if os.environ.get('RAILWAY_STATIC_URL'):
    CORS_ALLOWED_ORIGINS.append(os.environ.get('RAILWAY_STATIC_URL'))
```

## 🌐 Accès à l'Application

Après le déploiement :
- **URL principale** : `https://votre-app.railway.app`
- **Admin Django** : `https://votre-app.railway.app/admin/`
- **API** : `https://votre-app.railway.app/api/`

## 📊 Monitoring

Railway fournit :
- ✅ **Logs en temps réel**
- ✅ **Métriques de performance**
- ✅ **Redémarrage automatique** en cas d'erreur
- ✅ **Health checks** automatiques

## 🔒 Sécurité

Votre configuration inclut :
- ✅ **HTTPS forcé** en production
- ✅ **Headers de sécurité** (HSTS, XSS, etc.)
- ✅ **Cookies sécurisés**
- ✅ **SSL requis** pour PostgreSQL

## 🚨 Dépannage

### Erreur de Migration
```bash
# Dans Railway, exécuter manuellement :
python manage.py migrate
```

### Erreur de Fichiers Statiques
```bash
# Collecter les fichiers statiques :
python manage.py collectstatic --noinput
```

### Erreur de Base de Données
- Vérifier que `DATABASE_URL` est bien configuré
- Vérifier la connectivité PostgreSQL

## 📝 Notes Importantes

1. **Railway redémarre automatiquement** l'application en cas d'erreur
2. **Les migrations s'exécutent automatiquement** au déploiement
3. **Les fichiers statiques sont servis** par Whitenoise
4. **La sécurité est renforcée** automatiquement en production

## 🎯 Prochaines Étapes

1. **Déployer sur Railway**
2. **Configurer le domaine personnalisé** (optionnel)
3. **Configurer les notifications** (Slack, Discord, etc.)
4. **Mettre en place le monitoring** avancé

---

**Votre projet est maintenant 100% prêt pour Railway ! 🎉**

