# Quiz Game

## Overview
Quiz Game is a simple and interactive quiz application built with [Instructor](https://jxnl.github.io/instructor/) and [Streamlit](https://streamlit.io/) leveraging the [Radiant platform](https://radiantai.com). 

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
- Marvin
- Streamlit

## Future Enhancements
- Add a timer to each question.
- Add a leaderboard to track high scores.

## Marvin support

This application was originally built with Marvin 1.5.6. It was then moved to using Instructor in this [pull request](https://github.com/anjor/quiz-game/pull/3) in order to use the latest version of OpenAI python client.
There is tentative support for Marvin in this [pull request](https://github.com/anjor/quiz-game/pull/5), however, that requires pinning the openai python client to a `0.x` version.