from typing import List

import streamlit as st


def process_files(
    uploaded_files: List[st.runtime.uploaded_file_manager.UploadedFile],
) -> str:
    """Process uploaded files and return their combined content."""
    content = ""
    if uploaded_files:
        for file in uploaded_files:
            content += file.read().decode("utf-8") + "\n\n"
    return content


def get_content(
    uploaded_files: List[st.runtime.uploaded_file_manager.UploadedFile], text_input: str
) -> str:
    """Combine content from uploaded files and text input."""
    content = process_files(uploaded_files)
    if text_input:
        content += text_input
    return content.strip()
