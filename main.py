import streamlit as st

from quiz import generate_questions, check_answers
from utils import _check_answers

MODELS = ["gpt-3.5-turbo", "mistral-tiny", "mistral-small"]

def title():
    st.title("Simple Quiz")
    st.sidebar.header("Instructions")

    st.sidebar.markdown("This is a simple quiz game. You can select the category and the number of questions for the quiz.")
    st.sidebar.write('Click the "Start game" button to start the quiz.')
    st.sidebar.write("If you want to play again, click the button again.")


def quiz_params():
    cols = st.columns(2)

    with cols[0]:
        category = st.text_input("**Category**", key="category")
    with cols[1]:
        number_of_questions = st.text_input("**Number of questions**", key="number_of_questions")

    return category, number_of_questions


def run_quiz(model:str, category: str, number_of_questions: int):
    if "questions" not in st.session_state:
        st.session_state.questions = []

    if st.button("Start game"):
        questions = generate_questions(model=model, category=category, number_of_questions=number_of_questions)
        if not questions:
            st.write("The model returns invalid JSON. Please try again with a different model.")
        st.session_state.questions = questions

    questions_with_answers = {}
    for question in st.session_state.questions:
        st.write(question)
        questions_with_answers[question] = st.text_input("Answer", key=question)

    if st.session_state.questions:
        if st.button("Check answers"):
            results = check_answers(model=model, questions_with_answers=questions_with_answers)
            if not results:
                st.write("The model returns invalid JSON. Please try again with a different model.")
            _check_answers(results=results, questions_with_answers=questions_with_answers)


if __name__ == "__main__":
    title()

    if "model" not in st.session_state:
        st.session_state.model = "gpt-3.5-turbo"

    st.sidebar.header("Advanced settings")
    model = st.sidebar.radio("Model", MODELS)

    if model != st.session_state.model:
        st.session_state.model = model

    category, number_of_questions = quiz_params()

    run_quiz(model=st.session_state.model, category=category, number_of_questions=number_of_questions)
