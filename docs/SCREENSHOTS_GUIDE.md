# Guide de Capture de Screenshots - EduQuiz AI

Ce guide vous explique comment capturer et ajouter des screenshots professionnels au README.

## Prérequis

- Application EduQuiz AI en cours d'exécution
- Navigateur web (Chrome, Firefox, Edge recommandés)
- Outil de capture d'écran

## Étapes de Capture

### 1. Préparer l'Environnement

```bash
# Lancer le serveur
python manage.py runserver

# Créer le dossier screenshots
mkdir -p docs/screenshots
```

### 2. Pages à Capturer

| # | Page | URL | Fichier |
|---|------|-----|---------|
| 1 | Accueil | http://127.0.0.1:8000/ | homepage.png |
| 2 | Inscription | http://127.0.0.1:8000/auth/register/ | register.png |
| 3 | Connexion | http://127.0.0.1:8000/auth/login/ | login.png |
| 4 | Config Quiz | http://127.0.0.1:8000/quiz/setup/ | quiz_setup.png |
| 5 | Quiz | http://127.0.0.1:8000/quiz/take/<id>/ | quiz_take.png |
| 6 | Résultats | http://127.0.0.1:8000/quiz/result/<id>/ | quiz_results.png |
| 7 | Historique | http://127.0.0.1:8000/quiz/history/ | quiz_history.png |
| 8 | Mode Sombre | (Activer mode sombre) | dark_mode.png |

### 3. Outils de Capture

**Windows :**
- `Windows + Shift + S` - Outil intégré
- Snagit - Professionnel
- Greenshot - Gratuit

**macOS :**
- `Cmd + Shift + 4` - Outil intégré
- Skitch - Gratuit
- CleanShot X - Professionnel

**Extensions Navigateur :**
- Awesome Screenshot
- Fireshot
- Nimbus Screenshot

### 4. Paramètres Recommandés

- **Résolution :** 1920x1080 minimum
- **Format :** PNG (meilleure qualité)
- **Taille :** < 500 KB par image
- **Mode :** Plein écran pour cohérence

### 5. Optimisation des Images

```python
# Script d'optimisation (optionnel)
from PIL import Image
import os

def optimize_screenshot(input_path, output_path, max_width=1200):
    img = Image.open(input_path)
    
    # Redimensionner si nécessaire
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    
    # Sauvegarder avec optimisation
    img.save(output_path, optimize=True, quality=85)
    print(f"✅ Optimisé: {output_path}")

# Utilisation
for file in os.listdir('docs/screenshots'):
    if file.endswith('.png'):
        optimize_screenshot(
            f'docs/screenshots/{file}',
            f'docs/screenshots/{file}'
        )
```

### 6. Checklist de Qualité

Avant de commit, vérifiez :

- [ ] Toutes les 8 pages sont capturées
- [ ] Images en haute résolution (1920x1080+)
- [ ] Pas de données personnelles sensibles
- [ ] Pas d'erreurs visibles
- [ ] Noms de fichiers corrects
- [ ] Images optimisées (< 500 KB)
- [ ] Mode clair ET mode sombre capturés

### 7. Ajouter au Git

```bash
# Vérifier les fichiers
ls -lh docs/screenshots/

# Ajouter au repository
git add docs/screenshots/
git commit -m "Docs: Ajout des screenshots de l'application"
git push origin main
```

## Conseils Professionnels

### ✅ Bonnes Pratiques

1. **Cohérence Visuelle**
   - Utilisez les mêmes données de test
   - Même résolution pour toutes les captures
   - Même thème (clair ou sombre)

2. **Données de Démonstration**
   - Créez un compte "demo@eduquiz.ai"
   - Utilisez des quiz de démonstration
   - Remplissez avec des données réalistes

3. **Timing**
   - Capturez quand l'UI est stable
   - Attendez le chargement complet
   - Pas d'animations en cours

### ❌ À Éviter

- Screenshots flous ou pixelisés
- Données personnelles réelles
- Erreurs ou messages d'erreur
- Captures partielles
- Résolution trop faible

## Résultat Final

Une fois terminé, votre dossier devrait ressembler à :

```
docs/screenshots/
├── homepage.png          (Page d'accueil)
├── register.png          (Inscription)
├── login.png             (Connexion)
├── quiz_setup.png        (Configuration)
├── quiz_take.png         (Interface quiz)
├── quiz_results.png      (Résultats)
├── quiz_history.png      (Historique)
└── dark_mode.png         (Mode sombre)
```

Les images seront automatiquement affichées dans le README !
