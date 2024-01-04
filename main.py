from typing import Callable

import streamlit as st
from openai import OpenAI

from quiz.quiz_with_prompts import (
    generate_questions_with_prompts,
    check_answer_with_prompts,
)

MODELS = ["gpt-3.5-turbo", "claude-instant-1", "mistral-small", "ollama-wrapper-zephyr"]


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


def check_answers(
    check_answer_fn: Callable,
    client: OpenAI,
    model: str,
    questions_with_answers: dict[str, str],
):
    total_score = 0
    for question in st.session_state.questions:
        user_answer = questions_with_answers[question]
        result = check_answer_fn(
            client=client, model=model, question=question, user_answer=user_answer
        )
        is_correct = result.is_correct
        correct_answer = result.correct_answer

        if is_correct:
            total_score += 1
            st.markdown(
                f":white_check_mark: {question}  \n You answered: {user_answer}"
            )
        else:
            st.markdown(
                f":x: {question}  \n You answered: {user_answer}. Correct answer: {correct_answer}"
            )
    st.write(f"Total score: {total_score}/{len(st.session_state.questions)}")


def run_quiz(
    client: OpenAI,
    model: str,
    generate_questions_fn: Callable,
    check_answer_fn: Callable,
    category: str,
    number_of_questions: int,
):
    if "questions" not in st.session_state:
        st.session_state.questions = []

    if st.button("Start game"):
        st.session_state.questions = generate_questions_fn(
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
                check_answer_fn=check_answer_fn,
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

    if "model" not in st.session_state:
        st.session_state.model = MODELS[0]
    st.sidebar.header("Model Selection")
    st.session_state.model = st.sidebar.selectbox(
        "Select a model", MODELS, index=MODELS.index(st.session_state.model)
    )

    run_quiz(
        client=openai_client,
        model=st.session_state.model,
        generate_questions_fn=generate_questions_with_prompts,
        check_answer_fn=check_answer_with_prompts,
        category=category,
        number_of_questions=number_of_questions,
    )
