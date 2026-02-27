# EduQuiz AI 🎓🤖

<div align="center">

![EduQuiz AI](https://img.shields.io/badge/EduQuiz-AI%20Powered-4F46E5?style=for-the-badge&logo=robot&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1.5-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=for-the-badge&logo=postgresql&logoColor=white)

**Transformez vos documents en parcours d'apprentissage interactifs avec l'IA**

</div>

---

## 🎯 À Propos

**EduQuiz AI** est une plateforme intelligente qui utilise l'IA (Google Gemini) pour transformer instantanément vos documents (PDF, DOCX, TXT) en quiz interactifs.

### 🌟 Points Forts (EduQuiz AI Pro)
- 🤖 **IA Multimodale** : Génération de quiz via Documents, **YouTube** et **Photos (OCR)**.
- 🧠 **Apprentissage SRS** : Système de répétition espacée et tuteur IA interactif.
- 🎮 **Gamification** : XP, niveaux, badges et séries (Streaks) pour l'engagement.
- 📊 **Analytiques Pro** : Heatmap d'activité et analyse des lacunes par l'IA.
- 🌐 **Social & Community** : Bibliothèque publique et partage communautaire.
- 🎨 **Design Premium** : Interface ultra-moderniste, fluide et mode sombre.

---

## 📸 Aperçu du Parcours Utilisateur

Découvrez l'expérience **EduQuiz AI** étape par étape :

### 1. Une Suite d'Outils Complète (Public)
![Landing Page](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20103117.png)

### 2. Inscription & Sécurité
![Inscription](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20103200.png)

### 3. Votre Centre de Commande (Dashboard)
![Dashboard](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20102430.png)

### 4. Progression & Gamification (XP, Niveaux, Badges)
![Gamification](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20102747.png)

### 5. Génération Multimodale (YouTube, PDF, OCR)
![Quiz Setup](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20102559.png)

### 6. Analyse des Résultats
![Résultats](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20102630.png)

### 7. Système de Révision Espacée (SRS)
![SRS](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20102934.png)

### 8. Bibliothèque Communautaire
![Bibliothèque](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20102958.png)

### 9. Profil Utilisateur Personnalisé
![Profil](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20102817.png)

### 10. Paramètres & Mode Sombre
![Paramètres](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20102831.png)

### 11. Offres Premium & Footer
![Pricing](assets/images/Capture%20d%27%C3%A9cran%202026-02-23%20103040.png)

---

## 🛠 Stack Technique

- **Backend** : Django 5.1.5, Python 3.10+
- **Base de données** : PostgreSQL 16 (ou SQLite en local)
- **IA** : Google Gemini API
- **Frontend** : HTML5, CSS3 (Vanilla), JavaScript, Bootstrap 5
- **Outils** : Whitenoise, Pillow, ReportLab, python-dotenv

---

## 📦 Prérequis

- **Python 3.10+**
- **PostgreSQL 16** (recommandé) ou **SQLite**
- **Clé API Google Gemini** (gratuite sur [Google AI Studio](https://aistudio.google.com/))

---

## 🚀 Installation Rapide

### 1. Cloner le Projet
```bash
git clone https://github.com/python-groupe-6/Groupe-6.git
cd Groupe-6
```

### 2. Environnement Virtuel
```bash
python -m venv .venv_new
# Activez-le :
# Windows: .\.venv_new\Scripts\activate
# Unix: source .venv_new/bin/activate
```

### 3. Installation & Configuration
```bash
pip install -r requirements.txt
cp .env.example .env
```
Éditez le `.env` avec votre `SECRET_KEY` et votre `GEMINI_API_KEY`.

### 4. Lancement
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Accès : **http://127.0.0.1:8000/**

---

## 🤝 Contribution

Les contributions sont les bienvenues ! 
1. **Fork** le projet.
2. Créez votre branche (`git checkout -b feature/AmazingFeature`).
3. **Commit** vos changements (`git commit -m 'Add: feature'`).
4. **Push** vers la branche (`git push origin feature/AmazingFeature`).
5. Ouvrez une **Pull Request**.

---

## 📞 Contact & Support

- **Email** : contacteduquizai@gmail.com
- **GitHub** : [python-groupe-6/Groupe-6](https://github.com/python-groupe-6/Groupe-6)

---

## 📄 Licence
Sous licence **MIT**. Fait avec ❤️ par le **Groupe 6** pour l'éducation.
