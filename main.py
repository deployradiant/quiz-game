import streamlit as st
from openai import OpenAI

from quiz import generate_questions
from utils import check_answers


def title():
    st.title("Simple Quiz")
    st.sidebar.header("Instructions")

    st.sidebar.markdown(
        "This is a simple quiz game. You can select the category and the number of questions for the quiz."
    )
    st.sidebar.write('Click the "Start game" button to start the quiz.')
    st.sidebar.write("If you want to play again, click the button again.")


def quiz_params():
    cols = st.columns(2)

    with cols[0]:
        category = st.text_input("**Category**", key="category")
    with cols[1]:
        number_of_questions = st.text_input(
            "**Number of questions**", key="number_of_questions"
        )

    return category, number_of_questions


def run_quiz(client: OpenAI, model: str, category: str, number_of_questions: int):
    if "questions" not in st.session_state:
        st.session_state.questions = []

    if st.button("Start game"):
        st.session_state.questions = generate_questions(
            client=client,
            model=model,
            category=category,
            number_of_questions=number_of_questions,
        )

    questions_with_answers = {}
    for question in st.session_state.questions:
        st.write(question)
        questions_with_answers[question] = st.text_input("Answer", key=question)

    if st.session_state.questions:
        if st.button("Check answers"):
            check_answers(
                client=client,
                model=model,
                questions_with_answers=questions_with_answers,
            )


if __name__ == "__main__":
    openai_client = OpenAI(
        api_key="notNeeded", base_url="http://localhost:8001/anjor-1/openai"
    )

    title()
    category, number_of_questions = quiz_params()
    run_quiz(
        client=openai_client,
        model="gpt-3.5-turbo",
        category=category,
        number_of_questions=number_of_questions,
    )
