import json
import streamlit as st
import openai
from marvin import ai_fn

openai.api_base = "https://demo.deployradiant.com/anjor-test/openai"
openai.api_key = "notNeeded"


@ai_fn
def generate_math_questions(number_of_questions: int = 1) -> list[str]:
    """Generate simple math questions for a given number of questions. The questions will be addition or subtraction
    questions with numbers between 0 and 100."""


@ai_fn
def check_math_answer(question: str, answer: str) -> str:
    """Check the answer to a math question. The question should be a string in the format of "X + Y = ?" or "X - Y = ?".
    The answer should be a string with the correct answer. 

    Respond in json format with 1 key: "answer". "answer" should be the correct answer. Do not add anything else in your response. """


def main():
    st.title("Math Quiz Game")
    st.header("Solve the math questions below")
    if 'questions' not in st.session_state:
        st.session_state.questions = generate_math_questions(number_of_questions=3)

    answers = {}

    i = 1
    for question in st.session_state.questions:
        st.write(question)
        answers[question] = st.text_input("Answer", key=question)
    
    total_score = 0
    if st.button("Check answers"):
        for question, answer in answers.items():
            if answer:
                result = check_math_answer(question, answer)
                result = json.loads(result)
                correct_answer = result["answer"]
                if answer == correct_answer:
                    total_score += 1
                    st.markdown(f":white_check_mark: {question} \n You answered: {answer}")
                else:
                    st.markdown(f":x: {question} \n You answered: {answer} \n Correct answer: {correct_answer}")
    
        st.write(f"Total score: {total_score}/{len(st.session_state.questions)}")

        if st.button("Play again"):
            st.session_state.questions = generate_math_questions(number_of_questions=2)


if __name__ == "__main__":
    main()
