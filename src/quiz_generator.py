try:
    import spacy
except Exception as e:
    # Catch Pydantic ConfigError or other initialization errors (common in Python 3.14)
    print(f"[WARNING] Spacy import failed (likely Pydantic/Python 3.14 conflict): {e}")
    spacy = None
import random
import re
import json
import google.generativeai as genai
from .config import USE_GEMINI, GOOGLE_API_KEY, GEMINI_MODEL

class QuizGenerator:
    def __init__(self):
        # Initialize Google Gemini with System Instructions for consistent formatting and better speed
        if USE_GEMINI and GOOGLE_API_KEY and GOOGLE_API_KEY != "YOUR_API_KEY_HERE":
            genai.configure(api_key=GOOGLE_API_KEY)
            
            system_instruction = """
            Tu es un assistant pédagogique expert de classe mondiale, spécialisé dans la conception de QCM (Questions à Choix Multiples) de haut niveau.
            
            Règles de Qualité (CRITIQUE) :
            1. INTERDICTION FORMELLE : Ne crée JAMAIS de questions à trous (type '_____'). Produis des questions interrogatives complètes.
            2. NIVEAU COGNITIF : Privilégie les questions de réflexion, d'analyse et d'application des concepts. Évite le simple rappel de faits.
            3. STRUCTURE : Chaque question doit être une interrogation complète, claire et directe.
            4. OPTIONS : Exactement 4 options. Les distracteurs doivent être plausibles et basés sur des erreurs de raisonnement courantes.
            5. EXPLICATIONS PÉDAGOGIQUES : Fournis une explication d'expert (2-3 phrases) qui :
               - Explique le CONCEPT derrière la réponse correcte.
               - Démontre POURQUOI cette réponse est la plus logique dans ce contexte.
               - Ne mentionne jamais la position du mot dans le texte original.
            6. FORMAT : Réponds UNIQUEMENT en JSON pur (tableau d'objets).
            """
            
            self.model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                system_instruction=system_instruction
            )
        else:
            self.model = None
        
        # Load French model for NLP (legacy/fallback)
        try:
            self.nlp = spacy.load("fr_core_news_sm")
        except:
            self.nlp = None

    def generate_quiz(self, text, num_questions=5, difficulty="Standard", use_ai=True):
        """
        Main entry point for quiz generation.
        """
        if use_ai and self.model:
            return self._generate_with_gemini(text, num_questions, difficulty)
        else:
            return self._generate_with_local_nlp(text, num_questions, difficulty)

    def generate_summary(self, text, use_ai=True):
        """
        Generates a summary of key points from the text.
        """
        if not use_ai or not self.model:
            # Simple fallback: return a few sentences or use NLP
            doc = self.nlp(text[:2000]) if self.nlp else None
            if doc:
                keywords = list(set([t.text for t in doc if t.pos_ in ["NOUN", "PROPN"] and len(t.text) > 4]))
                random.shuffle(keywords)
                return [f"Concept clé : {kw}" for kw in keywords[:5]]
            return ["Synthèse non disponible en mode local."]

        prompt = f"""
        En tant qu'expert pédagogique, analyse le texte suivant et extrais les 7 points essentiels à retenir absolument sous forme de liste concise.
        Chaque point doit être clair, pédagogique et facile à mémoriser.
        
        Texte source :
        {self._sample_text(text)}
        """

        try:
            response = self.model.generate_content(prompt)
            content = response.text
            # Split into list, cleanup common list prefixes
            points = [re.sub(r'^[\d\.\-\*\s]+', '', p).strip() for p in content.strip().split('\n') if p.strip()]
            return points[:10]
        except Exception as e:
            print(f"Summary Error: {e}")
            return ["Erreur lors de la génération de la synthèse."]

    def chat_with_document(self, text, query, history=[], use_ai=True):
        """
        Answers a specific question about the document.
        """
        if not use_ai or not self.model:
            return "Le chat est uniquement disponible avec une clé API Google AI active."

        # Prepare chat context
        context = f"Tu es un professeur particulier expert. Tu as lu le document suivant : \n\n{self._sample_text(text)}\n\nAide l'élève en répondant de façon claire, pédagogique et précise à ses questions en te basant exclusivement sur ce texte."
        
        # Simple history formatting for Gemini
        gemini_history = []
        for msg in history[-4:]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})
            
        try:
            chat = self.model.start_chat(history=gemini_history)
            response = chat.send_message(f"{context}\n\nQuestion de l'élève : {query}")
            return response.text
        except Exception as e:
            return f"Désolé, je rencontre une erreur avec Gemini : {str(e)}"

    def _generate_with_gemini(self, text, num_questions, difficulty):
        """
        Generates quiz using Google Gemini API with Native JSON mode.
        """
        prompt = f"""
        Génère un quiz de {num_questions} questions de niveau '{difficulty}' à partir du texte ci-dessous.
        
        Consignes :
        - Pose des questions de réflexion qui testent la compréhension des concepts.
        - INTERDICTION d'utiliser des blancs (_____) ou des questions de vocabulaire simple.
        - Chaque explication doit être un mini-cours expliquant la logique du concept.
        - Langue : Français.
        
        Format attendu :
        [
            {{
                "question": "Question interrogative complète ?",
                "options": ["Choix 1", "Choix 2", "Choix 3", "Choix 4"],
                "answer": "La réponse correcte exacte",
                "explanation": "Analyse pédagogique approfondie du concept."
            }}
        ]

        Texte source :
        {self._sample_text(text)}
        """

        try:
            # Use JSON Mode for Gemini 2.0+ (faster and more reliable)
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            
            content = response.text
            quiz_data = json.loads(content)
            
            # Ensure we respect the requested number of questions
            final_quiz = quiz_data if isinstance(quiz_data, list) else []
            return final_quiz[:num_questions]
            
            # Ensure we respect the requested number of questions
            final_quiz = quiz_data if isinstance(quiz_data, list) else []
            return final_quiz[:num_questions]
            
        except Exception as e:
            error_msg = str(e)
            print(f"Gemini Error: {error_msg}")
            
            # Specific handling for safety blocks or quota
            if "safety" in error_msg.lower():
                return [
                    {
                        "question": "⚠️ Contenu Bloqué (Filtres de Sécurité)",
                        "options": ["Réessayer", "Changer de texte", "Mode Local", "Désactiver filtres"],
                        "answer": "Changer de texte",
                        "explanation": "Google Gemini a détecté du contenu sensible dans votre document et a bloqué la génération par sécurité."
                    }
                ] * num_questions
                
            return self._generate_with_local_nlp(text, num_questions, difficulty)

    def _sample_text(self, text, max_chars=4000):
        """
        If the text is too long, takes representative samples from start, middle, and end.
        """
        if len(text) <= max_chars:
            return text
        
        chunk_size = max_chars // 3
        start = text[:chunk_size]
        middle = text[len(text)//2 - chunk_size//2 : len(text)//2 + chunk_size//2]
        end = text[-chunk_size:]
        
        return f"{start}\n\n[...]\n\n{middle}\n\n[...]\n\n{end}"

    def _generate_with_local_nlp(self, text, num_questions=5, difficulty="Standard"):
        """
        Generates a list of QCM questions using local Spacy model.
        Falls back to regex-based generation if Spacy is unavailable.
        """
        if not self.nlp:
            # Direct fallback to regex generator (no error message)
            # This is normal when using Python 3.14 or when Spacy is not installed
            return self._simple_regex_fallback(text, num_questions) or []

        doc = self.nlp(text)
        
        # Adjust filters based on difficulty
        min_words = 15
        max_words = 50
        require_proper_noun = False
        
        if difficulty == "Avancée":
            min_words = 20
            max_words = 60
        elif difficulty == "Expert":
            min_words = 25
            max_words = 80
            require_proper_noun = True

        sentences = []
        for sent in doc.sents:
            text_sent = sent.text.strip()
            words = text_sent.split()
            if min_words < len(words) < max_words:
                has_noun = any(t.pos_ == "NOUN" for t in sent)
                has_verb = any(t.pos_ == "VERB" for t in sent)
                has_propn = any(t.pos_ == "PROPN" for t in sent)
                
                if has_noun and has_verb:
                    if not require_proper_noun or has_propn:
                        sentences.append(sent)
        
        if not sentences:
            sentences = [sent for sent in doc.sents if len(sent.text.split()) > 10]

        quiz = []
        all_nouns = list(set([t.text for t in doc if t.pos_ in ["NOUN", "PROPN"] and len(t.text) > 3]))
        random.shuffle(sentences)
        
        # First pass: try to get high-quality questions
        for sent in sentences:
            if len(quiz) >= num_questions:
                break
            question_data = self._create_question_from_sentence(sent, all_nouns)
            if question_data:
                quiz.append(question_data)
        
        # Second pass: if not enough questions, be less restrictive with sentences
        if len(quiz) < num_questions:
            remaining = num_questions - len(quiz)
            fallback_sentences = [sent for sent in doc.sents if 10 < len(sent.text.split()) < 100 and sent not in sentences]
            random.shuffle(fallback_sentences)
            for sent in fallback_sentences:
                if len(quiz) >= num_questions:
                    break
                question_data = self._create_question_from_sentence(sent, all_nouns)
                if question_data:
                    quiz.append(question_data)
        
        if not quiz:
             error_extraction = {
                "question": "⚠️ Mode Dégradé (Environnement Instable)",
                "options": ["Mettre à jour Python", "Vérifier les libs", "Réessayer", "Changer de fichier"],
                "answer": "Mettre à jour Python",
                "explanation": "L'IA locale rencontre des difficultés avec votre version de Python (3.14). Utilisez une version stable (3.10 ou 3.11) ou activez vos crédits OpenAI pour une expérience fluide."
            }
             
             # Ultra-simple regex fallback as a last resort "Pro" move
             # To ensure the app ALWAYS produces something even if libs are broken
             try:
                 fallback_quiz = self._simple_regex_fallback(text, num_questions)
                 if fallback_quiz:
                     return fallback_quiz
             except:
                 pass

             while len(quiz) < num_questions:
                 quiz.append(error_extraction)
             return quiz[:num_questions]

    def _generate_rich_explanation(self, target, full_sentence, question_text):
        """
        Génère une explication riche et pédagogique pour une question (Mode Local).
        """
        # Liste de mots à ignorer pour les explications conceptuelles
        stop_concepts = ["pouvoir", "être", "avoir", "faire", "dire", "aller", "voir", "vouloir", "devoir"]
        
        # Déterminer la nature du terme
        word_length = len(target)
        is_concept = word_length > 5 and target.lower() not in stop_concepts
        term_label = "concept clé" if is_concept else "terme"
        
        # Modèles d'explication simplifiés et pédagogiques
        intro = [
            f"La réponse correcte est '{target}'.",
            f"Le terme '{target}' est ici l'élément essentiel.",
            f"Dans ce contexte, '{target}' est la réponse exacte."
        ]
        
        logic = [
            f"Ce {term_label} est utilisé pour définir une action ou une propriété fondamentale décrite dans le document.",
            f"L'utilisation de '{target}' permet d'apporter une précision nécessaire à la cohérence de cette affirmation.",
            f"Sur le plan pédagogique, retenir '{target}' aide à structurer la compréhension globale du sujet.",
            f"Ce choix s'appuie sur les principes fondamentaux exposés dans la source."
        ]
        
        # Ajout d'une astuce de mémorisation
        tips = [
            "💡 Conseil : Visualisez comment ce concept s'articule avec les autres points clés du sujet.",
            "💡 Méthode : Essayez d'associer ce terme à un exemple concret pour mieux le retenir.",
            "💡 Astuce : Relisez la phrase complète pour assimiler la structure logique autour de ce mot.",
            "💡 Technique : Reformulez l'idée principale en utilisant votre propre vocabulaire."
        ]
        
        return f"{random.choice(intro)} {random.choice(logic)} {random.choice(tips)}"

    def _simple_regex_fallback(self, text, num_questions):
        """Minimalist backup generator that doesn't depend on Spacy or Pydantic."""
        # Split into sentences roughly
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.split()) > 10]
        if not sentences:
            # If no good sentences, split by length
            words = text.split()
            sentences = [' '.join(words[i:i+15]) for i in range(0, len(words), 15) if len(words[i:i+15]) > 10]
        
        if not sentences:
            return None
        
        random.shuffle(sentences)
        quiz = []
        
        # Extract all potential target words from the entire text
        # Filter for words that are at least 4 chars long, start with uppercase, and contain ONLY letters
        all_words = re.findall(r'\b[A-ZÀÂÄÉÈÊËÏÎÔÙÛÜ][a-zàâäéèêëïîôùûüç]{3,}\b', text)
        all_words = list(set(all_words))  # Remove duplicates
        
        for s in sentences:
            if len(quiz) >= num_questions:
                break
            
            # Find words in this sentence that could be blanked (clean words only)
            words = re.findall(r'\b[A-ZÀÂÄÉÈÊËÏÎÔÙÛÜ][a-zàâäéèêëïîôùûüç]{3,}\b', s)
            
            if words:
                target = random.choice(words)
                question_text = s.replace(target, "__________")
                
                # Create distractors from other words in the text
                # Filter out small words or common verbs
                distractors = [w for w in all_words if w.lower() != target.lower() and len(w) > 4]
                random.shuffle(distractors)
                distractors = distractors[:3]
                
                # Ensure we have 4 options
                while len(distractors) < 3:
                    distractors.append(f"Option {len(distractors) + 1}")
                
                options = distractors + [target]
                random.shuffle(options)
                
                # Generate rich, contextual explanation
                explanation = self._generate_rich_explanation(target, s, question_text)
                
                quiz.append({
                    "question": question_text,
                    "options": options,
                    "answer": target,
                    "explanation": explanation
                })
        
        return quiz if len(quiz) >= 1 else None

    def _create_question_from_sentence(self, sent, all_nouns):
        """
        Creates a fill-in-the-blank question from a sentence with better distractors.
        """
        # Find the most "important" noun in the sentence (e.g., subject or object)
        candidates = [token for token in sent if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 3]
        
        if not candidates:
            return None
        
        # Prefer proper nouns if available
        propn = [c for c in candidates if c.pos_ == "PROPN"]
        target = random.choice(propn) if propn else random.choice(candidates)
        answer = target.text
        
        # Create question by replacing target text with a placeholder
        # We use a case-insensitive replacement to handle start of sentences
        pattern = r"\b" + re.escape(answer) + r"\b"
        question_text = re.sub(pattern, "__________", sent.text, flags=re.IGNORECASE)
        
        if "__________" not in question_text:
            return None

        # Create distractors
        # 1. Other nouns from the same sentence
        sentence_nouns = [t.text for t in sent if t.pos_ in ["NOUN", "PROPN"] and t.text.lower() != answer.lower()]
        
        # 2. Random nouns from the whole document
        other_nouns = [n for n in all_nouns if n.lower() != answer.lower() and n not in sentence_nouns]
        
        distractors = list(set(sentence_nouns + other_nouns))
        random.shuffle(distractors)
        distractors = distractors[:3]
        
        # Fallback if still not enough
        while len(distractors) < 3:
            distractors.append(f"Option {len(distractors) + 1}")
            
        options = distractors + [answer]
        random.shuffle(options)
        
        return {
            "question": question_text,
            "options": options,
            "answer": answer,
            "explanation": self._generate_rich_explanation(answer, sent.text, question_text)
        }
