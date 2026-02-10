"""
Script de diagnostic pour tester la clé API Google Gemini (AI Studio).
Vérifie si la clé fonctionne et affiche le statut.
"""

import os
import sys
from dotenv import load_dotenv
import io

# Charger le .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(env_path):
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(env_path, 'r', encoding='latin-1') as f:
            content = f.read()
    load_dotenv(stream=io.StringIO(content))

print("=" * 70)
print("🔍 DIAGNOSTIC DE LA CLÉ API GOOGLE GEMINI")
print("=" * 70)

# 1. Vérifier que la clé existe
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "YOUR_API_KEY_HERE":
    print("\n❌ Aucune clé API Google Gemini trouvée dans le fichier .env")
    print("\n💡 Solution :")
    print("   1. Ajoutez votre clé dans le fichier .env : GOOGLE_API_KEY=votre_clé")
    print("   2. Obtenez une clé sur : https://aistudio.google.com/app/apikey")
    sys.exit(1)

print(f"\n✅ Clé API trouvée : {api_key[:10]}...{api_key[-4:]}")

# 2. Tester la connexion
print("\n🔌 Test de connexion à Google Gemini...")

try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Faire un appel minimal pour tester
    response = model.generate_content("Dis juste 'OK' en français.")
    
    print("✅ Connexion réussie !")
    print(f"   Réponse de l'API : {response.text.strip()}")
    print("\n" + "=" * 70)
    print("🎉 VOTRE CLÉ GOOGLE GEMINI FONCTIONNE PARFAITEMENT !")
    print("=" * 70)
    
except Exception as e:
    error_msg = str(e)
    print(f"\n❌ Erreur lors de la connexion : {error_msg}")
    
    if "API_KEY_INVALID" in error_msg:
        print("\n❌ La clé API est INVALIDE.")
        print("\n💡 Solution : Vérifiez votre clé sur Google AI Studio.")
    elif "quota" in error_msg.lower():
        print("\n⚠️ Quota dépassé pour le niveau gratuit.")
    else:
        print("\n💡 Vérifiez votre connexion internet ou la configuration de Google AI Studio.")
    
    print("\n" + "=" * 70)
    sys.exit(1)
