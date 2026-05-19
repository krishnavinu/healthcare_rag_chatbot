"""Streamlit UI — LOCAL mode (downloads/runs FLAN-T5 on your PC)."""

import streamlit as st

from college_chatbot import create_chatbot, load_documents
from streamlit_ui import render_app

st.set_page_config(
    page_title="College FAQ Chatbot (Local)",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_document_count():
    return len(load_documents())


@st.cache_resource(show_spinner="Loading local FLAN-T5 model (first run may take a few minutes)...")
def get_chatbot():
    return create_chatbot(mode="local", top_k=2, max_tokens=80)


render_app(
    title="College FAQ Chatbot (Local)",
    subtitle="FLAN-T5 runs on your computer. First run downloads ~1 GB.",
    generator_label="FLAN-T5 (local)",
    mode_description=(
        "1. **Retrieve** — TF-IDF over `college_data.txt`\n"
        "2. **Generate** — **Local** `google/flan-t5-base` on your PC"
    ),
    get_chatbot=get_chatbot,
    get_document_count=get_document_count,
)
