# EduQuiz AI 🎓🤖

<div align="center">

![EduQuiz AI](https://img.shields.io/badge/EduQuiz-AI%20Powered-4F46E5?style=for-the-badge&logo=robot&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1.5-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Transformez vos documents en parcours d'apprentissage interactifs avec l'Intelligence Artificielle**

[Démo en ligne](https://eduquiz-ai.onrender.com) • [Documentation](#-documentation) • [Installation](#-installation-rapide) • [Contribuer](#-contribution)

</div>

---

## 📋 Table des Matières

- [À Propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies-utilisées)
- [Prérequis](#-prérequis)
- [Installation Rapide](#-installation-rapide)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [Déploiement](#-déploiement)
- [Dépannage](#-dépannage)
- [Contribution](#-contribution)
- [Documentation](#-documentation)
- [Licence](#-licence)

---

## 🎯 À Propos

**EduQuiz AI** est une plateforme éducative intelligente qui utilise l'intelligence artificielle pour transformer instantanément vos documents (PDF, DOCX, TXT) en outils de révision interactifs. Générez des quiz personnalisés, suivez votre progression et améliorez vos performances d'apprentissage.

### 🌟 Points Forts

- 🤖 **IA Avancée** : Utilise Google Gemini pour une génération de contenu de haute qualité
- 🎨 **Design Premium** : Interface moderne et responsive avec mode sombre
- 📊 **Analytique Complète** : Suivi détaillé de la progression et statistiques de performance
- 🔒 **Sécurisé** : Authentification robuste et protection des données (RGPD)
- 🚀 **Performance** : Optimisé pour une expérience utilisateur fluide
- 📱 **Responsive** : Fonctionne parfaitement sur tous les appareils

---

## ️ Technologies Utilisées

### Backend
- **Django 5.1.5** - Framework web Python
- **PostgreSQL 16** - Base de données relationnelle
- **Google Gemini AI** - Génération de contenu intelligent
- **Python 3.10+** - Langage de programmation

### Frontend
- **HTML5/CSS3** - Structure et style
- **JavaScript** - Interactivité
- **Bootstrap 5** - Framework CSS
- **FontAwesome 6** - Icônes

### Outils & Services
- **WhiteNoise** - Gestion des fichiers statiques
- **python-dotenv** - Gestion des variables d'environnement
- **Pillow** - Traitement d'images
- **ReportLab** - Génération de PDF

---

## 📦 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Python 3.10 ou supérieur** ([Télécharger](https://www.python.org/downloads/))
- **PostgreSQL 16** ([Télécharger](https://www.postgresql.org/download/)) *(optionnel, SQLite par défaut)*
- **Git** ([Télécharger](https://git-scm.com/downloads))
- **Un éditeur de code** (VS Code recommandé)

### Clé API Google Gemini (Optionnelle)
Pour utiliser l'IA Google Gemini, obtenez une clé API gratuite :
1. Visitez [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créez une nouvelle clé API
3. Copiez la clé pour la configuration

---

## 🚀 Installation Rapide

### 1. Cloner le Projet

```bash
# Cloner le dépôt
git clone https://github.com/python-groupe-6/Groupe-6.git

# Accéder au répertoire
cd Groupe-6
```

### 2. Créer l'Environnement Virtuel

**Windows :**
```bash
# Créer l'environnement virtuel
python -m venv .venv_new

# Activer l'environnement
.\.venv_new\Scripts\activate
```

**macOS/Linux :**
```bash
# Créer l'environnement virtuel
python3 -m venv .venv_new

# Activer l'environnement
source .venv_new/bin/activate
```

### 3. Installer les Dépendances

```bash
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Configuration de l'Environnement

Créez un fichier `.env` à la racine du projet :

```bash
# Copier le fichier d'exemple
cp .env.example .env
```

Éditez le fichier `.env` avec vos paramètres :

```env
# Configuration Django
SECRET_KEY=votre-cle-secrete-django-tres-longue-et-aleatoire
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données PostgreSQL (optionnel)
DB_NAME=eduquiz_db
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432

# Google Gemini AI (optionnel)
GEMINI_API_KEY=votre-cle-api-gemini

# Email (pour réinitialisation de mot de passe)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-application
```

> **💡 Note :** Si PostgreSQL n'est pas configuré, l'application utilisera automatiquement SQLite pour le développement local.

### 5. Configurer la Base de Données

**Option A : PostgreSQL (Recommandé pour la production)**

```bash
# Créer la base de données PostgreSQL
psql -U postgres
CREATE DATABASE eduquiz_db;
\q

# Appliquer les migrations
python manage.py migrate
```

**Option B : SQLite (Développement local)**

```bash
# Les migrations créeront automatiquement la base SQLite
python manage.py migrate
```

### 6. Créer un Super Utilisateur

```bash
# Créer un compte administrateur
python manage.py createsuperuser

# Suivez les instructions pour définir :
# - Nom d'utilisateur
# - Email
# - Mot de passe
```

### 7. Collecter les Fichiers Statiques

```bash
# Collecter tous les fichiers CSS, JS, images
python manage.py collectstatic --noinput
```

### 8. Lancer le Serveur de Développement

```bash
# Démarrer le serveur
python manage.py runserver

# Le serveur sera accessible à :
# http://127.0.0.1:8000/
```

🎉 **Félicitations !** Votre application est maintenant opérationnelle !

---

## ⚙️ Configuration

### Variables d'Environnement Importantes

| Variable | Description | Valeur par Défaut | Requis |
|----------|-------------|-------------------|--------|
| `SECRET_KEY` | Clé secrète Django | - | ✅ Oui |
| `DEBUG` | Mode debug | `False` | ✅ Oui |
| `ALLOWED_HOSTS` | Hôtes autorisés | `localhost` | ✅ Oui |
| `DB_NAME` | Nom de la base PostgreSQL | `eduquiz_db` | ❌ Non |
| `DB_USER` | Utilisateur PostgreSQL | `postgres` | ❌ Non |
| `DB_PASSWORD` | Mot de passe PostgreSQL | - | ❌ Non |
| `GEMINI_API_KEY` | Clé API Google Gemini | - | ❌ Non |
| `EMAIL_HOST_USER` | Email pour notifications | - | ❌ Non |

### Génération d'une SECRET_KEY

```python
# Dans un terminal Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 📖 Utilisation

### 1. Accéder à l'Application

Ouvrez votre navigateur et accédez à : **http://127.0.0.1:8000/**

### 2. Créer un Compte

1. Cliquez sur **"Inscription"**
2. Remplissez le formulaire avec vos informations
3. Acceptez les conditions d'utilisation
4. Cliquez sur **"Créer un compte"**

### 3. Générer un Quiz

1. **Connectez-vous** à votre compte
2. Cliquez sur **"Nouveau Quiz"**
3. **Téléchargez** un document (PDF, DOCX, ou TXT)
4. **Configurez** les paramètres :
   - Nombre de questions (3-15)
   - Niveau de difficulté
   - Temps limite
5. Cliquez sur **"Générer le Quiz"**
6. **Répondez** aux questions
7. **Consultez** vos résultats et téléchargez le rapport PDF

### 4. Suivre votre Progression

- Accédez à **"Historique"** pour voir tous vos quiz
- Consultez vos **statistiques** de performance
- Analysez vos **points forts** et **axes d'amélioration**

### 5. Administration

Accédez au panneau d'administration : **http://127.0.0.1:8000/admin/**

- Gérez les utilisateurs
- Consultez les quiz générés
- Modérez le contenu
- Configurez les paramètres

---

## 📁 Structure du Projet

```
Groupe-6/
├── 📁 accounts/                    # Application de gestion des utilisateurs
│   ├── 📁 migrations/              # Migrations de base de données
│   ├── 📁 templates/accounts/      # Templates d'authentification
│   ├── forms.py                    # Formulaires d'inscription/connexion
│   ├── models.py                   # Modèles utilisateur
│   ├── urls.py                     # Routes d'authentification
│   └── views.py                    # Vues d'authentification
│
├── 📁 core/                        # Application principale
│   ├── 📁 migrations/              # Migrations de base de données
│   ├── 📁 templates/core/          # Templates des pages principales
│   │   ├── home.html               # Page d'accueil
│   │   ├── about.html              # À propos
│   │   ├── contact.html            # Contact
│   │   ├── terms.html              # Conditions d'utilisation
│   │   ├── privacy.html            # Politique de confidentialité
│   │   └── help.html               # Aide
│   ├── models.py                   # Modèles (Contact, Testimonial)
│   ├── urls.py                     # Routes principales
│   └── views.py                    # Vues principales
│
├── 📁 quiz/                        # Application de quiz
│   ├── 📁 migrations/              # Migrations de base de données
│   ├── 📁 templates/quiz/          # Templates de quiz
│   │   ├── quiz_setup.html         # Configuration du quiz
│   │   ├── quiz_take.html          # Passer le quiz
│   │   ├── quiz_result.html        # Résultats
│   │   └── quiz_history.html       # Historique
│   ├── models.py                   # Modèles (Quiz, Question, Result)
│   ├── services.py                 # Services (génération IA)
│   ├── urls.py                     # Routes de quiz
│   └── views.py                    # Vues de quiz
│
├── 📁 eduquiz_project/             # Configuration Django
│   ├── settings.py                 # Paramètres du projet
│   ├── urls.py                     # Routes principales
│   └── wsgi.py                     # Configuration WSGI
│
├── 📁 static/                      # Fichiers statiques
│   ├── 📁 css/                     # Feuilles de style
│   │   ├── styles.css              # Styles globaux
│   │   ├── auth.css                # Styles d'authentification
│   │   ├── legal.css               # Styles pages légales
│   │   └── quiz.css                # Styles de quiz
│   ├── 📁 js/                      # Scripts JavaScript
│   └── 📁 images/                  # Images et logos
│
├── 📁 templates/                   # Templates globaux
│   ├── base.html                   # Template de base
│   └── 📁 registration/            # Templates d'authentification
│       ├── login.html              # Page de connexion
│       └── password_reset.html     # Réinitialisation MDP
│
├── 📁 media/                       # Fichiers uploadés (générés)
├── 📁 staticfiles/                 # Fichiers statiques collectés (générés)
│
├── .env                            # Variables d'environnement (à créer)
├── .env.example                    # Exemple de configuration
├── .gitignore                      # Fichiers ignorés par Git
├── manage.py                       # Script de gestion Django
├── requirements.txt                # Dépendances Python
├── README.md                       # Ce fichier
└── db.sqlite3                      # Base de données SQLite (générée)
```

---

## 🌐 Déploiement

### Déploiement sur Render

1. **Créer un compte** sur [Render](https://render.com)

2. **Créer un nouveau Web Service**
   - Connectez votre dépôt GitHub
   - Sélectionnez la branche `main`

3. **Configuration du Service**
   ```
   Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   Start Command: gunicorn eduquiz_project.wsgi:application
   ```

4. **Variables d'Environnement**
   Ajoutez dans le dashboard Render :
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=votre-app.onrender.com`
   - `DATABASE_URL` (PostgreSQL fourni par Render)
   - `GEMINI_API_KEY`

5. **Déployer** et accédez à votre application !

📖 **Guide détaillé :** Consultez [DEPLOYMENT_RENDER.md](./DEPLOYMENT_RENDER.md)

---

## 🔧 Dépannage

### Problème : Le serveur ne démarre pas

**Solution :**
```bash
# Vérifier que l'environnement virtuel est activé
# Windows
.\.venv_new\Scripts\activate

# macOS/Linux
source .venv_new/bin/activate

# Réinstaller les dépendances
pip install -r requirements.txt

# Vérifier les migrations
python manage.py migrate
```

### Problème : Erreur de connexion à PostgreSQL

**Solution :**
```bash
# Vérifier que PostgreSQL est en cours d'exécution
# Windows
pg_ctl status

# Vérifier les credentials dans .env
# Ou utiliser SQLite en commentant les variables DB_* dans .env
```

### Problème : Les fichiers statiques ne se chargent pas

**Solution :**
```bash
# Vérifier que DEBUG=True dans .env
# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Redémarrer le serveur
python manage.py runserver
```

### Problème : Erreur "SECRET_KEY not found"

**Solution :**
```bash
# Générer une nouvelle SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Ajouter dans .env
SECRET_KEY=la-cle-generee
```

### Problème : L'IA ne génère pas de quiz

**Solution :**
1. Vérifiez que `GEMINI_API_KEY` est définie dans `.env`
2. Vérifiez votre quota API sur [Google AI Studio](https://makersuite.google.com/)
3. L'application utilisera un fallback local si l'API n'est pas disponible

### Problème : Erreur lors de l'inscription

**Solution :**
```bash
# Vérifier que les migrations sont appliquées
python manage.py showmigrations

# Appliquer les migrations manquantes
python manage.py migrate

# Créer un superuser pour tester
python manage.py createsuperuser
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

### 1. Fork le Projet

```bash
# Cliquez sur "Fork" en haut de la page GitHub
```

### 2. Créer une Branche

```bash
git checkout -b feature/AmazingFeature
```

### 3. Commit vos Changements

```bash
git add .
git commit -m "Add: Description de votre fonctionnalité"
```

### 4. Push vers la Branche

```bash
git push origin feature/AmazingFeature
```

### 5. Ouvrir une Pull Request

Allez sur GitHub et créez une Pull Request avec une description détaillée.

### Conventions de Commit

- `Add:` Nouvelle fonctionnalité
- `Fix:` Correction de bug
- `Update:` Mise à jour de code existant
- `Docs:` Documentation
- `Style:` Formatage, style
- `Refactor:` Refactorisation de code
- `Test:` Ajout de tests

---

## 📚 Documentation

### Documentation Complémentaire

- 📖 [Guide de Migration PostgreSQL](./docs/Migration_PostgreSQL.md)
- 📋 [Cahier des Charges](./docs/Cahier_des_charges.md)
- 👤 [Manuel Utilisateur](./docs/Manuel_Utilisateur.md)
- 🚀 [Guide de Déploiement Render](./DEPLOYMENT_RENDER.md)

### API et Services

- [Documentation Django](https://docs.djangoproject.com/)
- [Google Gemini AI](https://ai.google.dev/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)
- [PostgreSQL](https://www.postgresql.org/docs/)

---

## 👥 Équipe

**Groupe 6 - Python**

- 👨‍💻 Développeurs Backend & Frontend
- 🎨 Designers UI/UX
- 📊 Analystes de données
- 🧪 Testeurs QA

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](./LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- Google Gemini AI pour la génération de contenu intelligent
- La communauté Django pour le framework robuste
- Bootstrap pour les composants UI
- FontAwesome pour les icônes
- Tous les contributeurs du projet

---

## 📞 Contact

**Email :** contacteduquizai@gmail.com

**GitHub :** [python-groupe-6/Groupe-6](https://github.com/python-groupe-6/Groupe-6)

**Démo :** [eduquiz-ai.onrender.com](https://eduquiz-ai.onrender.com)

---

<div align="center">

**Fait avec ❤️ pour l'éducation**

⭐ Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile !

</div>
