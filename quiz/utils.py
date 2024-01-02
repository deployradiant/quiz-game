from constants import QuizType
from math_quiz import MathQuiz


def get_quiz(quiz_type):
    if quiz_type == QuizType.ELEMENTARY_MATH.value:
        return MathQuiz()
    else:
        raise ValueError(f"Quiz type {quiz_type} is not supported.")