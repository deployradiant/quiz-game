import json

from openai import OpenAI

from data_types import Answer


def generate_questions_with_prompts(
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
                        
                        The output should be a list of strings with the questions. Do not include anything else in the output.
                        
                        For example, if the input is:
                        category: "math", number_of_questions: 2
                        
                        The output should be:
                        ["What is 1 + 1?", "What is 2 + 2?"]
                        
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

    response = client.chat.completions.create(messages=messages, model=model, n=1)
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Selected model did not return a valid JSON response. Response: {content}")


def check_answer_with_prompts(client: OpenAI, model: str, question: str, user_answer: str) -> Answer:
    messages = [
        {
            "role": "system",
            "content": """Check the answer to the question. Both the question and answer should be strings.

            Allow for minor differences in the answer. This includes differences such as whitespace, capitalization, and punctuation.
            It also includes differences in the way the answer is expressed.

            For example if the correct answer to a math question is "x = 5", then "x=5", "X = 5", "x = 5." and "5" 
            should all be considered correct.
            
            The output should be a dictionary with 2 keys: "is_correct" and "correct_answer". "is_correct" should be 
            a boolean with either True or False. "correct_answer" should be a string with the correct answer.
            Do not include anything else in the output.
            
            For example, if the input is:
            question: "What is 1 + 1?", user_answer: "2"
            
            The output should be:
            {"is_correct": true, "correct_answer": "2"}

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

    response = client.chat.completions.create(messages=messages, model=model, n=1)
    content = response.choices[0].message.content
    try:
        return Answer(**json.loads(content))
    except json.JSONDecodeError:
        raise ValueError(f"Selected model did not return a valid JSON response. Response: {content}")