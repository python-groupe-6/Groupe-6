import streamlit as st
import random
from utils import extract_text_from_file, generate_quiz_from_text

st.set_page_config(page_title="Générer un Quiz", page_icon="⚙️")

st.title("⚙️ Générer un Quiz")

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = []

uploaded_file = st.file_uploader("Téléchargez votre document de cours (Texte, PDF ou DOCX)", type=['txt', 'pdf', 'docx'])
num_questions = st.number_input("Nombre de questions souhaitées", min_value=1, max_value=20, value=5)

if st.button("🚀 Générer le Quiz"):
    if uploaded_file is not None:
        with st.spinner("Analyse du document et génération des questions..."):
            # Extract text from the uploaded file
            text = extract_text_from_file(uploaded_file)
            
            if text and len(text.strip()) > 100:
                # Generate real quiz data
                st.session_state.quiz_data = generate_quiz_from_text(text, num_questions)
                
                if st.session_state.quiz_data:
                    st.success(f"✅ Quiz de {len(st.session_state.quiz_data)} questions généré avec succès !")
                    st.info("👉 Allez à la page 'Passer le Quiz' pour commencer.")
                else:
                    st.error("Désolé, nous n'avons pas pu générer assez de questions à partir de ce document. Essayez un document plus long ou plus riche en texte.")
            else:
                st.error("Le document semble vide ou trop court pour générer un quiz de qualité.")
    else:
        st.error("Veuillez télécharger un document pour commencer.")
