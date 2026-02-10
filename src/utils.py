import streamlit as st
import pypdf
import docx
import random
import re

def extract_text_from_file(uploaded_file):
    """Extracts text from PDF, DOCX, or TXT files."""
    text = ""
    try:
        if uploaded_file.name.endswith('.pdf'):
            pdf_reader = pypdf.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif uploaded_file.name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif uploaded_file.name.endswith('.txt'):
            text = uploaded_file.read().decode('utf-8')
    except Exception as e:
        st.error(f"Erreur lors de l'extraction du texte : {e}")
    return text

def generate_quiz_from_text(text, num_questions=5):
    """
    Generates MCQ questions from text.
    Currently uses a rule-based approach for reliability and speed.
    """
    if not text or len(text) < 100:
        return []

    # Clean text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Simple logic: split into sentences and pick some to turn into questions
    # In a more advanced version, we'd use NLTK or Spacy to find key concepts.
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s for s in sentences if len(s.split()) > 10] # Filter short sentences
    
    if not sentences:
        return []

    # Simple heuristic to identify "definitional" or important sentences
    keywords = ["est", "sont", "dépend", "consiste", "appelle", "signifie", "permet"]
    important_sentences = [s for s in sentences if any(k in s.lower() for k in keywords)]
    
    if len(important_sentences) < num_questions:
        important_sentences = sentences # Fallback to all sentences if not enough important ones

    selected_sentences = random.sample(important_sentences, min(num_questions, len(important_sentences)))
    
    quiz_data = []
    for sentence in selected_sentences:
        # Create a basic question by removing a key word or phrase
        # This is a placeholder for a more advanced NLP question generation
        # For now, we simulate relevance by using parts of the sentence
        
        words = sentence.split()
        if len(words) < 5: continue
        
        # Pick a word to hide (avoiding small common words)
        candidate_words = [w for w in words if len(w) > 5 and w.lower() not in ["lequel", "laquelle", "pendant", "environ"]]
        if not candidate_words: continue
        
        answer = random.choice(candidate_words).strip(".,!?;:")
        question_text = sentence.replace(answer, "_______")
        
        # Generate some distractor options (fake words or words from other sentences)
        distractors = []
        all_words = list(set(re.findall(r'\b\w{5,}\b', text)))
        if answer in all_words: all_words.remove(answer)
        
        if len(all_words) >= 3:
            distractors = random.sample(all_words, 3)
        else:
            distractors = ["Option A", "Option B", "Option C"]
            
        options = distractors + [answer]
        random.shuffle(options)
        
        quiz_data.append({
            "question": f"Complétez la phrase suivante issue du document : \n\n '{question_text}'",
            "options": options,
            "answer": answer
        })
        
    return quiz_data
