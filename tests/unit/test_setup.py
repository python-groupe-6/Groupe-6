#!/usr/bin/env python
"""
Script de test pour EduQuiz AI
Vérifie que la configuration est correcte avant de lancer l'app
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Vérifie l'environnement"""
    print("🔍 Vérification de l'environnement...\n")
    
    errors = []
    warnings = []
    
    # 1. Vérifie Python version
    print(f"✓ Python: {sys.version}")
    if sys.version_info < (3, 9):
        errors.append("Python 3.9+ requis")
    
    # 2. Vérifie .env existe
    print("2️⃣ Fichier .env:")
    if os.path.exists(".env"):
        print("   ✅ .env trouvé")
    else:
        print("   ⚠️ .env non trouvé")
        print("   → Crée un fichier .env avec:")
        print("     GOOGLE_API_KEY=ta_cle_ici")
        warnings.append(".env manquant")
    
    # 3. Vérifie les env vars
    print("\n3️⃣ Variables d'environnement:")
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        errors.append("GOOGLE_API_KEY non définie")
        print("   ❌ GOOGLE_API_KEY: NON DÉFINIE")
    elif api_key.startswith("ta_cle") or api_key.startswith("votre"):
        errors.append("GOOGLE_API_KEY contient un placeholder")
        print("   ❌ GOOGLE_API_KEY: PLACEHOLDER")
    else:
        key_preview = f"{api_key[:10]}...{api_key[-5:]}"
        print(f"   ✅ GOOGLE_API_KEY: {key_preview}")
    
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    print(f"   ✅ GEMINI_MODEL: {model}")
    
    # 4. Vérifie les dépendances
    print("\n4️⃣ Dépendances Python:")
    dependencies = [
        "streamlit",
        "google.generativeai",
        "dotenv",
        "pandas",
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep.replace(".generativeai", "google.generativeai").replace("dotenv", "dotenv"))
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep}")
            missing.append(dep)
    
    if missing:
        errors.append(f"Dépendances manquantes: {', '.join(missing)}")
        print(f"\n   → Installe avec: pip install {' '.join(missing)}")
    
    # 5. Vérifie la structure du projet
    print("\n5️⃣ Fichiers du projet:")
    required_files = [
        "app.py",
        "quiz_generator.py",
        ".env",
        "requirements_streamlit.txt"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ⚠️ {file} manquant")
            if file == ".env":
                warnings.append(f"{file} manquant")
    
    # 6. Test la connexion Google
    print("\n6️⃣ Test de connexion Google Gemini:")
    if api_key and not api_key.startswith("ta_cle"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            print("   ✅ Connexion Google réussie")
        except Exception as e:
            errors.append(f"Erreur connexion Google: {str(e)}")
            print(f"   ❌ Erreur: {e}")
    else:
        print("   ⏭️  Skipped (clé non configurée)")
    
    # 7. Résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ")
    print("="*50)
    
    if errors:
        print(f"\n❌ {len(errors)} ERREUR(S):")
        for err in errors:
            print(f"   • {err}")
    
    if warnings:
        print(f"\n⚠️ {len(warnings)} AVERTISSEMENT(S):")
        for warn in warnings:
            print(f"   • {warn}")
    
    if not errors:
        print("\n✅ TOUS LES VÉRIFICATIONS PASSÉES!")
        print("\nTu peux maintenant lancer:")
        print("   streamlit run app.py")
        return 0
    else:
        print("\n❌ CORRIGE LES ERREURS ET RÉESSAYE")
        return 1

def test_quiz_generator():
    """Test le module de génération"""
    print("\n" + "="*50)
    print("🧪 TEST DU GÉNÉRATEUR")
    print("="*50)
    
    try:
        from quiz_generator import generate_quiz
        
        print("\n📝 Test: Génération d'un petit quiz...")
        result = generate_quiz("Test Python", "Débutant", 1)
        
        if result and result.get("success"):
            print("✅ Quiz généré avec succès!")
            print(f"   Question: {result['questions'][0]['question']}")
            return 0
        else:
            print("❌ Erreur de génération:")
            print(f"   {result.get('error', 'Erreur inconnue')}")
            return 1
    
    except Exception as e:
        print(f"❌ Erreur du test: {e}")
        return 1

if __name__ == "__main__":
    # Vérifie l'environnement
    exit_code = check_environment()
    
    if exit_code == 0:
        # Test optionnel la génération
        response = input("\n🤔 Veux-tu tester la génération de quiz? (y/n): ").lower()
        if response in ("y", "yes", "oui"):
            test_quiz_generator()
    
    sys.exit(exit_code)
