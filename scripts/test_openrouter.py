import os
import sys
import django
from dotenv import load_dotenv

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduquiz_project.settings')
django.setup()

from quiz.services import QuizGeneratorService

def test_generation():
    print("--- Test de Génération de Quiz via OpenRouter ---")
    service = QuizGeneratorService()
    
    if not service.use_openrouter:
        print("ERREUR : OpenRouter n'est pas configuré. Vérifiez votre fichier .env")
        return

    sample_text = """
    L'intelligence artificielle (IA) est un processus d'imitation de l'intelligence humaine qui repose sur la création et l'application d'algorithmes exécutés dans un environnement informatique dynamique. Son but est de permettre à des ordinateurs de penser et d'agir comme des êtres humains.
    """
    
    print("Envoi de la requête à OpenRouter...")
    try:
        quiz = service.generate_quiz(sample_text, num_questions=2, difficulty="Standard")
        if quiz and len(quiz) > 0:
            print(f"SUCCÈS : {len(quiz)} questions générées.")
            for i, q in enumerate(quiz):
                print(f"\nQuestion {i+1}: {q['question']}")
                print(f"Options: {q['options']}")
                print(f"Réponse: {q['answer']}")
        else:
            print("ÉCHEC : Aucun quiz généré (probablement le fallback regex).")
    except Exception as e:
        print(f"ERREUR lors du test : {e}")

if __name__ == "__main__":
    test_generation()
