"""
Script de test rapide pour vérifier que l'application fonctionne en mode local.
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.quiz_generator import QuizGenerator
from src.config import USE_OPENAI

print("=" * 70)
print("🧪 TEST DU MODE LOCAL (SANS OPENAI)")
print("=" * 70)

# Vérifier la configuration
print(f"\n📊 Configuration actuelle:")
print(f"   USE_OPENAI = {USE_OPENAI}")

if USE_OPENAI:
    print("\n⚠️ ATTENTION: Le mode OpenAI est encore activé!")
    print("   Modifiez src/config.py : USE_OPENAI = False")
    sys.exit(1)

print("   ✅ Mode local activé")

# Tester la génération de quiz
print("\n🔧 Test de génération de quiz...")

text_sample = """
L'intelligence artificielle (IA) est un domaine de l'informatique qui vise à créer des machines 
capables de réaliser des tâches nécessitant normalement l'intelligence humaine. Les applications 
de l'IA incluent la reconnaissance vocale, la vision par ordinateur et le traitement du langage 
naturel. Le machine learning est une branche importante de l'IA qui permet aux ordinateurs 
d'apprendre à partir de données sans être explicitement programmés. Les réseaux de neurones 
artificiels s'inspirent du fonctionnement du cerveau humain pour résoudre des problèmes complexes.
"""

try:
    generator = QuizGenerator()
    quiz = generator.generate_quiz(text_sample, num_questions=3, difficulty="Standard")
    
    if quiz and len(quiz) > 0:
        print(f"   ✅ Quiz généré avec succès ({len(quiz)} questions)")
        print("\n📝 Exemple de question générée:")
        print(f"   Q: {quiz[0]['question'][:80]}...")
        print(f"   Options: {len(quiz[0]['options'])} choix")
        print(f"   Réponse: {quiz[0]['answer']}")
        
        print("\n" + "=" * 70)
        print("🎉 L'APPLICATION FONCTIONNE EN MODE LOCAL !")
        print("=" * 70)
        print("\n💡 Vous pouvez maintenant lancer l'application:")
        print("   streamlit run app.py")
        print()
        
    else:
        print("   ⚠️ Aucune question générée")
        
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
