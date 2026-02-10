"""
Script pour basculer rapidement entre le mode OpenAI et le mode Local.
Usage: python scripts/switch_mode.py [openai|local]
"""

import sys
import os
import re

def switch_mode(mode):
    """Bascule entre OpenAI et Local en modifiant src/config.py"""
    
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'config.py')
    
    if not os.path.exists(config_path):
        print(f"❌ Fichier config.py introuvable : {config_path}")
        return False
    
    # Lire le fichier
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if mode == "local":
        # Désactiver Gemini
        new_content = re.sub(
            r'USE_GEMINI = True',
            'USE_GEMINI = False',
            content
        )
        mode_name = "LOCAL (Spacy)"
        
    elif mode == "gemini":
        # Activer Gemini
        new_content = re.sub(
            r'USE_GEMINI = False',
            'USE_GEMINI = True',
            content
        )
        mode_name = "GOOGLE GEMINI"
    else:
        print("❌ Mode invalide. Utilisez 'gemini' ou 'local'")
        return False
    
    # Sauvegarder
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("=" * 60)
    print(f"✅ Mode basculé vers : {mode_name}")
    print("=" * 60)
    
    if mode == "local":
        print("\n📦 Vérification de Spacy...")
        try:
            import spacy
            try:
                nlp = spacy.load("fr_core_news_sm")
                print("   ✅ Modèle français Spacy installé")
            except:
                print("   ⚠️ Modèle français manquant")
                print("\n💡 Installation requise :")
                print("   python -m spacy download fr_core_news_sm")
        except ImportError:
            print("   ❌ Spacy non installé")
            print("\n💡 Installation requise :")
            print("   pip install spacy")
            print("   python -m spacy download fr_core_news_sm")
    
    elif mode == "gemini":
        print("\n🔑 Vérification de la clé API...")
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and api_key != "YOUR_API_KEY_HERE":
            print(f"   ✅ Clé API configurée : {api_key[:10]}...")
            print("\n💡 Pour tester la clé :")
            print("   python scripts/test_google_key.py")
        else:
            print("   ⚠️ Clé API non configurée dans .env")
    
    print("\n🚀 Vous pouvez maintenant relancer l'application :")
    print("   streamlit run app.py")
    print()
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("=" * 60)
        print("🔧 SWITCH MODE - EduQuiz AI")
        print("=" * 60)
        print("\nUsage :")
        print("  python scripts/switch_mode.py openai   # Utiliser OpenAI GPT")
        print("  python scripts/switch_mode.py local    # Utiliser Spacy local")
        print()
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    success = switch_mode(mode)
    sys.exit(0 if success else 1)
