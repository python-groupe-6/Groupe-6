import os
import database
import sys

# Forcer l'encodage UTF-8 pour la console
sys.stdout.reconfigure(encoding='utf-8')

print("--- Test Final de Résilience EduQuiz ---")
try:
    print("1. Initialisation de la DB...")
    # Ceci va créer le fichier sqlite si postgres échoue
    success = database.init_database()
    if success:
        print("   ✅ Init succès.")
    else:
        print("   ❌ Echec Init.")
    
    mode = database.get_db_mode()
    print(f"   Mode détecté : {mode}")
    
    if mode == "SQLite":
        db_path = os.path.join(os.path.dirname(os.path.abspath(database.__file__)), 'db.sqlite3')
        if os.path.exists(db_path):
             print(f"   ✅ Fichier SQLite verifié : {db_path}")
        else:
             print("   ❌ Fichier SQLite NON trouvé sur le disque !")
    elif mode == "PostgreSQL":
        print("   ✅ Mode PostgreSQL actif.")
    
    print("2. Test d'insertion de score...")
    # Insertion d'un score fictif
    res = database.save_score(100, "0m 10s", 5, "TestVerification")
    if res:
         print("   ✅ Insertion OK.")
    else:
         print("   ❌ Echec Insertion.")
    
    print("3. Lecture de l'historique...")
    history = database.get_score_history(1)
    if history:
        last = history[0]
        print(f"   Dernier score : {last['score']}% ({last['difficulty']})")
        if last['difficulty'] == "TestVerification":
             print("   ✅ Données cohérentes.")
        else:
             print("   ⚠️ Données lues mais différentes du test.")
    else:
        print("   ❌ Historique vide ou erreur lecture.")

except Exception as e:
    print(f"❌ ERREUR CRITIQUE DANS LE SCRIPT : {e}")
