import streamlit as st
from math_quiz import generate_math_questions, generate_math_answers


def main():
    st.title("Math Quiz")
    st.write("Click the button below to start the game.")
    st.write("You will be asked 3 questions. You can answer them one by one and then check the answers.")
    st.write("If you want to play again, click the button again.")

    if "played" not in st.session_state:
        st.session_state.played = False
    
    if "questions" not in st.session_state: 
        st.session_state.questions = []

    if st.button("Start game"):
        st.session_state.questions = generate_math_questions(number_of_questions=3)

    questions_with_answers = {}

    i = 1
    for question in st.session_state.questions:
        st.write(question)
        questions_with_answers[question] = st.text_input("Answer", key=question)
    
    total_score = 0
    if st.button("Check answers"):
        correct_answers = generate_math_answers(st.session_state.questions)
        for question in st.session_state.questions:
            if question in questions_with_answers:
                answer = questions_with_answers[question]
                correct_answer = correct_answers[question]
                if answer == correct_answer:
                    total_score += 1
                    st.markdown(f":white_check_mark: {question} \n You answered: {answer}")
                else:
                    st.markdown(f":x: {question} \n You answered: {answer} \n Correct answer: {correct_answer}")
    
        st.write(f"Total score: {total_score}/{len(st.session_state.questions)}")

if __name__ == "__main__":
    main()
