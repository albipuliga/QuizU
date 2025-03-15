import io
import os
from typing import List

import docx
import PyPDF2
import streamlit as st


def process_files(
    uploaded_files: List[st.runtime.uploaded_file_manager.UploadedFile],
) -> str:
    """Process uploaded files and return their combined content."""
    content = ""
    if uploaded_files:
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[1].lower()

            if file_extension == ".pdf":
                try:
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                    pdf_text = ""
                    for _, page in enumerate(pdf_reader.pages):
                        pdf_text += page.extract_text() + "\n"
                    content += pdf_text + "\n\n"
                except Exception as e:
                    st.error(f"Error processing PDF file {file.name}: {str(e)}")

            elif file_extension == ".docx":
                try:
                    doc = docx.Document(io.BytesIO(file.read()))
                    docx_text = ""
                    for para in doc.paragraphs:
                        docx_text += para.text + "\n"
                    content += docx_text + "\n\n"
                except Exception as e:
                    st.error(f"Error processing DOCX file {file.name}: {str(e)}")

            else:
                # Handle text files (assuming UTF-8 encoding)
                try:
                    content += file.read().decode("utf-8") + "\n\n"
                except UnicodeDecodeError:
                    # If UTF-8 fails, try with a more forgiving encoding
                    file.seek(0)  # Reset file pointer
                    content += file.read().decode("latin-1") + "\n\n"
                except Exception as e:
                    st.error(f"Error processing text file {file.name}: {str(e)}")

    return content


def get_content(
    uploaded_files: List[st.runtime.uploaded_file_manager.UploadedFile], text_input: str
) -> str:
    """Combine content from uploaded files and text input."""
    content = process_files(uploaded_files)
    if text_input:
        content += text_input
    return content.strip()
