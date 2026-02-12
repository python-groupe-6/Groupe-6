# 🚀 Guide de Déploiement - EduQuiz AI sur Render

## 📋 Prérequis

- Compte [Render.com](https://render.com)
- Compte [Google Cloud Console](https://console.cloud.google.com)
- Clé API Google Gemini valide
- Repository GitHub avec le code

## 🔧 Étape 1: Configurer Google Gemini API

### 1.1 Crée un projet Google Cloud
1. Va sur [Google Cloud Console](https://console.cloud.google.com)
2. Crée un nouveau projet
3. Actif l'API **Google Generative AI**

### 1.2 Génère une clé API
1. Va dans **APIs & Services → Credentials**
2. Clique **Create Credentials → API Key**
3. Copie ta clé (format: `AIzaSy...`)
4. **Ne partage JAMAIS cette clé publiquement**

### 1.3 Configure les restrictions (optionnel mais recommandé)
1. Clique sur ta clé dans Credentials
2. Ajoute des restrictions:
   - **API restriction**: "Google Generative AI"
   - **Application restriction**: HTTP referrer (domaine Render)

---

## 🌐 Étape 2: Déployer sur Render

### 2.1 Prépare ton repository GitHub

Assure-toi que ton repo contient:
```
.gitignore          ← Contient .env
.env.example        ← Exemple de variables d'environnement
app.py              ← Application Streamlit
quiz_generator.py   ← Module de génération
requirements_streamlit.txt  ← Dépendances
README.md           ← Documentation
```

Vérifie que `.env` est dans `.gitignore`:
```bash
# Dans .gitignore
.env
.env.local
```

### 2.2 Push ton code sur GitHub

```bash
git add .
git commit -m "Initial commit: EduQuiz AI"
git push origin main
```

git add .
git commit -m "Ajout des modifications sur les thèmes de sécurité"
git push origin main

### 2.3 Déploie sur Render

1. Va sur [Render Dashboard](https://dashboard.render.com)
2. Clique **+ New → Web Service**
3. **Connect ta repo GitHub**
4. Configure le service:

```
Service Name:       eduquiz-ai
Repository:         [Sélectionne ton repo]
Branch:            main
Runtime:           Python 3.11
Build Command:     pip install -r requirements_streamlit.txt
Start Command:     streamlit run app.py --server.port=10000 --server.address=0.0.0.0
```

### 2.4 Ajoute les variables d'environnement

**Dans Render Dashboard:**
1. Clique sur ton service → **Environment**
2. Ajoute les variables:

| Clé | Valeur |
|-----|--------|
| `GOOGLE_API_KEY` | `AIzaSy...` (ta vraie clé) |
| `GEMINI_MODEL` | `gemini-2.0-flash` |

⚠️ **Ne mets JAMAIS de vraie clé en clair!** Render propose des secrets.

### 2.5 Lance le déploiement

1. Clique **Create Web Service**
2. Attends ~2-5 minutes pour le déploiement
3. Une URL sera générée: `https://eduquiz-ai.onrender.com`

---

## ✅ Vérification Post-Déploiement

### Teste ton app:
1. Accède à `https://ton-app.onrender.com`
2. Génère un quiz de test
3. Vérifie les logs en cas d'erreur

### Affiche les logs:
```
Render Dashboard → Ton service → Logs
```

---

## 🔐 Sécurité - Best Practices

### ✅ À FAIRE:
- ✅ Utiliser des **secrets Render** pour les clés API
- ✅ Ajouter `.env` à `.gitignore`
- ✅ Créer `.env.example` sans vraie clé
- ✅ Utiliser des clés d'API **restrictives** (IP, API limits)
- ✅ Monitorer la consommation (quotas Google)
- ✅ Activer les logs pour détecter les abus

### ❌ À ÉVITER:
- ❌ Ne JAMAIS committer `.env`
- ❌ Ne partage jamais ta clé API
- ❌ Ne laisse pas de clés en clair dans le code
- ❌ Ne teste pas directement avec des données sensibles

---

## 🐛 Troubleshooting

### Erreur: "Clé API invalide"
```
Solution:
1. Vérifie la clé dans Render → Environment
2. Assure-toi qu'elle est exactement identique à celle de Google Cloud
3. Redis les logs Render
```

### Erreur: "504 Gateway Timeout"
```
Solution:
1. Réduisez le nombre de questions
2. Utilise un modèle plus léger si disponible
3. Augmente le timeout dans resources Render
```

### Erreur: "Quota exceeded"
```
Solution:
1. Attends 1 heure avant de réessayer
2. Configure les quotas dans Google Cloud Console
3. Considère un plan payant Google
```

### Cold Start lent (~30s)
```
Normal sur Render (free tier). Solutions:
1. Upgrade vers un plan payant
2. Maintiene ton app active (keep-alive)
3. Optimise size du bundle (pip install -U)
```

---

## 📊 Monitoring

### Sur Render:
- **Metrics**: CPU, mémoire, requêtes
- **Logs**: Erreurs et événements
- **Alerts**: Configurer notifications

### Commandes utiles:

```bash
# Test local avant déploiement
streamlit run app.py

# Vérifier les logs
curl https://ton-app.onrender.com/api/health

# Voir les variables d'env (ne pas afficher les secrets!)
printenv | grep -v SECRET
```

---

## 💰 Coûts

### Google Gemini API:
- **Gratuit**: 60 appels/minute (Free tier)
- **Payant**: $0.075 pour 1M input tokens
- Monitor usage: [Google Cloud Console](https://console.cloud.google.com/billing)

### Render:
- **Free tier**: 750 heures/mois
- **Paid**: À partir de $7/mois

---

## 🔄 Mises à Jour

### Pour mettre à jour l'app:

```bash
# Localement
git add .
git commit -m "Feature: Nouvelle amélioration"
git push origin main

# Render re-déploira automatiquement
# Vérifie les logs pour confirmee
```

---

## 📚 Ressources

- [Render Docs](https://render.com/docs)
- [Streamlit Deployment](https://docs.streamlit.io/deploy)
- [Google Gemini API](https://ai.google.dev/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 🎯 Checklist Final

- [ ] Clé API Google Gemini générée et testée
- [ ] `.env` ajouté à `.gitignore`
- [ ] `.env.example` créé sans vraie clé
- [ ] `requirements_streamlit.txt` à jour
- [ ] Code pushé sur GitHub
- [ ] Service Render créé
- [ ] Variables d'env configurées dans Render
- [ ] Déploiement réussi
- [ ] App accessible et fonctionnelle
- [ ] Quotas Google Gemini monitorés

**🚀 Bon déploiement! Si tu as des questions, consulta la doc Render ou Google Cloud.**
