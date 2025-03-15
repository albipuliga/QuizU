import json
from typing import Dict, List

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

    genai = init_gemini()

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

    # Create a generation config
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    # Create a safety settings list
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
    ]

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        response = model.generate_content(prompt)

        # Get the text from the response
        response_text = response.text

        # Remove the markdown code block markers if present
        json_str = response_text.replace("```json", "").replace("```", "").strip()

        # Parse the JSON string into a Python object
        questions = json.loads(json_str)

        if validate_questions(questions):
            return questions
        else:
            print("Generated questions failed validation")
            return []

    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return []
