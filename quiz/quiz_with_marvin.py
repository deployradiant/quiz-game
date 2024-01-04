import openai
from marvin import ai_fn

from data_types import Questions, Answer

openai.api_base = "https://demo.deployradiant.com/anjor-test/openai"
openai.api_key = "notNeeded"


@ai_fn
def generate_questions_with_marvin(
    category: str, number_of_questions: int
) -> Questions:
    """Generate questions for a given category and number of questions.

    For example,
    If the category is "math", the questions should be simple math questions.

    If you generate good questions, you will be rewarded with a bonus of $500.
    """


@ai_fn
def check_answer_with_marvin(question: str, user_answer: str) -> Answer:
    """
    Check the answers to questions. The input should be a dictionary with the questions along with the answers, where the key is the question and the value is the answer.
    The question should be a string.
    The answer should be a string.

    Respond as a dictionary with the question as the key and a dictionary with two keys: "is_correct" and
    "correct_answer". "is_correct" should be a boolean with either True or False. "correct_answer" should be a
    string with the correct answer.
    """
