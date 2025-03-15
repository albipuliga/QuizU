import os

import google.generativeai as genai
import streamlit as st


def init_gemini():
    """Initialize and configure the Gemini API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key is None:
        st.error(
            "Please set the GOOGLE_API_KEY in your environment variables or Streamlit secrets."
        )
        st.stop()
    genai.configure(api_key=api_key)
    return genai
