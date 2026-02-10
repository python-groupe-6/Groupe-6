import streamlit as st

st.set_page_config(page_title="Résultats", page_icon="📊")

st.title("📊 Vos Résultats")

if 'quiz_submitted' not in st.session_state or not st.session_state.quiz_submitted:
    st.warning("Veuillez d'abord passer un quiz et soumettre vos réponses.")
    st.stop()

score = 0
total = len(st.session_state.quiz_data)

for i, q in enumerate(st.session_state.quiz_data):
    user_answer = st.session_state.user_answers.get(i)
    correct_answer = q['answer']
    
    with st.expander(f"Question {i + 1}: {q['question']}", expanded=True):
        if user_answer == correct_answer:
            st.success(f"✅ Correct ! (Votre réponse : {user_answer})")
            score += 1
        else:
            st.error(f"❌ Incorrect. (Votre réponse : {user_answer})")
            st.info(f"La bonne réponse était : **{correct_answer}**")

st.metric(label="Score Final", value=f"{score}/{total}", delta=f"{int((score/total)*100)}%")

if score == total:
    st.success("Félicitations ! Un score parfait ! 🎉")
elif score > total / 2:
    st.info("Bon travail ! Continuez à réviser.")
else:
    st.warning("Il semble que vous ayez besoin de réviser un peu plus.")

if st.button("Recommencer un nouveau Quiz"):
    # Reset state
    st.session_state.quiz_data = []
    st.session_state.user_answers = {}
    st.session_state.quiz_submitted = False
    st.rerun()
