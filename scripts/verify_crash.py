import sys
import os
import traceback

print("--- Test de Stabilité (Crash Check) ---")

# Mock de streamlit car il n'est pas nécessaire pour tester l'import du backend
import unittest.mock
sys.modules['streamlit'] = unittest.mock.MagicMock()

try:
    print("1. Importation de quiz_generator...")
    import quiz_generator
    print("   ✅ Import réussi.")
    
    print("2. Instanciation de QuizGenerator...")
    qg = quiz_generator.QuizGenerator()
    print("   ✅ Instanciation réussie.")
    
    if qg.nlp is None:
        print("   ⚠️ Mode : Spacy désactivé (Résilience active). L'application fonctionne mais sans NLP local.")
    else:
        print("   ✅ Mode : Spacy actif.")

except Exception as e:
    print(f"❌ ECHEC : L'application plante toujours.")
    print(f"Erreur : {e}")
    traceback.print_exc()
