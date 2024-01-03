from marvin import ai_fn
import openai
from quiz.quiz import Quiz

openai.api_base = "https://demo.deployradiant.com/anjor-test/openai"
openai.api_key = "notNeeded"

class AmericanHistory(Quiz):

    @ai_fn
    def generate_questions(number_of_questions: int = 1) -> list[str]:
        """Generate questions about American History for a given number of questions. The questions should be elementary, designed for primary school children."""


    @ai_fn
    def check_answers(questions_with_answers: dict[str,str]) -> dict[str, dict[str, str]]:
        """Check the answers to american history questions. The input should be a list with the questions along with the answers.
        Both the question and answer should be strings.

        While checking the answers, allow for some flexibility in the answers. For example, if the correct answer is "George Washington",
        allow for "Washington" or "George Washington" to be correct. If the correct answer is "1776", allow for "1776" or "1776 AD" to be correct.
        Also allow for some spelling mistakes.

        Respond as a dictionary with the question as the key and a dictionary with two keys: "is_correct" and "correct_answer".
        "is_correct" should be a string with either "true" or "false".
        "correct_answer" should be a string with the correct answer.
        """