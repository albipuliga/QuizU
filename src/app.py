import base64
import pickle
import urllib.parse

import streamlit as st

from file_handler import get_content
from quiz_generator import generate_questions


def main():
    """Main application entry point for quiz generation."""
    st.set_page_config(page_title="QuizU", page_icon="📚", layout="wide")

    # Initialize session state for questions if not already done
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    # Page header with styled banner
    st.markdown(
        """
    <div style="padding:10px; border-radius:10px">
        <h1 style="color:white; text-align:center">📚 QuizU</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <h3 style="text-align:center">Generate personalized quizzes from your study materials! 🎯</h3>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### Materials")

    uploaded_files = st.file_uploader(
        "Upload your study materials",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True,
    )

    text_input = st.text_area("Or enter your text directly", height=150)

    st.markdown("### Quiz Settings")

    num_questions = st.number_input(
        "Number of questions",
        min_value=1,
        max_value=15,
        value=5,
        help="(Maximum 15)",
    )

    question_types = st.segmented_control(
        "Question types",
        options=["Multiple Choice", "True/False"],
        selection_mode="multi",
        default=["Multiple Choice"],
    )

    if not question_types:
        st.warning("Please select at least one question type.")
        return

    st.markdown("---")
    generate_button = st.button("Generate Quiz", type="primary")

    # Process button
    if generate_button:
        content = get_content(uploaded_files, text_input)

        if not content:
            st.warning("Please upload files or enter text to generate questions.")
            return

        with st.spinner("Generating quiz questions..."):
            questions = generate_questions(
                question_types,
                content,
                num_questions,
            )

            # Store questions in session state for persistence
            if questions:
                # Store in session state
                st.session_state.quiz_questions = questions

                # Also encode the questions into a base64 string for the URL
                # This is needed because the session state isn't shared between pages
                serialized = pickle.dumps(questions)
                encoded = base64.b64encode(serialized).decode("utf-8")

                # URL-encode the base64 string to ensure it's URL-safe
                url_safe_encoded = urllib.parse.quote(encoded)

                # Automatically redirect to the Quiz page with the encoded data
                # Set query parameter separately instead of including it in the path
                st.query_params.update({"data": url_safe_encoded})
                st.switch_page("pages/Quiz.py")
            else:
                st.error("Failed to generate questions. Please try again.")


if __name__ == "__main__":
    main()
