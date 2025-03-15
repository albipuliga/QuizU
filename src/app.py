import streamlit as st

from file_handler import get_content
from quiz_generator import display_question, generate_questions


def main():
    """Main application entry point."""
    st.set_page_config(page_title="QuizU", page_icon="📚", layout="wide")

    st.title("QuizU 📚")
    st.html("""
            <h3>A Streamlit app for generating quiz questions based on your files! 🎯 ✨</h3>
            """)

    uploaded_files = st.file_uploader(
        "Upload your study materials",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True,
    )

    text_input = st.text_area("Or enter your text directly", height=120)

    num_questions = st.number_input(
        "Number of questions to generate",
        min_value=1,
        max_value=15,
        value=5,
        help="(Maximum 15)",
    )

    question_types = st.segmented_control(
        "Select question type to include",
        options=["Multiple Choice", "True/False"],
        selection_mode="multi",
        default=["Multiple Choice"],
    )

    # Process button
    if st.button("Generate Quiz", type="primary"):
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

        if questions:
            # Display questions
            for i, question in enumerate(questions, 1):
                display_question(i, question)


if __name__ == "__main__":
    main()
