# EduQuiz AI – Le Futur de la Révision 🎓🤖

**EduQuiz AI** est une plateforme avancée conçue pour transformer instantanément vos documents PDF en parcours d'apprentissage interactifs. 

## 🛠️ Méthodologie de Réalisation
Ce projet suit une méthodologie rigoureuse pour garantir sa qualité et sa modularité :
1. **Cahier des charges** : [Consulter le document](./docs/Cahier_des_charges.md)
2. **Environnement** : Utilisation de `virtualenv` et gestion stricte des dépendances via `requirements.txt`.
3. **Développement Modulaire** :
    - `pdf_processor.py` (Extraction)
    - `quiz_generator.py` (Logique IA/NLP)
    - `report_generator.py` (Export PDF)
    - `app.py` (Interface Streamlit)
4. **Interface** : Interface Web moderne via **Streamlit** (v2.1.0).
5. **Documentation** : [Manuel Utilisateur](./docs/Manuel_Utilisateur.md)

## ✨ Fonctionnalités
- **Design Premium** : Interface basée sur le "Glassmorphism".
- **Workflow Guidé** : Processus en 4 étapes pour une efficacité maximale.
- **Intelligence Hybride** : OpenAI GPT avec fallback local Spacy.
- **Export PDF** : Rapports de performance téléchargeables.

## 🚀 Démarrage Rapide

### 1. Prérequis
- Python 3.9+
- Clé API OpenAI (optionnelle, placée dans `.env`)

### 2. Installation
```bash
# Activation de l'environnement virtuel (Windows)
.\venv\Scripts\activate

# Installation des dépendances
pip install -r requirements.txt
```

### 3. Configuration de la base de données

**Option 1 : PostgreSQL (Recommandé pour la production)**
```bash
# Créer la base de données dans PostgreSQL
# Puis configurer le fichier .env avec vos credentials
# Voir docs/Migration_PostgreSQL.md pour plus de détails

# Vérifier la connexion
python scripts/verify_database.py
```

**Option 2 : SQLite (Développement local)**
L'application bascule automatiquement sur SQLite si PostgreSQL n'est pas configuré.

### 4. Lancement
```bash
streamlit run app.py
```

## 📚 Documentation complémentaire
- [Guide de migration PostgreSQL](./docs/Migration_PostgreSQL.md)
- [Cahier des charges](./docs/Cahier_des_charges.md)
- [Manuel Utilisateur](./docs/Manuel_Utilisateur.md)
