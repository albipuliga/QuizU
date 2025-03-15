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

    for question in questions:
        if not isinstance(question, dict):
            return False

        if (
            "question" not in question
            or "type" not in question
            or "correct_answer" not in question
        ):
            return False

        if question["type"] == "multiple_choice" and "options" not in question:
            return False

        if question["type"] == "true_false" and "options" not in question:
            question["options"] = ["True", "False"]

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

    # Map UI options to internal types
    type_mapping = {"Multiple Choice": "multiple_choice", "True/False": "true_false"}
    selected_types = [type_mapping[t] for t in question_types]

    prompt = f"""Generate {num_questions} quiz questions based on the following content. Include the following question types: {selected_types}.
    
    For each question, provide:
    1. `question`: The question text
    2. `type`: The type of question (multiple_choice or true_false)
    3. `options`: For multiple_choice questions, provide an array of 4 options
    4. `correct_answer`: The correct answer (should be one of the options)
    5. `explanation`: A brief explanation of why the answer is correct

    For true_false questions, set `correct_answer` to either "True" or "False".
    
    Return the response as a JSON array of question objects.
    Content: {content}
    """

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    try:
        response_text = response.candidates[0].content.parts[0].text

        # Remove the markdown code block markers if present
        json_str = response_text.replace("```json", "").replace("```", "").strip()

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
    question_key = f"question_{index}"
    answer_key = f"answer_{index}"
    feedback_key = f"feedback_{index}"

    with st.expander(f"Question {index}", expanded=True):
        st.write(question["question"])

        # Initialize session state for this question if not already done
        if answer_key not in st.session_state:
            st.session_state[answer_key] = None

        if feedback_key not in st.session_state:
            st.session_state[feedback_key] = False

        if question["type"] == "multiple_choice":
            options = question["options"]
        else:  # true_false
            options = question.get("options", ["True", "False"])
            # Convert correct_answer to proper case for True/False
            if isinstance(question["correct_answer"], str) and question[
                "correct_answer"
            ].lower() in ["true", "false"]:
                question["correct_answer"] = question["correct_answer"].capitalize()

        selected_answer = st.radio(
            "Select your answer:", options, key=f"radio_{index}", index=None
        )
        st.session_state[answer_key] = selected_answer

        # Use a unique key for the button and check if it's pressed
        button_key = f"check_button_{index}"
        if st.button("Check Answer", key=button_key):
            st.session_state[feedback_key] = True

        # Display feedback if button was pressed
        if st.session_state[feedback_key]:
            if st.session_state[answer_key] == question["correct_answer"]:
                st.success("Correct! 🎉")
            else:
                st.error(f"The correct answer is: {question['correct_answer']}")

            # Show explanation if it exists
            if "explanation" in question:
                st.write(f"Explanation: {question['explanation']}")
            else:
                st.write("No explanation provided.")
