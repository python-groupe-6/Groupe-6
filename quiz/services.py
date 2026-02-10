import google.generativeai as genai
import json
import re
import random
from django.conf import settings
import os
from pypdf import PdfReader

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
        if self.model:
            return self._generate_with_gemini(text, num_questions, difficulty)
        return self._simple_regex_fallback(text, num_questions)

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
            return json.loads(response.text)[:num_questions]
        except Exception as e:
            print(f"Gemini error: {e}")
            return self._simple_regex_fallback(text, num_questions)

    def _simple_regex_fallback(self, text, num_questions):
        """
        Génère un quiz basique à partir du texte si l'IA n'est pas disponible.
        Recherche des phrases courtes se terminant par un point comme base de questions.
        """
        # Nettoyage et segmentation simple
        sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 30]
        
        if not sentences:
            sentences = ["Le contenu du document est trop court pour générer des questions.", 
                         "L'analyse automatique nécessite un texte plus structuré."]
            
        random.shuffle(sentences)
        quiz_data = []
        
        for i in range(min(num_questions, len(sentences))):
            sentence = sentences[i]
            # Création d'une question "Trouvez le mot manquant"
            words = sentence.split()
            if len(words) < 5: continue
            
            # Choisir un mot à cacher (non trivial)
            target_idx = random.randint(len(words)//2, len(words)-1)
            target_word = words[target_idx].strip(',.:;()!?')
            
            if len(target_word) < 4: continue
            
            words[target_idx] = "________"
            question_text = " ".join(words) + " ?"
            
            options = [target_word]
            # Ajouter des distracteurs aléatoires
            other_words = [w.strip(',.:;()!?') for w in text.split() if len(w) > 4 and w.lower() != target_word.lower()]
            if len(other_words) > 3:
                distractors = random.sample(list(set(other_words)), 3)
                options.extend(distractors)
            else:
                options.extend(["Réponse B", "Réponse C", "Réponse D"])
            
            random.shuffle(options)
            
            quiz_data.append({
                "question": question_text,
                "options": options,
                "answer": target_word,
                "explanation": f"Cette phrase est extraite directement de votre document : \"{sentence}.\""
            })
            
        return quiz_data
