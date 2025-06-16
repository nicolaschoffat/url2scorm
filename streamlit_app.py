import streamlit as st

QUIZ = [
    {"question": "Quel est le résultat de 3 * 3 ?", "options": ["6", "9", "12"], "answer": "9"},
    {"question": "Quelle est la capitale de la France ?", "options": ["Paris", "Lyon", "Marseille"], "answer": "Paris"},
    {"question": "Python est un ?", "options": ["Serpent", "Langage", "Oiseau"], "answer": "Langage"}
]

st.title("🎓 Quiz interactif")

if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = []

current = st.session_state.current_q

if current < len(QUIZ):
    q = QUIZ[current]
    st.write(f"**Question {current+1}/{len(QUIZ)}**")
    st.write(q["question"])
    choice = st.radio("Choisissez une réponse :", q["options"], key=current)

    if st.button("Valider"):
        st.session_state.answers.append(choice)
        if choice == q["answer"]:
            st.session_state.score += 1
        st.session_state.current_q += 1
        st.experimental_rerun()
else:
    st.success(f"✅ Score final : {st.session_state.score} / {len(QUIZ)}")
    if st.button("Recommencer"):
        st.session_state.clear()
        st.experimental_rerun()

