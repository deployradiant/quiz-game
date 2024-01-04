import json

import instructor
from openai import OpenAI

from data_types import Answer, Questions


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

    response = client.chat.completions.create(
        messages=messages, model=model, n=1, temperature=1.8
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print(
            f"Selected model did not return a valid JSON response. Response: {content}"
        )
        return best_effort_extract_question_from_response(client, content)


def check_answer_with_prompts(
    client: OpenAI, model: str, question: str, user_answer: str
) -> Answer:
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
        print(
            f"Selected model did not return a valid JSON response. Response: {content}"
        )
        return best_effort_extract_answer_from_response(client, content)


def best_effort_extract_question_from_response(
    client: OpenAI, response: str
) -> list[str]:
    client = instructor.patch(client)

    messages = [
        {
            "role": "system",
            "content": """Your job is to extract the JSON from the response. The response is a string. 
            Inside that string is a JSON object that is a list of strings. 
            This list is supposed to be a list of questions.
            Output just the JSON object. Do not include anything else in the output.
            
            For example, if the input is: response: "The `generate_questions` function takes two arguments, 
            `category` (a string) and `number_of_questions` (an integer), and returns a list of strings containing 
            questions related to the specified category. The docstring provides a clear description of what the 
            function does. Assuming the user calls this function with inputs 'physics' for `category` and 2 for 
            `number_of_questions`, we can expect the output to be a list containing two physics-related questions. 
            Here's an example: ```python def generate_questions(category: str, number_of_questions: int) -> List[
            str]: \"\"\"Generate questions for a given category and number of questions.\"\"\" # This is the 
            implementation of the function logic # ... question_templates = { "physics": [ "What force acts on an 
            object at rest?", "What is the formula for calculating acceleration?" ], "math": [ "What is 5 + 3? ", 
            "What is the product of 2 and 4?" ] } questions = [] for I in range(number_of_questions): 
            category_templates = question_templates[category] questions.append(random.choice(category_templates)) 
            return questions ``` In this implementation, the function creates a dictionary `question_templates` with 
            keys representing different categories and corresponding lists containing possible questions for each 
            category. The function then iteratively selects one question from the list for the given category using 
            Python's built-in random module. Using this approach, if the user calls `generate_questions("physics", 
            2)`, we can expect output like: ```python ["What force acts on an object at rest? ", "What is the formula 
            for calculating acceleration?"] ```"
            
            The output should be:
            ["What force acts on an object at rest?", "What is the formula for calculating acceleration?"]""",
        },
        {
            "role": "user",
            "content": f"""response: {response}

                        What is the JSON output that is a list of strings?""",
        },
    ]

    response = client.chat.completions.create(
        messages=messages, model="gpt-3.5-turbo", n=1, response_model=Questions
    )

    return response.questions


def best_effort_extract_answer_from_response(client: OpenAI, response: str) -> Answer:
    client = instructor.patch(client)

    messages = [
        {
            "role": "system",
            "content": """Your job is to extract the JSON from the response. The response is a string. 
            Inside that string is a JSON object that is a dictionary with two keys: "is_correct" and "correct_answer".
            "is_correct" should be a boolean with either True or False. "correct_answer" should be a string.
            Output just the JSON object. Do not include anything else in the output.

            For example, if the input is: response: "Your function should have the following signature: `(question: 
            str, user_answer: str) -> Dict[str, Any]` Here's an implementation of your function based on your 
            requirements: ```python def check_answer(question: str, user_answer: str) -> dict: # Convert all to 
            lowercase and replace spaces with underscores question = ''.join(c if c.isalnum() or c.isspace() else ' 
            '_ for c in question).replace(' ', '_').lower() user_answer = ''.join(c if c.isalnum() or c.isspace() 
            else ' '_ for c in user_answer).replace(' ', '_').lower() # Split both the question and answer into lists 
            of words qwords = [word for word in question.split('_')] uwords = [word for word in user_answer.split(
            '_')] # Check if lengths are equal, as we assume correct answers are shorter if len(qwords) != len(
            uwords): return {'is_correct': False, 'correct_answer': question} # Check for differences in words or 
            spacing for I in range(len(qwords)): if qwords[i] != uwords[i]: return {'is_correct': False, 
            'correct_answer': question} # If we've made it this far, answer is correct! return {'is_correct': True, 
            'correct_answer': user_answer} ``` I'm assuming you want minor differences to be allowed, as per your 
            requirements. This implementation converts both the question and answer to lowercase, replaces spaces 
            with underscores, and splits them into lists of words. Then, it checks for length equality first, 
            as we assume correct answers are shorter, and then iterates through each word in both lists, checking for 
            differences. If any difference is found, the function returns early with an indication that the answer is 
            incorrect, along with the original question. Otherwise, it returns a dictionary indicating that the 
            answer is correct. I'm not including the second input (`user_answer`) in the output of the function, 
            as your requirements explicitly state that you should only return `{'is_correct': boolean, 
            'correct_answer': string}'`. To test this implementation with your example: ```python print(check_answer(
            'what force acts on an object at rest?', 'inertia')) # Output: {'is_correct': True, 'correct_answer': 
            'inertia'} ``` Let me know if you have any questions or need further help!"

            The output should be:
            {'is_correct': True, 'correct_answer': 'inertia'}""",
        },
        {
            "role": "user",
            "content": f"""response: {response}

                        What is the JSON output that is a dictionary with keys is_correct and correct_answer?""",
        },
    ]

    response = client.chat.completions.create(
        messages=messages, model="gpt-3.5-turbo", n=1, response_model=Answer
    )

    return response
