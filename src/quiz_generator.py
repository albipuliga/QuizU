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

        # Check for required fields based on question type
        if (
            "question" not in question
            or "type" not in question
            or "correct_answer" not in question
        ):
            return False

        # Multiple choice questions require options
        if question["type"] == "multiple_choice" and "options" not in question:
            return False

        # For true_false questions, add default options if missing
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

    # Convert selected types to internal format
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
    question_key = f"question_{index}"
    answer_key = f"answer_{index}"
    feedback_key = f"feedback_{index}"
    correct_key = f"correct_{index}"

    # Initialize session state for this question if not already done
    if answer_key not in st.session_state:
        st.session_state[answer_key] = None

    if feedback_key not in st.session_state:
        st.session_state[feedback_key] = False

    if correct_key not in st.session_state:
        st.session_state[correct_key] = False

    # Determine if question should be expanded
    # Keep expanded if: not yet answered, or answered incorrectly
    should_expand = (
        not st.session_state[feedback_key] or not st.session_state[correct_key]
    )

    # Create custom expander title with visual indicator for correct answers
    if st.session_state[feedback_key] and st.session_state[correct_key]:
        expander_title = f"✅ Question {index} (Correct)"
    else:
        expander_title = f"Question {index}"

    with st.expander(expander_title, expanded=should_expand):
        # Apply custom styling based on question state
        if st.session_state[feedback_key] and st.session_state[correct_key]:
            st.markdown(
                f"""
                <div style="border-left: 4px solid #28a745; padding-left: 10px;">
                    <p>{question["question"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.write(question["question"])

        # Get options based on question type
        if question["type"] == "multiple_choice":
            options = question["options"]
        else:  # true_false
            options = question.get("options", ["True", "False"])
            # Convert correct_answer to proper case for True/False
            if isinstance(question["correct_answer"], str) and question[
                "correct_answer"
            ].lower() in ["true", "false"]:
                question["correct_answer"] = question["correct_answer"].capitalize()

        # Display options with radio button
        selected_answer = st.radio(
            "Select your answer:", options, key=f"radio_{index}", index=None
        )

        # Store selected answer in session state
        st.session_state[answer_key] = selected_answer

        # Only show check button if feedback hasn't been given yet
        if not st.session_state[feedback_key]:
            button_key = f"check_button_{index}"
            if st.button("Check Answer", key=button_key):
                st.session_state[feedback_key] = True
                # Check if answer is correct and update state
                if st.session_state[answer_key] == question["correct_answer"]:
                    st.session_state[correct_key] = True
                    st.success("Correct! 🎉")
                    # Force a rerun to collapse the expander
                    st.rerun()
                else:
                    st.session_state[correct_key] = False
                    st.error(
                        f"Incorrect. The correct answer is: {question['correct_answer']}"
                    )

                    # Only show explanation for incorrect answers
                    if "explanation" in question:
                        st.write(f"Explanation: {question['explanation']}")
        else:
            # Show persistent feedback for questions that were already checked
            if st.session_state[correct_key]:
                st.success("Correct! 🎉")
            else:
                st.error(
                    f"Incorrect. The correct answer is: {question['correct_answer']}"
                )

                # Only show explanation for incorrect answers
                if "explanation" in question:
                    st.write(f"Explanation: {question['explanation']}")

        # Add a "Try Again" button for incorrect answers
        if st.session_state[feedback_key] and not st.session_state[correct_key]:
            if st.button("Try Again", key=f"retry_{index}"):
                st.session_state[feedback_key] = False
                st.rerun()
