"""
Script de test pour vérifier la configuration de l'API Google Gemini
"""

import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_api_configuration():
    """Tester la configuration de l'API"""
    
    print("🔍 Vérification de la configuration API Gemini...\n")
    
    # 1. Vérifier la présence de la clé API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERREUR: GOOGLE_API_KEY non trouvée dans .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...{api_key[-4:]}")
    
    # 2. Vérifier le modèle
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    print(f"✅ Modèle configuré: {model_name}")
    
    # 3. Tester l'import de google-generativeai
    try:
        import google.generativeai as genai
        print("✅ Module google-generativeai importé avec succès")
    except ImportError:
        print("❌ ERREUR: Module google-generativeai non installé")
        print("   Exécutez: pip install google-generativeai")
        return False
    
    # 4. Tester la connexion à l'API
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        print("✅ Connexion à l'API Gemini réussie")
        
        # 5. Test simple de génération
        print("\n🧪 Test de génération de contenu...")
        response = model.generate_content("Dis bonjour en une phrase courte.")
        print(f"✅ Réponse reçue: {response.text[:100]}...")
        
        print("\n✅ ✅ ✅ TOUS LES TESTS RÉUSSIS ! ✅ ✅ ✅")
        print("\n📝 Votre configuration est prête pour générer des quiz !")
        return True
        
    except Exception as e:
        print(f"❌ ERREUR lors du test de l'API: {str(e)}")
        print("\n🔧 Solutions possibles:")
        print("   1. Vérifiez que votre clé API est valide")
        print("   2. Activez l'API Generative Language dans Google Cloud Console")
        print("   3. Vérifiez votre connexion Internet")
        return False

if __name__ == "__main__":
    success = test_api_configuration()
    sys.exit(0 if success else 1)
