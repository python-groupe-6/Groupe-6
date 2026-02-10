# Cahier des Charges - EduQuiz AI

## 1. Présentation du Projet
**EduQuiz AI** est une application web intelligente conçue pour automatiser la révision académique. Elle permet de transformer des documents pédagogiques (PDF, DOCX, TXT) en quiz interactifs (QCM) avec des explications détaillées.

## 2. Public Cible (Utilisateurs)
- **Étudiants** : Pour tester leurs connaissances avant un examen.
- **Enseignants** : Pour générer rapidement des supports d'évaluation à partir de leurs cours.
- **Apprenants en autodidacte** : Pour valider leur compréhension d'un sujet technique ou théorique.

## 3. Fonctionnalités Principales
- **Importation Multi-formats** : Support des fichiers PDF, Word (.docx) et texte brut (.txt).
- **Analyse Sémantique** : Extraction des concepts clés via IA (OpenAI) ou NLP local (Spacy).
- **Génération de Quiz Personnalisée** : Choix du nombre de questions et du niveau de difficulté (Standard, Avancé, Expert).
- **Interface Interactive** : Passage du quiz avec feedback immédiat ou différé.
- **Rapports de Performance** : Génération d'un bilan PDF incluant le score, les bonnes réponses et des explications pédagogiques.
- **Révision par Flashcards** : Mode mémo pour la mémorisation active.

## 4. Spécifications Techniques
- **Langage** : Python 3.9+
- **Framework Web** : Streamlit (Interface réactive et moderne).
- **Traitement de texte** : PyPDF, python-docx.
- **Intelligence Artificielle** : API OpenAI (GPT) avec fallback local Spacy.
- **Design** : CSS personnalisé, Glassmorphism, Google Fonts (Plus Jakarta Sans).

## 5. Objectifs de Qualité
- **Accessibilité** : Interface intuitive ne nécessitant pas de formation préalable.
- **Rapidité** : Génération d'un quiz en moins de 10 secondes.
- **Fiabilité** : Gestion robuste des erreurs d'encodage et des fichiers corrompus.
