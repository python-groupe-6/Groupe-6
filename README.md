# EduQuiz AI – Le Futur de la Révision 🎓🤖

**EduQuiz AI** est une plateforme avancée conçue pour transformer instantanément vos documents PDF en parcours d'apprentissage interactifs. 

## 🛠️ Méthodologie de Réalisation
Ce projet suit une méthodologie rigoureuse pour garantir sa qualité et sa modularité :
1. **Cahier des charges** : [Consulter le document](./docs/Cahier_des_charges.md)
2. **Environnement** : Utilisation de `virtualenv` et gestion stricte des dépendances via `requirements.txt`.
3. **Développement Modulaire** :
    - `src/pdf_processor.py` (Extraction)
    - `src/quiz_generator.py` (Logique IA/NLP)
    - `src/utils.py` (Utilitaires)
4. **Interface** : Interface Web robuste via **Django** (v5.0+).
5. **Documentation** : [Manuel Utilisateur](./docs/Manuel_Utilisateur.md)

## ✨ Fonctionnalités
- **Design Premium** : Interface moderne et responsive.
- **Workflow Django** : Gestion complète des utilisateurs, des quiz et des résultats.
- **Intelligence Hybride** : Google Gemini avec fallback local.
- **Export PDF** : Rapports de performance téléchargeables.

## 🚀 Démarrage Rapide

### 1. Prérequis
- Python 3.14 (ou version stable supportée)
- Clé API Google Gemini (optionnelle, placée dans `.env`)

### 2. Installation
```bash
# Installation des dependances via le script automatique
.\install_dependencies.bat
```

Ou manuellement :
```bash
# Activation de l'environnement virtuel (.venv)
.\.venv\Scripts\activate

# Installation des dépendances
pip install -r requirements.txt

# Migrations de la base de données
python manage.py migrate
```

### 3. Lancement du serveur
```bash
python manage.py runserver
```

## 📚 Documentation complémentaire
- [Guide de migration PostgreSQL](./docs/Migration_PostgreSQL.md)
- [Cahier des charges](./docs/Cahier_des_charges.md)
- [Manuel Utilisateur](./docs/Manuel_Utilisateur.md)
