"""Shared Streamlit chat UI for local and API modes."""

import streamlit as st

CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        color: #5f6368;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
</style>
"""

SAMPLE_QUESTIONS = [
    "When are undergraduate admissions open?",
    "What B.Tech branches are offered?",
    "What is the annual tuition fee?",
    "What are the library timings?",
    "How can I contact the admin office?",
]


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am the College FAQ Assistant. "
                    "Ask me about admissions, courses, fees, hostel, library, exams, or placements."
                ),
                "context": None,
            }
        ]


def render_sidebar(mode_description: str):
    with st.sidebar:
        st.header("About")
        st.markdown(
            f"""
This chatbot uses **Retrieval-Augmented Generation (RAG)**:

{mode_description}
            """
        )

        st.divider()
        st.subheader("Try a sample question")
        for question in SAMPLE_QUESTIONS:
            if st.button(question, use_container_width=True, key=f"sample_{question}"):
                st.session_state.pending_question = question

        st.divider()
        if st.button("Clear chat", use_container_width=True, type="primary"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Chat cleared. How can I help you today?",
                    "context": None,
                }
            ]
            st.rerun()

        st.divider()
        st.caption("GenAI College Project • RAG + Streamlit")


def handle_user_message(query: str, get_chatbot):
    st.session_state.messages.append({"role": "user", "content": query, "context": None})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chatbot = get_chatbot()
                response, retrieved = chatbot.chat(query, return_context=True)
            except FileNotFoundError as exc:
                response = str(exc)
                retrieved = []
            except Exception as exc:
                response = f"Sorry, something went wrong: {exc}"
                retrieved = []

        st.markdown(response)

        if retrieved:
            with st.expander("View retrieved context (for demo)"):
                for i, doc in enumerate(retrieved, start=1):
                    st.markdown(f"**Chunk {i}**")
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
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("context"):
                with st.expander("View retrieved context (for demo)"):
                    for i, doc in enumerate(message["context"], start=1):
                        st.markdown(f"**Chunk {i}**")
                        st.info(doc)


def render_app(title, subtitle, generator_label, mode_description, get_chatbot, get_document_count):
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_session_state()
    render_sidebar(mode_description)

    st.markdown(f'<p class="main-header">🎓 {title}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{subtitle}</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Knowledge chunks", get_document_count())
    col2.metric("Retriever", "TF-IDF")
    col3.metric("Generator", generator_label)

    st.divider()

    render_chat_history()

    pending = st.session_state.pop("pending_question", None)
    if pending:
        handle_user_message(pending, get_chatbot)
        st.rerun()

    if query := st.chat_input("Type your college-related question here..."):
        handle_user_message(query, get_chatbot)
        st.rerun()
