from marvin import ai_fn
import openai
from quiz.quiz import Quiz

openai.api_base = "https://demo.deployradiant.com/anjor-test/openai"
openai.api_key = "notNeeded"

class ElementaryMath(Quiz):

    @ai_fn
    def generate_questions(number_of_questions: int = 1) -> list[str]:
        """Generate simple math questions for a given number of questions. The questions will be addition or subtraction
        questions with numbers between 0 and 100."""


    @ai_fn
    def check_answers(questions_with_answers: dict[str,str]) -> dict[str, dict[str, str]]:
        """Check the answers to math questions. The input should be a list with the questions along with the answers.
        The question should be a string in the format of "X + Y = ?" or "X - Y = ?".
        The answer should be a string with the number.

        Respond as a dictionary with the question as the key and a dictionary with two keys: "is_correct" and "correct_answer".
        "is_correct" should be a string with either "true" or "false".
        "correct_answer" should be a string with the correct answer.
        """