import streamlit as st

st.set_page_config(page_title="Passer le Quiz", page_icon="📝")

st.title("📝 Passer le Quiz")

if 'quiz_data' not in st.session_state or not st.session_state.quiz_data:
    st.warning("⚠️ Aucun quiz n'est disponible. Veuillez d'abord en générer un dans la section 'Générer un Quiz'.")
    st.stop()

if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

with st.form("quiz_form"):
    for i, q in enumerate(st.session_state.quiz_data):
        st.subheader(f"Question {i + 1}")
        st.write(q['question'])
        
        # Unique key for each radio button
        st.session_state.user_answers[i] = st.radio(
            "Choisissez une réponse :",
            q['options'],
            key=f"q_{i}"
        )
        st.write("---")
    
    submitted = st.form_submit_button("Soumettre les réponses")
    
    if submitted:
        st.session_state.quiz_submitted = True
        st.success("Réponses soumises ! Allez voir vos résultats.")
        st.balloons()
