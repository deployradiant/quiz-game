import streamlit as st


def _check_answers(check_answers_fn, questions_with_answers):
    results = check_answers_fn(questions_with_answers)

    total_score = 0
    for question in st.session_state.questions:
        if question in results:
            user_answer = questions_with_answers[question]
            is_correct = results[question]["is_correct"]
            correct_answer = results[question]["correct_answer"]

            if is_correct:
                total_score += 1
                st.markdown(
                    f":white_check_mark: {question}  \n You answered: {user_answer}. Correct answer: {correct_answer}")
            else:
                st.markdown(f":x: {question}  \n You answered: {user_answer}. Correct answer: {correct_answer}")
    st.write(f"Total score: {total_score}/{len(st.session_state.questions)}")
