import google.generativeai as genai
import json
import re
import random
from django.conf import settings
import os
from pypdf import PdfReader
import requests
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

# Configuration from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

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
        # Prioritize Google API Key, then OpenAI, then OpenRouter
        self.use_google_direct = bool(GOOGLE_API_KEY)
        self.use_openai = bool(OPENAI_API_KEY)
        self.use_openrouter = bool(OPENROUTER_API_KEY)
        self.model = None
        self.openai_client = None
        
        if self.use_google_direct:
            try:
                genai.configure(api_key=GOOGLE_API_KEY)
                self.model = genai.GenerativeModel(GEMINI_MODEL)
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
                self.use_google_direct = False
        
        if self.use_openai:
            try:
                self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize OpenAI: {e}")
                self.use_openai = False

    def generate_quiz(self, text, num_questions=5, difficulty="Standard"):
        # Order of execution: Gemini -> OpenAI -> OpenRouter -> Fallback
        if self.use_google_direct and self.model:
            try:
                return self._generate_with_gemini(text, num_questions, difficulty)
            except:
                pass
        
        if self.use_openai and self.openai_client:
            try:
                return self._generate_with_openai(text, num_questions, difficulty)
            except:
                pass
                
        if self.use_openrouter:
            return self._generate_with_openrouter(text, num_questions, difficulty)
            
        return self._simple_regex_fallback(text, num_questions)

    def _generate_with_openai(self, text, num_questions, difficulty):
        prompt = f"""Génère un quiz de HAUTE QUALITÉ à partir du texte fourni.
        
        PARAMÈTRES:
        - Nombre de questions : {num_questions}
        - Niveau de difficulté : {difficulty}
        
        NIVEAUX DE DIFFICULTÉ :
        - Standard : Questions de base, mémorisation simple.
        - Intermédiaire : Compréhension et application des concepts.
        - Avancée : Analyse et lien entre les parties du texte.
        - Expert : Pensée critique, synthèse complexe et cas limites.

        TEXTE SÉLECTIONNÉ :
        {self._sample_text(text, 5000)}
        
        CONSIGNES :
        1. Les options doivent être plausibles mais sans ambiguïté pour la bonne réponse.
        2. L'explication doit justifier POURQUOI la réponse est correcte.
        3. Retourne UNIQUEMENT un objet JSON valide.

        FORMAT JSON ATTENDU :
        {{
            "quiz": [
                {{
                    "question": "Texte de la question ?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "answer": "Option exacte telle qu'écrite dans options",
                    "explanation": "Détails explicatifs..."
                }}
            ]
        }}"""
        try:
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "system", "content": "Tu es un expert en pédagogie spécialisé dans la création de quiz évaluatifs."},
                          {"role": "user", "content": prompt}],
                response_format={ "type": "json_object" },
                temperature=0.4
            )
            content = response.choices[0].message.content
            quiz_data = json.loads(content)
            
            if isinstance(quiz_data, dict) and "quiz" in quiz_data:
                return quiz_data["quiz"][:num_questions]
            return quiz_data[:num_questions] if isinstance(quiz_data, list) else []
        except Exception as e:
            print(f"OpenAI error: {e}")
            if self.use_openrouter:
                return self._generate_with_openrouter(text, num_questions, difficulty)
            return self._simple_regex_fallback(text, num_questions)

    def _generate_with_openrouter(self, text, num_questions, difficulty):
        prompt = f"""Génère un quiz JSON de {num_questions} questions ({difficulty}):
        [
            {{
                "question": "...",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "..."
            }}
        ]
        Texte: {self._sample_text(text, 3000)}"""
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "google/gemini-flash-1.5",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": { "type": "json_object" },
            "temperature": 0.3
        }
        
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=20)
            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            if "```json" in content:
                content = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL).group(1)
            elif "```" in content:
                content = re.search(r"```\s*(.*?)\s*```", content, re.DOTALL).group(1)
                
            quiz_data = json.loads(content)
            if isinstance(quiz_data, dict):
                for key in quiz_data:
                    if isinstance(quiz_data[key], list):
                        return quiz_data[key][:num_questions]
            return quiz_data[:num_questions] if isinstance(quiz_data, list) else []
            
        except Exception as e:
            print(f"OpenRouter error: {e}")
            return self._simple_regex_fallback(text, num_questions)

    def _sample_text(self, text, max_chars=3000):
        if len(text) <= max_chars:
            return text
        chunk = max_chars // 2
        return f"{text[:chunk]}\n...\n{text[-chunk:]}"

    def _generate_with_gemini(self, text, num_questions, difficulty):
        prompt = f"""Génère un quiz de HAUTE QUALITÉ à partir du texte fourni.
        
        PARAMÈTRES:
        - Nombre de questions : {num_questions}
        - Niveau de difficulté : {difficulty}
        
        NIVEAUX DE DIFFICULTÉ :
        - Standard : Questions de base, mémorisation simple.
        - Intermédiaire : Compréhension et application des concepts.
        - Avancée : Analyse et lien entre les parties du texte.
        - Expert : Pensée critique, synthèse complexe et cas limites.

        TEXTE SÉLECTIONNÉ :
        {self._sample_text(text, 5000)}
        
        CONSIGNES :
        1. Génère exactement {num_questions} questions.
        2. Adapte la complexité au niveau '{difficulty}'.
        3. Retourne UNIQUEMENT une liste JSON d'objets.

        FORMAT JSON ATTENDU :
        [
            {{
                "question": "...",
                "options": ["...", "...", "...", "..."],
                "answer": "...",
                "explanation": "..."
            }}
        ]"""
        try:
            response = self.model.generate_content(
                prompt, 
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.4,
                    "top_p": 1,
                    "max_output_tokens": 4096,
                }
            )
            data = json.loads(response.text)
            if isinstance(data, dict) and "quiz" in data:
                return data["quiz"][:num_questions]
            return data[:num_questions]
        except Exception as e:
            with open("debug_quiz.log", "a", encoding="utf-8") as f:
                f.write(f"Gemini error: {e}\n")
            print(f"Gemini error: {e}")
            if self.use_openai:
                return self._generate_with_openai(text, num_questions, difficulty)
            if self.use_openrouter:
                return self._generate_with_openrouter(text, num_questions, difficulty)
            return self._simple_regex_fallback(text, num_questions)

    def _simple_regex_fallback(self, text, num_questions):
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
