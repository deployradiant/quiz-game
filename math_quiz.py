from marvin import ai_fn
import openai
from quiz import Quiz

openai.api_base = "https://demo.deployradiant.com/anjor-test/openai"
openai.api_key = "notNeeded"

class MathQuiz(Quiz):

    @ai_fn
    def generate_questions(number_of_questions: int = 1) -> list[str]:
        """Generate simple math questions for a given number of questions. The questions will be addition or subtraction
        questions with numbers between 0 and 100."""


    @ai_fn
    def generate_answers(questions: list[str]) -> dict[str, str]:
        """Check the answers to math questions. The input should be a list with the questions
        The question should be a string in the format of "X + Y = ?" or "X - Y = ?".

        Respond as a dictionary with the question as the key and the correct answer as the value. 
        """