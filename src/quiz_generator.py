import json
from typing import Dict, List

import streamlit as st

from utils import init_gemini


def validate_questions(questions):
    """Function to validate the generated questions.

    Args:
        questions: List of question dictionaries containing question text, type, options, correct answer.

    Returns:
        bool: True if all questions are valid, False otherwise.
    """
    if not isinstance(questions, list):
        return False

    required_fields = {"question", "type", "options", "correct_answer"}

    for question in questions:
        if not isinstance(question, dict):
            return False
        if not all(field in question for field in required_fields):
            return False

    return True


def generate_questions(
    question_types: List[str], content: str, num_questions: int = 5
) -> List[Dict]:
    """Generate quiz questions using Gemini AI.

    Args:
        content: The text content to generate questions from
        num_questions: Number of questions to generate
        question_types: List of question types to include (Multiple Choice, True/False)

    Returns:
        List of question dictionaries containing question text, type, options,
        correct answer and explanation
    """

    client = init_gemini()
    prompt = f"""Generate {num_questions} quiz questions based on the following content. Please include the following format of questions only: {question_types}.
    
    For each question, provide:
    1. `question`: The question text
    2. `type`: The type of question (multiple_choice or true_false)
    3. `options`: The possible options (for multiple choice)
    4. `correct_answer`: The correct answer

    Return the response as a JSON array of question objects.
    Content: {content}
    """

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    try:
        response_text = response.candidates[0].content.parts[0].text

        # Remove the markdown code block markers if present
        json_str = response_text.replace("```json", "").replace("```", "").strip()

        # Parse the JSON string into a Python object
        questions = json.loads(json_str)

        if validate_questions(questions):
            return questions
        else:
            print("Generated questions failed validation")
            return []

    except json.JSONDecodeError:
        print("Failed to generate properly formatted questions. Please try again.")
        return []


def display_question(index: int, question: Dict):
    """Display a single quiz question with its answer options.

    Args:
        index: Question number
        question: Question dictionary containing all question data
    """
    with st.expander(f"Question {index}"):
        st.write(question["question"])

        if question["type"] == "multiple_choice":
            answer = st.radio(
                "Select your answer:", question["options"], key=f"q_{index}"
            )
        else:  # true_false
            answer = st.radio(
                "Select your answer:", ["True", "False"], key=f"q_{index}"
            )

        if st.button("Check Answer", key=f"check_{index}"):
            if answer == question["correct_answer"]:
                st.success("Correct! 🎉")
            else:
                st.error("Incorrect. Try again!")
            st.write(f"Explanation: {question['explanation']}")
