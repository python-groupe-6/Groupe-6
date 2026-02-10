# Migration PostgreSQL - Guide Complet

## 📋 Vue d'ensemble

EduQuiz AI utilise maintenant **PostgreSQL** comme base de données principale avec un **fallback automatique vers SQLite** pour le développement local.

## 🎯 Avantages de PostgreSQL

- ✅ **Performance** : Meilleure gestion des requêtes concurrentes
- ✅ **Scalabilité** : Support de grandes quantités de données
- ✅ **Fiabilité** : Transactions ACID complètes
- ✅ **Fonctionnalités avancées** : Types de données riches, indexation performante

## 🔧 Configuration

### 1. Prérequis

- PostgreSQL 12+ installé
- Accès administrateur à PostgreSQL
- Fichier `.env` configuré

### 2. Configuration du fichier `.env`

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=eduquiz_db
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
```

### 3. Création de la base de données

```sql
-- Dans pgAdmin ou psql
CREATE DATABASE eduquiz_db;
```

## 🚀 Migration des données

### Étape 1 : Vérifier la connexion

```bash
python scripts/verify_database.py
```

### Étape 2 : Migrer les données SQLite vers PostgreSQL

```bash
python scripts/migrate_to_postgres.py
```

Le script va :
1. Se connecter à PostgreSQL
2. Créer la table `score_history` si elle n'existe pas
3. Récupérer toutes les données de SQLite
4. Les insérer dans PostgreSQL

### Étape 3 : Vérifier la migration

```bash
python scripts/verify_database.py
```

## 🔄 Fonctionnement du Fallback

Le module `src/database.py` implémente un système de fallback automatique :

1. **Tentative PostgreSQL** : Si les credentials sont configurés dans `.env`
2. **Fallback SQLite** : Si PostgreSQL n'est pas disponible ou mal configuré

```python
from src.database import get_db_mode

# Vérifier le mode actuel
print(get_db_mode())  # "PostgreSQL" ou "SQLite"
```

## 📊 Structure de la base de données

### Table `score_history`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | SERIAL/INTEGER | Clé primaire auto-incrémentée |
| `score` | INTEGER | Score obtenu (0-100) |
| `time_elapsed` | VARCHAR(50) | Temps écoulé (format: "Xmin Ys") |
| `quiz_date` | TIMESTAMP | Date et heure du quiz |
| `num_questions` | INTEGER | Nombre de questions |
| `difficulty` | VARCHAR(50) | Niveau de difficulté |

## 🛠️ Scripts disponibles

### `scripts/migrate_to_postgres.py`
Migre les données de SQLite vers PostgreSQL.

**Usage :**
```bash
python scripts/migrate_to_postgres.py
```

### `scripts/verify_database.py`
Vérifie la connexion et teste toutes les opérations de base de données.

**Usage :**
```bash
python scripts/verify_database.py
```

## ⚠️ Dépannage

### Erreur : "password authentication failed"

**Solution :**
1. Vérifiez le mot de passe dans `.env`
2. Assurez-vous qu'il n'y a pas de guillemets autour du mot de passe
3. Vérifiez que l'utilisateur `postgres` existe

### Erreur : "database does not exist"

**Solution :**
```sql
CREATE DATABASE eduquiz_db;
```

### L'application utilise SQLite au lieu de PostgreSQL

**Solution :**
1. Vérifiez que PostgreSQL est démarré
2. Vérifiez les credentials dans `.env`
3. Testez la connexion avec `scripts/verify_database.py`

## 🔐 Sécurité

> [!WARNING]
> Ne commitez JAMAIS le fichier `.env` dans Git. Il contient des informations sensibles.

Le fichier `.gitignore` doit contenir :
```
.env
*.env
```

## 📈 Performance

### Optimisations recommandées

1. **Index sur quiz_date** :
```sql
CREATE INDEX idx_quiz_date ON score_history(quiz_date DESC);
```

2. **Index sur score** :
```sql
CREATE INDEX idx_score ON score_history(score);
```

## 🔄 Retour à SQLite

Si vous souhaitez revenir à SQLite temporairement :

1. Commentez les variables dans `.env` :
```env
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=eduquiz_db
# DB_USER=postgres
# DB_PASSWORD=votre_mot_de_passe
```

2. L'application basculera automatiquement sur SQLite

## ✅ Checklist de migration

- [x] PostgreSQL installé et configuré
- [x] Base de données `eduquiz_db` créée
- [x] Fichier `.env` configuré
- [x] Script de migration exécuté
- [x] Vérification réussie
- [x] Application testée avec PostgreSQL

## 📞 Support

En cas de problème, vérifiez :
1. Les logs de PostgreSQL
2. Le fichier `.env`
3. La sortie de `scripts/verify_database.py`
