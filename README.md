# Quiz Game

## Overview
Quiz Game is a simple and interactive quiz application built with [Streamlit](https://streamlit.io/) leveraging the [Radiant platform](https://radiantai.com). 

The application generates quiz questions for the user to solve using AI functions in Marvin. After the user submits their answers, the application checks the answers and provides immediate feedback, along with the correct answers for any questions the user got wrong.

## Features
- Generates a set of quiz questions for the user to solve.
- Allows the user to submit their answers and get immediate feedback.
- Displays a score indicating how many questions the user got right.

## How to Run Locally
1. Ensure you have Python and Streamlit installed on your machine.
2. Clone this repository to your local machine.
3. Navigate to the directory containing the application.
4. Run the command `streamlit run main.py` to start the application.
5. Open your web browser and go to `http://localhost:8501` to view the application.

## Dependencies
- Streamlit
- [Optional] [Instructor](https://jxnl.github.io/instructor/)
- [Optional] [Marvin](https://www.askmarvin.ai/)

## Future Enhancements
- Add a timer to each question.
- Add a leaderboard to track high scores.

## Enforcing JSON response format

Enforcing JSON responses from LLMs was probably the trickiest part in this project.
If we only stick to OpenAI models, then using [JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode) in OpenAI text generation helps.

Both [Instructor](https://jxnl.github.io/instructor/) and [Marvin](https://www.askmarvin.ai/) also enable this functionality by using the [function calling](https://platform.openai.com/docs/guides/function-calling) feature in OpenAI text generation.

However, that means we are restricted to using OpenAI models only. If we want to use other models, we need to find a way to enforce JSON responses from them.

The solution (workaround?) implemented here is to use model-of-choice for the question generation and answer checking, but use `gpt-3.5-turbo` to extract the correct JSON object from the generated text.
For more details see [quiz_with_prompts.py](quiz/quiz_with_prompts.py).

## Using Instructor and Marvin

By default the application uses the [quiz_with_prompts.py](quiz/quiz_with_prompts.py) module to generate questions and check answers.
To use Instructor/Marvin, simply swap out the `generate_questions_fn` and `check_answers_fn` in [main.py](main.py) with the corresponding functions from Instructor/Marvin.

> [!NOTE]
> Instructor requires OpenAI python client version 1.x, while Marvin requires version 0.x.
> Ensure you have the correct version installed in your environment before running the application.

