# Scripts de Vérification de la Configuration de Production

Ce dossier contient des scripts pour vérifier que votre configuration est prête pour la production sur Railway.

## Scripts Disponibles

### 1. `check_production.py` - Vérification Complète
Script principal qui effectue une vérification détaillée de tous les aspects de la configuration.

**Utilisation :**
```bash
python check_production.py
```

**Ce qu'il vérifie :**
- Variables d'environnement critiques (SECRET_KEY, DEBUG, DB_*, etc.)
- Configuration de la base de données
- Fichiers de configuration requis (railway.json, Procfile, requirements.txt)
- Paramètres de sécurité (SSL, HSTS, etc.)

### 2. `check_quick.py` - Vérification Rapide
Script rapide pour une vérification basique des éléments critiques.

**Utilisation :**
```bash
python check_quick.py
```

**Ce qu'il vérifie :**
- Variables d'environnement essentielles
- Fichiers de configuration
- Statut DEBUG

## Résolution des Problèmes

### Variables d'Environnement Manquantes
Si des variables sont manquantes, vérifiez que votre fichier `railway.env` contient :

```env
# Configuration Django
SECRET_KEY=votre_cle_secrete
DEBUG=False

# Configuration de la base de données
DB_ENGINE=postgresql
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=votre_host
DB_PORT=votre_port

# Configuration de sécurité
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
```

### Fichiers Manquants
Assurez-vous que ces fichiers sont présents dans le répertoire `backend/` :
- `railway.json` - Configuration Railway
- `Procfile` - Configuration de déploiement
- `requirements.txt` - Dépendances Python

### Problème DEBUG Activé
Si `DEBUG=True`, changez-le en `DEBUG=False` dans `railway.env` pour la production.

## Déploiement

Une fois que tous les tests passent, vous pouvez déployer sur Railway :

```bash
# Vérifier la configuration
python check_production.py

# Si tout est OK, déployer
railway up
```

## Support

En cas de problème, vérifiez :
1. Le contenu de `railway.env`
2. L'existence des fichiers de configuration
3. Les logs d'erreur du script
