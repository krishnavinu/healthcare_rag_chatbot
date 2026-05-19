"""
Domain-Specific Chatbot Using RAG for Healthcare FAQs
Streamlit web interface.
"""

import streamlit as st

from healthcare_chatbot import create_chatbot, load_documents
from streamlit_ui import render_app

st.set_page_config(
    page_title="CareGuide AI | Healthcare RAG Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_document_count():
    return len(load_documents())


@st.cache_resource(show_spinner="Loading FLAN-T5 model (first run may take a few minutes)...")
def get_chatbot():
    return create_chatbot(top_k=2, max_tokens=80)


render_app(
    title="Healthcare FAQ Assistant",
    subtitle="Domain-specific answers from hospital FAQs using Retrieval-Augmented Generation",
    generator_label="FLAN-T5",
    mode_description="",
    get_chatbot=get_chatbot,
    get_document_count=get_document_count,
)
