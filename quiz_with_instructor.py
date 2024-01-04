import instructor
from openai import OpenAI
from pydantic import BaseModel


class Questions(BaseModel):
    questions: list[str]


class Answer(BaseModel):
    is_correct: bool
    correct_answer: str


def generate_questions_with_instructor(
    client: OpenAI, model: str, category: str, number_of_questions: int
) -> list[str]:
    messages = [
        {
            "role": "system",
            "content": """Your job is to generate one single likely output for a Python function with the following 
                        signature and docstring:

                       def generate_questions(category: str, number_of_questions: int) -> list[str]:
                            \"\"\"Generate questions for a given category and number of questions.\"\"\"

                        The user will provide function inputs (if any).
                        """,
        },
        {
            "role": "user",
            "content": f"""The function was called with the following inputs:
                         - category: {category}
                         - number_of_questions: {number_of_questions}

                        What is its output?""",
        },
    ]

    client = instructor.patch(client)
    response = client.chat.completions.create(
        messages=messages, model=model, n=1, response_model=Questions
    )

    return response


def check_answer_with_instructor(client: OpenAI, model: str, question: str, user_answer: str) -> Answer:
    messages = [
        {
            "role": "system",
            "content": """Check the answer to the question. Both the question and answer should be strings.
            
            Allow for minor differences in the answer. This includes differences such as whitespace, capitalization, and punctuation.
            It also includes differences in the way the answer is expressed.
            
            For example if the correct answer to a math question is "x = 5", then "x=5", "X = 5", "x = 5." and "5" should all be considered correct.
            
            """,
        },
        {
            "role": "user",
            "content": f"""The function was called with the following inputs:
                         - {question}
                         - {user_answer}

                        What is the output?""",
        },
    ]

    client = instructor.patch(client)
    response = client.chat.completions.create(
        messages=messages, model=model, n=1, response_model=Answer
    )

    return response
