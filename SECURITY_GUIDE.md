# 🔐 Guide de Sécurité - EduQuiz AI

## 📋 Table des matières
1. [Configuration de la clé API](#configuration-de-la-clé-api)
2. [Sécurisation de la clé](#sécurisation-de-la-clé)
3. [Déploiement sur Render](#déploiement-sur-render)
4. [Bonnes pratiques](#bonnes-pratiques)

---

## 🔑 Configuration de la clé API

### Fichier `.env` (Local)
Votre clé API est stockée dans le fichier `.env` :

```bash
GOOGLE_API_KEY=AIzaSyDvmCe0zWVrUv6uBseSakXyPxzt_EmolV8
GEMINI_MODEL=gemini-2.0-flash
```

> ⚠️ **IMPORTANT** : Ce fichier ne doit **JAMAIS** être commité sur GitHub !

### Vérification `.gitignore`
Assurez-vous que `.env` est bien dans votre `.gitignore` :

```bash
# Environment Variables - NEVER COMMIT
.env
.env.local
.env.*.local
```

✅ **Statut actuel** : Votre `.gitignore` est correctement configuré.

---

## 🛡️ Sécurisation de la clé

### 1. Restrictions dans Google Cloud Console

Pour sécuriser votre clé API, suivez ces étapes :

1. **Accédez à Google Cloud Console**
   - URL : https://console.cloud.google.com/apis/credentials
   - Connectez-vous avec votre compte Google

2. **Sélectionnez votre clé API**
   - Cliquez sur votre clé : `AIzaSyDvmCe0zWVrUv6uBseSakXyPxzt_EmolV8`

3. **Ajoutez des restrictions d'API**
   - Dans "API restrictions", sélectionnez **"Restrict key"**
   - Cochez uniquement : **Generative Language API**
   - Cliquez sur **"Save"**

4. **Restrictions d'application (Optionnel mais recommandé)**
   
   **Pour le développement local** :
   - Sélectionnez "IP addresses"
   - Ajoutez : `127.0.0.1` (localhost)
   
   **Pour la production (Render)** :
   - Créez une clé API séparée pour la production
   - Ajoutez les IP de Render (voir section Déploiement)

### 2. Surveillance de l'utilisation

- **Quotas** : Vérifiez régulièrement votre utilisation
  - URL : https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
  
- **Alertes** : Configurez des alertes de quota
  - Définissez un seuil (ex: 80% du quota)
  - Recevez des notifications par email

---

## 🚀 Déploiement sur Render

### Configuration des variables d'environnement

1. **Accédez à votre dashboard Render**
   - URL : https://dashboard.render.com/

2. **Sélectionnez votre service**
   - Cliquez sur votre application EduQuiz AI

3. **Ajoutez les variables d'environnement**
   - Allez dans **"Environment"** → **"Environment Variables"**
   - Ajoutez :

   ```
   GOOGLE_API_KEY=AIzaSyDvmCe0zWVrUv6uBseSakXyPxzt_EmolV8
   GEMINI_MODEL=gemini-2.0-flash
   ```

4. **Sauvegardez et redéployez**
   - Cliquez sur **"Save Changes"**
   - Render redéploiera automatiquement votre application

### Fichier `render.yaml` (Optionnel)

Si vous utilisez un fichier `render.yaml`, ajoutez :

```yaml
services:
  - type: web
    name: eduquiz-ai
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python manage.py runserver 0.0.0.0:$PORT"
    envVars:
      - key: GOOGLE_API_KEY
        sync: false  # Ne pas synchroniser depuis le repo
      - key: GEMINI_MODEL
        value: gemini-2.0-flash
```

> ⚠️ **Ne mettez JAMAIS la vraie clé dans `render.yaml`** - Configurez-la manuellement dans le dashboard.

---

## ✅ Bonnes pratiques

### 1. Séparation des clés
- **Développement** : Utilisez une clé API différente
- **Production** : Utilisez une clé avec restrictions strictes

### 2. Rotation des clés
- Changez votre clé API tous les 3-6 mois
- Supprimez les anciennes clés après migration

### 3. Gestion des erreurs
Le fichier `quiz_generator.py` gère déjà :
- ✅ Clé API invalide
- ✅ Quota dépassé
- ✅ Erreurs réseau
- ✅ Timeout

### 4. Logs et monitoring
```python
# Les logs sont automatiquement générés
logger.info("✅ Quiz généré avec succès")
logger.error("❌ Erreur: Quota dépassé")
```

### 5. Fallback mechanism
En cas d'échec de l'API Gemini, le système retourne :
```json
{
  "success": false,
  "error": "Description de l'erreur",
  "details": "Informations supplémentaires"
}
```

---

## 🧪 Test de la configuration

### Test local

```bash
# Activez votre environnement virtuel
.venv\Scripts\activate

# Testez le générateur
python quiz_generator.py
```

**Résultat attendu** :
```json
{
  "success": true,
  "theme": "Histoire de France",
  "level": "Débutant",
  "questions": [...]
}
```

### Test dans Django

```python
# Dans votre vue Django
from quiz_generator import generate_quiz

result = generate_quiz("Python", "Intermédiaire", 5)
if result["success"]:
    print("✅ Quiz généré !")
else:
    print(f"❌ Erreur: {result['error']}")
```

---

## 🆘 Dépannage

### Erreur : "Clé API invalide"
- Vérifiez que la clé dans `.env` est correcte
- Assurez-vous que l'API Generative Language est activée

### Erreur : "Quota dépassé"
- Attendez quelques minutes
- Vérifiez votre quota : https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas

### Erreur : "Service indisponible"
- Les serveurs Google sont temporairement surchargés
- Réessayez dans quelques minutes

---

## 📞 Support

- **Documentation Gemini** : https://ai.google.dev/docs
- **Google Cloud Console** : https://console.cloud.google.com/
- **Render Documentation** : https://render.com/docs

---

**Dernière mise à jour** : 2026-02-11
