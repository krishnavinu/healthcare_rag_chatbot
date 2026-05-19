"""Shared Streamlit chat UI for the healthcare RAG chatbot."""

import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Force readable light main area (fixes dark-theme white-on-white chat) */
    .stApp {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }
    .main .block-container {
        color: #0f172a !important;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    [data-testid="stAlert"] {
        background-color: #f0fdfa !important;
        border: 1px solid #99f6e4 !important;
        color: #134e4a !important;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f766e 0%, #134e4a 100%);
    }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #f0fdfa !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2);
    }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.15) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.28) !important;
        color: #ffffff !important;
        border-color: rgba(255,255,255,0.55) !important;
    }
    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stButton > button span,
    [data-testid="stSidebar"] .stButton > button div {
        color: #ffffff !important;
    }

    .sidebar-brand {
        text-align: center;
        padding: 0.5rem 0 1.25rem 0;
    }
    .sidebar-brand .icon {
        font-size: 2.5rem;
        line-height: 1;
    }
    .sidebar-brand h2 {
        margin: 0.5rem 0 0.25rem 0;
        font-size: 1.35rem;
        font-weight: 700;
        color: #fff !important;
    }
    .sidebar-brand p {
        margin: 0;
        font-size: 0.8rem;
        opacity: 0.85;
        color: #ccfbf1 !important;
    }

    .sidebar-step {
        background: rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 0.65rem 0.85rem;
        margin-bottom: 0.5rem;
        font-size: 0.88rem;
        border-left: 3px solid #5eead4;
    }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #0d9488 0%, #0f766e 50%, #115e59 100%);
        border-radius: 16px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.25rem;
        color: white;
        box-shadow: 0 10px 40px rgba(13, 148, 136, 0.25);
    }
    .hero h1 {
        margin: 0 0 0.35rem 0;
        font-size: 1.85rem;
        font-weight: 700;
        color: white !important;
    }
    .hero p {
        margin: 0;
        font-size: 1rem;
        opacity: 0.92;
        color: #ccfbf1 !important;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        letter-spacing: 0.03em;
    }

    /* Metric cards */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.25rem;
    }
    @media (max-width: 768px) {
        .metric-row { grid-template-columns: 1fr; }
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.15rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    .metric-card .label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748b;
        margin-bottom: 0.35rem;
    }
    .metric-card .value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f766e;
    }

    /* Chat section */
    .chat-section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #134e4a;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.75rem;
    }

    [data-testid="stChatMessage"] .stMarkdown,
    [data-testid="stChatMessage"] .stMarkdown p,
    [data-testid="stChatMessage"] .stMarkdown li,
    [data-testid="stChatMessage"] .stMarkdown strong,
    [data-testid="stChatMessage"] .stMarkdown span {
        color: #1e293b !important;
    }

    [data-testid="stChatInput"] {
        border-radius: 12px;
    }
    [data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
        border: 2px solid #99f6e4 !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        caret-color: #0d9488 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #0d9488 !important;
        box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15) !important;
    }

    [data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] .stMarkdown {
        color: #1e293b !important;
    }

    .footer-note {
        text-align: center;
        color: #64748b !important;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
"""

SAMPLE_QUESTIONS = [
    "How do I book an appointment?",
    "What are the emergency department hours?",
    "Does the hospital accept health insurance?",
    "How can I get my lab test results?",
    "What are the visiting hours for patients?",
]

WELCOME_MESSAGE = (
    "Hello! I'm your **Healthcare FAQ Assistant**.\n\n"
    "Ask me about **appointments**, **emergency care**, **visiting hours**, "
    "**insurance**, **lab tests**, **pharmacy**, **telemedicine**, or **billing**.\n\n"
    "Use a quick question from the sidebar or type below."
)


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE,
                "context": None,
            }
        ]


def render_sidebar(mode_description: str):
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="icon">🏥</div>
                <h2>CareGuide AI</h2>
                <p>Healthcare FAQ • RAG Chatbot</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### How it works")
        st.markdown(
            '<div class="sidebar-step"><strong>1. Retrieve</strong><br/>'
            "Find relevant FAQ passages (TF-IDF)</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sidebar-step"><strong>2. Generate</strong><br/>'
            "FLAN-T5 answers from context only</div>",
            unsafe_allow_html=True,
        )

        st.divider()
        st.markdown("#### Quick questions")
        for question in SAMPLE_QUESTIONS:
            if st.button(question, use_container_width=True, key=f"sample_{question}"):
                st.session_state.pending_question = question

        st.divider()
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Conversation cleared. What would you like to know?",
                    "context": None,
                }
            ]
            st.rerun()


def render_hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero">
            <span class="hero-badge">RETRIEVAL-AUGMENTED GENERATION</span>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(chunk_count: int, retriever: str, generator: str):
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="label">Knowledge base</div>
                <div class="value">{chunk_count} FAQ chunks</div>
            </div>
            <div class="metric-card">
                <div class="label">Retriever</div>
                <div class="value">{retriever}</div>
            </div>
            <div class="metric-card">
                <div class="label">Generator</div>
                <div class="value">{generator}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def handle_user_message(query: str, get_chatbot):
    st.session_state.messages.append({"role": "user", "content": query, "context": None})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="🏥"):
        with st.spinner("Searching FAQs and generating answer..."):
            try:
                chatbot = get_chatbot()
                response, retrieved = chatbot.chat(query, return_context=True)
            except FileNotFoundError as exc:
                response = str(exc)
                retrieved = []
            except Exception as exc:
                response = f"Sorry, something went wrong: **{exc}**"
                retrieved = []

        st.markdown(response)

        if retrieved:
            with st.expander("📄 Retrieved context (RAG source chunks)", expanded=False):
                for i, doc in enumerate(retrieved, start=1):
                    st.markdown(f"**Source {i}**")
                    st.info(doc)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "context": retrieved if retrieved else None,
        }
    )


def render_chat_history():
    for message in st.session_state.messages:
        avatar = "🧑" if message["role"] == "user" else "🏥"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("context"):
                with st.expander("📄 Retrieved context (RAG source chunks)", expanded=False):
                    for i, doc in enumerate(message["context"], start=1):
                        st.markdown(f"**Source {i}**")
                        st.info(doc)


def render_app(title, subtitle, generator_label, mode_description, get_chatbot, get_document_count):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_session_state()
    render_sidebar(mode_description)

    render_hero(title, subtitle)
    render_metrics(get_document_count(), "TF-IDF + Cosine", generator_label)

    st.markdown('<p class="chat-section-title">💬 Conversation</p>', unsafe_allow_html=True)

    render_chat_history()

    pending = st.session_state.pop("pending_question", None)
    if pending:
        handle_user_message(pending, get_chatbot)
        st.rerun()

    if query := st.chat_input("Ask about appointments, insurance, labs, visiting hours..."):
        handle_user_message(query, get_chatbot)
        st.rerun()

