# 📊 Bilan du Projet EduQuiz AI : Problématiques, Difficultés et Améliorations

Ce document récapitule les défis techniques rencontrés lors du développement d'EduQuiz AI, les solutions apportées et les pistes d'amélioration pour le futur.

---

## 🛠 1. Problématiques Techniques Majeures

### 📄 Génération de Flashcards PDF (Cœur de Métier)
- **Problème** : Rupture de la fonctionnalité d'exportation après la mise à jour de la bibliothèque `fpdf` vers `fpdf2`.
- **Difficulté** : Incompatibilités de syntaxe (gestion des flux d'octets `output()`) et de polices standards (`Arial` indisponible par défaut dans certains environnements).
- **Résolution** : Migration technique vers `fpdf2` avec ajustement des appels système et passage à la police `helvetica`.

### 🤖 Intégration de l'IA (Google Gemini)
- **Problème** : Interruptions fréquentes du service de génération de quiz.
- **Difficulté** : 
    - **Quotas (Erreur 429)** : Dépassement des limites du "Free Tier" de Google Gemini (requêtes par minute et par jour).
    - **Configuration (Erreur 404)** : Tentatives d'utilisation de modèles non supportés ou mal nommés dans les paramètres.
- **Impact** : Expérience utilisateur dégradée (échecs de génération).

### 👤 Gestion du Profil et Médias
- **Problème** : Erreurs de chargement (crash) de la page profil et absence d'avatars personnalisables.
- **Difficulté** : Oublis d'imports (`NameError`), configuration complexe du stockage des médias (`MEDIA_ROOT` / `MEDIA_URL`) et gestion de l'upload asynchrone via JavaScript.
- **Résolution** : Mise en place de `Pillow`, création d'une interface de prévisualisation instantanée et correction des vues Django.

---

## 🚀 2. Difficultés de Développement et Déploiement

### 🌐 Déploiement sur Render
- **Cold Start** : Latence importante (~30s) au premier chargement sur l'instance gratuite.
- **Timeouts** : Risque d'erreurs 504 lors de générations de quiz volumineux dépassant le temps de réponse autorisé par Render.
- **Gestion des Secrets** : Nécessité de migrer toutes les configurations sensibles (`API_KEY`) vers les secrets Render pour éviter les fuites sur GitHub.

### 🏗 Build et Environnement
- **JavaFX/Maven** : Avertissements de build et conflits de versions rencontrés lors des phases d'outillage ou de modules secondaires.
- **Environnement Virtuel** : Nécessité de maintenir un fichier `requirements.txt` strict suite à l'ajout régulier de dépendances (`fpdf2`, `Pillow`, `python-dotenv`).

---

## 🎨 3. Expérience Utilisateur et UI

### 🧼 Simplification de l'Interface
- **Problème** : Interface "encombrée" par des fonctions expérimentales complexes.
- **Remarque** : L'onglet "Révision SRS" a été supprimé pour épurer le dashboard et se concentrer sur les fonctionnalités de base les plus robustes.

### 📚 Bibliothèque Publique
- **Difficulté** : La persistance de l'ID du quiz lors du passage de la bibliothèque à la vue "Take Quiz" via la session client était peu fiable.
- **Optimisation** : Passage à un routage direct via URL (`/take/<int:quiz_id>/`) pour une robustesse accrue.

---

## 📈 4. Points d'Amélioration Recommandés

### 🧠 Optimisation de l'IA 
- **Caching** : Implémenter un système de cache pour les quiz populaires afin de limiter les appels à l'API Gemini et économiser les quotas.
- **Fallback** : Prévoir un "Retry Mechanism" ou un modèle de secours plus léger en cas de saturation des quotas.

### ⚡ Performance
- **Tâches de Fond (Celery)** : Déporter la génération de quiz (longue) dans une tâche asynchrone pour éviter les timeouts HTTP 504 sur Render.

### 🛂 Sécurité et Robustesse
- **Validation Multimodal** : Renforcer la validation des fichiers OCR (Photos) et des liens YouTube pour éviter les plantages lors de la lecture des sources.
- **Guide de Sécurité** : Maintenir le `SECURITY_GUIDE.md` à jour, notamment pour les restrictions d'API Key Google Cloud.

### 📖 Documentation Visuelle
- Continuer l'effort d'intégration des captures d'écran dans le `Cahier des Charges` pour faciliter l'onboarding des nouveaux contributeurs.
