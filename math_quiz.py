from marvin import ai_fn


@ai_fn
def generate_math_questions(number_of_questions: int = 1) -> list[str]:
    """Generate simple math questions for a given number of questions. The questions will be addition or subtraction
    questions with numbers between 0 and 100."""


@ai_fn
def check_math_answer(question: str, answer: str) -> str:
    """Check the answer to a math question. The question should be a string in the format of "X + Y = ?" or "X - Y = ?".
    The answer should be a string with the correct answer. 
    Respond in json format with 1 key: "answer". "answer" should be the correct answer. Do not add anything else in your response. """