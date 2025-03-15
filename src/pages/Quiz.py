import base64
import os
import pickle
import sys
import urllib.parse

import streamlit as st

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from quiz_generator import display_question


def main():
    """Quiz taking page."""
    st.set_page_config(page_title="QuizU - Take Quiz", page_icon="📝", layout="wide")

    # Page header with styled banner
    st.markdown(
        """
    <div style="padding:10px; border-radius:10px">
        <h1 style="color:white; text-align:center">📝 QuizU - Take Quiz</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Get query parameters using the new non-experimental API
    query_params = st.query_params

    # Check if data parameter exists
    if "data" in query_params:
        try:
            # Get the encoded data and URL-decode it first
            encoded_data = query_params["data"]
            url_decoded = urllib.parse.unquote(encoded_data)

            # Then decode the base64 data and load the questions
            serialized = base64.b64decode(url_decoded)
            questions = pickle.loads(serialized)

            # Store in session state
            st.session_state.quiz_questions = questions
        except Exception as e:
            st.error(f"Error loading quiz data: {str(e)}")
            st.session_state.quiz_questions = []

    # Initialize session state for questions if not already done
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    # Check if questions exist
    if not st.session_state.quiz_questions:
        st.info("No quiz questions available. Please generate a quiz first.")

        # Button to go back to quiz creation
        st.markdown(
            """
        <div style="text-align:center; margin-top:20px">
            <a href="../" target="_self">
                <button style="
                    background-color:#4267B2; 
                    color:white; 
                    padding:12px 20px; 
                    border:none; 
                    border-radius:5px; 
                    cursor:pointer; 
                    font-size:16px">
                    Create a New Quiz
                </button>
            </a>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    # Show quiz information
    total_questions = len(st.session_state.quiz_questions)

    # Add quiz progress tracker
    correct_count = sum(
        1
        for i in range(1, total_questions + 1)
        if f"correct_{i}" in st.session_state and st.session_state[f"correct_{i}"]
    )

    # Create a dashboard-like header for the quiz
    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        # Progress bar and score
        progress = correct_count / total_questions if total_questions > 0 else 0
        st.progress(progress)

    st.markdown("---")

    for i, question in enumerate(st.session_state.quiz_questions, 1):
        display_question(i, question)

    if st.button("Reset All Answers"):
        # Clear all answer-related session state
        for key in list(st.session_state.keys()):
            if key.startswith(("answer_", "feedback_", "correct_", "radio_")):
                del st.session_state[key]

        for i in range(1, len(st.session_state.quiz_questions) + 1):
            st.session_state[f"radio_{i}"] = None

        st.rerun()

    if st.button("Create New Quiz", type="primary"):
        st.switch_page("app.py")


if __name__ == "__main__":
    main()
