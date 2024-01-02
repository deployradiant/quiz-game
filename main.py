import streamlit as st
from constants import QuizType
from utils import get_quiz


def main():
    st.title("Simple Quiz")
    st.write("Click the button below to start the game.")
    st.write("You will be asked 3 questions. You can answer them one by one and then check the answers.")
    st.write("If you want to play again, click the button again.")

    st.sidebar.title("Categories")
    category = st.sidebar.selectbox("Select a category", [category.value for category in QuizType])

    quiz = get_quiz(category)


    if "questions" not in st.session_state: 
        st.session_state.questions = []

    if st.button("Start game"):
        st.session_state.questions = quiz.generate_questions(number_of_questions=3)

    questions_with_answers = {}

    i = 1
    for question in st.session_state.questions:
        st.write(question)
        questions_with_answers[question] = st.text_input("Answer", key=question)
    
    total_score = 0
    if st.button("Check answers"):

        correct_answers = quiz.generate_answers(st.session_state.questions)

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
