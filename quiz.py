import json

import openai
from marvin import ai_fn

openai.api_base = "https://demo.deployradiant.com/anjor-test/openai"
openai.api_key = "notNeeded"


@ai_fn
def generate_questions_with_marvin(category: str, number_of_questions: int) -> list[str]:
    """Generate questions for a given category and number of questions.
    The complexity of the questions should be appropriate for primary school children, as they will be the primary quiz takers.

    For example,
    If the category is "math", the questions should be simple math questions.

    If you generate good questions, you will be rewarded with a bonus of $500.
    """


@ai_fn
def check_answers_with_marvin(questions_with_answers: dict[str, str]) -> dict[str, dict]:
    """
    Check the answers to questions. The input should be a dictionary with the questions along with the answers, where the key is the question and the value is the answer.
    The question should be a string.
    The answer should be a string.

    Respond as a dictionary with the question as the key and a dictionary with two keys: "is_correct" and
    "correct_answer". "is_correct" should be a boolean with either True or False. "correct_answer" should be a
    string with the correct answer.
    """


def generate_questions(model: str, category: str, number_of_questions: int) -> list[str]:
    messages = [
        {
            "role": "system",
            "content": """Your job is to generate one single likely output for a Python function with the following 
                        signature and docstring:
                       
                       def generate_questions(category: str, number_of_questions: int) -> list[str]:
                            \"\"\"Generate questions for a given category and number of questions.
                            The complexity of the questions should be appropriate for primary school children, as they 
                            will be the primary quiz takers.
                            
                            For example,
                            If the category is \"math\", the questions should be simple math questions.
                            \"\"\"
                            
                            
                        The user will provide function inputs (if any) and you must respond with
                        the most likely result, which must be valid, double-quoted JSON. Do not return anything else.
                        The response should not throw a JSONDecodeError when passed to json.loads().
                        
                        If you generate good questions compliant with the specified format, 
                        you will be rewarded with a bonus of $500.
                        If the response is not in the correct format and throws a JSONDecodeError when passed to 
                        json.loads(), you will be penalized $500.
                        """
        },
        {
            "role": "user",
            "content": f"""The function was called with the following inputs:
                         - category: {category}
                         - number_of_questions: {number_of_questions}
                         
                        What is its output?"""
        }
    ]

    response = openai.ChatCompletion.create(messages=messages, model=model, n=1)
    response = response.choices[0].message["content"]

    try:
        return json.loads(response)
    except json.decoder.JSONDecodeError:
        print(f"Invalid JSON, response={response}")
        return []


def check_answers(model:str, questions_with_answers: dict[str, str]) -> dict[str, dict]:
    messages = [
        {
            "role": "system",
            "content": """Check the answers to questions. The input should be a dictionary with the questions along with 
                the answers, where the key is the question and the value is the answer.
                The question should be a string.
                The answer should be a string.

                Respond as a dictionary with the question as the key and a dictionary with two keys: "is_correct" and
                "correct_answer". 
                "is_correct" should be a boolean with either True or False. 
                "correct_answer" should be a string with the correct answer.
                
                Do not include anything other than the dictionary in your response.
                The response should not throw a JSONDecodeError when passed to json.loads().
                
                If you check the answers correctly and return the correct format,
                you will be rewarded with a bonus of $500.
                If the response is not in the correct format and throws a JSONDecodeError when passed to 
                json.loads(), you will be penalized $500.
                """
        },
        {
            "role": "user",
            "content": f"""The function was called with the following inputs:
                         - {questions_with_answers}
                         
                        What is the output?"""
        }
    ]

    response = openai.ChatCompletion.create(messages=messages, model=model, n=1)
    response = response.choices[0].message["content"]

    try:
        return json.loads(response)
    except json.decoder.JSONDecodeError:
        print(f"Invalid JSON, response={response}")
        return {}