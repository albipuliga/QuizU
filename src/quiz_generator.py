import json
from typing import Dict, List

import streamlit as st

from utils import init_gemini


def generate_questions(content: str, num_questions: int = 5) -> List[Dict]:
    """Generate quiz questions using Gemini AI.

    Args:
        content: The text content to generate questions from
        num_questions: Number of questions to generate

    Returns:
        List of question dictionaries containing question text, type, options,
        correct answer and explanation
    """
    client = init_gemini()
    prompt = f"""Generate {num_questions} quiz questions based on the following content. Include a mix of multiple choice and true/false questions.
    For each question, provide:
    1. The question text
    2. The type of question (multiple_choice or true_false)
    3. The possible answers (for multiple choice)
    4. The correct answer
    5. An explanation of why the answer is correct

    Return the response as a JSON array of question objects.
    Content: {content}
    """

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    try:
        questions = json.loads(response.text)
        return questions
    except json.JSONDecodeError:
        st.error("Failed to generate properly formatted questions. Please try again.")
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
