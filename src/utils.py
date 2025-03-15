import os

import streamlit as st
from google import genai


def init_gemini():
    """Initialize and configure the Gemini API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key is None:
        st.error(
            "Please set the GOOGLE_API_KEY in your environment variables or Streamlit secrets."
        )
        st.stop()
    client = genai.Client(api_key=api_key)
    return client
