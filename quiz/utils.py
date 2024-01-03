from quiz.constants import QuizType
from quiz.elementary_math import ElementaryMath
from quiz.american_history import AmericanHistory


def get_quiz(quiz_type):
    if quiz_type == QuizType.ELEMENTARY_MATH.value:
        return ElementaryMath()
    elif quiz_type == QuizType.AMERICAN_HISTORY.value:
        return AmericanHistory() 
    else:
        raise ValueError(f"Quiz type {quiz_type} is not supported.")