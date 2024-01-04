import streamlit as st
from openai import OpenAI

from quiz import check_answer


def check_answers(client: OpenAI, model: str, questions_with_answers: dict[str, str]):
    total_score = 0
    for question in st.session_state.questions:
        user_answer = questions_with_answers[question]
        result = check_answer(
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
