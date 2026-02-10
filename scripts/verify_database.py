"""
Script de vérification de la configuration de la base de données.
Teste la connexion PostgreSQL et le fallback SQLite.
"""

import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_connection, get_db_mode, get_stats, get_score_history, init_database

def test_database():
    """Teste la connexion et les fonctionnalités de la base de données."""
    
    print("=" * 60)
    print("🔍 VÉRIFICATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    # 1. Test de connexion
    print("\n1️⃣ Test de connexion...")
    conn, db_type = get_connection()
    if conn:
        print(f"   ✅ Connexion réussie")
        print(f"   📊 Type de base: {get_db_mode()}")
        conn.close()
    else:
        print("   ❌ Échec de connexion")
        return False
    
    # 2. Test d'initialisation
    print("\n2️⃣ Test d'initialisation de la table...")
    if init_database():
        print("   ✅ Table score_history initialisée")
    else:
        print("   ❌ Erreur lors de l'initialisation")
        return False
    
    # 3. Test de récupération des statistiques
    print("\n3️⃣ Test de récupération des statistiques...")
    stats = get_stats()
    if stats:
        print(f"   ✅ Statistiques récupérées:")
        print(f"      • Total de quiz: {stats['total_quizzes']}")
        print(f"      • Score moyen: {stats['avg_score']}")
        print(f"      • Meilleur score: {stats['best_score']}")
    else:
        print("   ⚠️ Aucune statistique disponible (base vide)")
    
    # 4. Test de récupération de l'historique
    print("\n4️⃣ Test de récupération de l'historique...")
    history = get_score_history(limit=5)
    if history:
        print(f"   ✅ {len(history)} entrées récupérées")
        for i, entry in enumerate(history[:3], 1):
            print(f"      {i}. Score: {entry['score']}, Date: {entry['date']}")
    else:
        print("   ⚠️ Aucun historique disponible (base vide)")
    
    print("\n" + "=" * 60)
    print("✅ VÉRIFICATION TERMINÉE AVEC SUCCÈS")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
