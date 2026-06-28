import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"