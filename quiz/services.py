import google.generativeai as genai
import json
import re
import random
from django.conf import settings
import os
from pypdf import PdfReader

from dotenv import load_dotenv

load_dotenv()

# Configuration from environment variables (accessed via os or settings)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

class PDFProcessor:
    @staticmethod
    def extract_text(pdf_file):
        """
        Extracts text from an uploaded PDF file (InMemoryUploadedFile).
        """
        try:
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None

class QuizGeneratorService:
    def __init__(self):
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
        else:
            self.model = None

    def generate_quiz(self, text, num_questions=5, difficulty="Standard"):
        with open("debug_quiz.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- New Quiz Generation ---\n")
            f.write(f"Source text length: {len(text) if text else 0}\n")
            f.write(f"Num questions: {num_questions}, Difficulty: {difficulty}\n")
        
        if self.model:
            result = self._generate_with_gemini(text, num_questions, difficulty)
            with open("debug_quiz.log", "a", encoding="utf-8") as f:
                f.write(f"Gemini output length: {len(result) if result else 0}\n")
            return result
        
        result = self._simple_regex_fallback(text, num_questions)
        with open("debug_quiz.log", "a", encoding="utf-8") as f:
            f.write(f"Fallback output length: {len(result) if result else 0}\n")
        return result

    def _sample_text(self, text, max_chars=4000):
        if len(text) <= max_chars:
            return text
        chunk = max_chars // 3
        return f"{text[:chunk]}\n...\n{text[len(text)//2:len(text)//2+chunk]}\n...\n{text[-chunk:]}"

    def _generate_with_gemini(self, text, num_questions, difficulty):
        prompt = f"""
        Génère un quiz de {num_questions} questions de niveau '{difficulty}' à partir du texte.
        Format JSON strict:
        [
            {{
                "question": "Question ?",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "Pourquoi..."
            }}
        ]
        Texte: {self._sample_text(text)}
        """
        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            with open("debug_quiz.log", "a", encoding="utf-8") as f:
                f.write(f"Gemini Raw Response: {response.text[:200]}...\n")
            return json.loads(response.text)[:num_questions]
        except Exception as e:
            with open("debug_quiz.log", "a", encoding="utf-8") as f:
                f.write(f"Gemini error: {e}\n")
            print(f"Gemini error: {e}")
            return self._simple_regex_fallback(text, num_questions)

    def _simple_regex_fallback(self, text, num_questions):
        """
        Génère un quiz basique à partir du texte si l'IA n'est pas disponible.
        Recherche des segments de texte comme base de questions.
        """
        # Segmentation par ponctuation OU passage à la ligne pour gérer les listes/tableaux
        segments = [s.strip() for s in re.split(r'[.!?\n]', text) if len(s.strip()) > 20]
        
        if not segments:
            # Si vraiment rien, on découpe par blocs de mots
            words = text.split()
            segments = [" ".join(words[i:i+15]) for i in range(0, len(words), 15) if len(words[i:i+15]) > 10]
            
        if not segments:
            segments = ["Le contenu du document est trop court pour générer des questions.", 
                         "L'analyse automatique nécessite un texte plus structuré."]
            
        random.shuffle(segments)
        quiz_data = []
        
        # Collecte de mots pour les distracteurs
        all_words = [w.strip(',.:;()!?') for w in text.split() if len(w) > 4]
        
        for i in range(min(num_questions * 2, len(segments))):
            if len(quiz_data) >= num_questions:
                break
                
            sentence = segments[i]
            words = sentence.split()
            if len(words) < 4: continue
            
            # Choisir un mot à cacher (non trivial)
            target_idx = random.randint(0, len(words)-1)
            target_word = words[target_idx].strip(',.:;()!?')
            
            if len(target_word) < 3: continue
            
            words[target_idx] = "________"
            question_text = " ".join(words)
            
            options = [target_word]
            # Ajouter des distracteurs
            other_words = [w for w in all_words if w.lower() != target_word.lower()]
            if len(other_words) > 3:
                distracts = random.sample(list(set(other_words)), 3)
                options.extend(distracts)
            else:
                options.extend(["Réponse B", "Réponse C", "Réponse D"])
            
            random.shuffle(options)
            
            quiz_data.append({
                "question": question_text,
                "options": options,
                "answer": target_word,
                "explanation": f"Basé sur l'extrait : \"{sentence}\""
            })
            
        return quiz_data
