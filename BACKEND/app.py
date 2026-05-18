"""
AI Vaidya - Streamlit Frontend (Consultation + History)
Run with:  python -m streamlit run app.py
"""

import streamlit as st
import re as _re
import io
import datetime
import speech_recognition as sr

from rag import init, get_answer

# ── Page config ─────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Vaidya - Ayurveda Assistant",
    page_icon="🌿",
    layout="centered",
)

# ── Session state ───────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "voice_query" not in st.session_state:
    st.session_state.voice_query = ""
if "query_input" not in st.session_state:
    st.session_state.query_input = ""
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []  # [{"role": "user"|"assistant", "content": str, "sources": [...]}]

# ── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Manrope:wght@400;500;600;700&display=swap');

/* ── Base ─────────────────────────────────────────── */
.stApp {
    background: radial-gradient(circle at 50% -20%, #fbf9f5 0%, #efeeea 40%, #e4e2de 100%) !important;
    background-attachment: fixed !important;
}
html, body, .stApp, .stApp *, [class*="css"],
p, span, div, li, label, input,
h1, h2, h3, h4, h5, h6,
.stMarkdown, .stMarkdown p, .stMarkdown span,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    font-family: 'Manrope', sans-serif !important;
    color: #1b1c1a !important;
}
header[data-testid="stHeader"] {
    background: #fbf9f5 !important;
    border-bottom: 1px solid #d1c5b4;
    box-shadow: 0 1px 4px rgba(119,90,25,0.06);
}

/* ── Tabs — styled like bottom nav ────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #f5f3ef;
    border: 1px solid #d1c5b4;
    border-radius: 16px;
    padding: 4px;
    gap: 4px;
    justify-content: center;
    margin-bottom: 8px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Manrope', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #7f7667 !important;
    border-radius: 12px;
    padding: 10px 24px;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: rgba(197,160,89,0.15) !important;
    color: #775a19 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Top Bar ──────────────────────────────────────── */
.topbar {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 0; border-bottom: 1px solid #d1c5b4;
    margin-bottom: 8px;
}
.topbar-title {
    font-family: 'Libre Caslon Text', serif !important;
    font-size: 26px !important; font-weight: 400 !important;
    letter-spacing: 0.15em; color: #775a19 !important;
    margin: 0; line-height: 36px;
}

/* ── Hero ─────────────────────────────────────────── */
.hero {
    text-align: center; padding: 40px 24px 24px;
}
.hero-icon {
    display: inline-flex; align-items: center; justify-content: center;
    width: 56px; height: 56px; margin-bottom: 20px;
    font-size: 36px; color: #775a19;
}
.hero-heading {
    font-family: 'Libre Caslon Text', serif !important;
    font-size: 28px !important; font-weight: 400 !important;
    line-height: 38px; color: #775a19 !important;
    margin: 0 0 14px; letter-spacing: -0.01em;
}
.hero-subtitle {
    font-family: 'Libre Caslon Text', serif !important;
    font-size: 15px !important; font-style: italic;
    line-height: 24px; color: #4e4639 !important;
    max-width: 460px; margin: 0 auto; opacity: 0.85;
}

/* ── History Hero ─────────────────────────────────── */
.history-hero {
    text-align: center; padding: 40px 24px 24px;
}
.history-heading {
    font-family: 'Libre Caslon Text', serif !important;
    font-size: 28px !important; font-weight: 400 !important;
    color: #1b1c1a !important; margin: 0 0 10px;
}
.history-subtitle {
    font-family: 'Libre Caslon Text', serif !important;
    font-size: 15px !important; font-style: italic;
    color: #4e4639 !important; max-width: 460px;
    margin: 0 auto; opacity: 0.85; line-height: 24px;
}

/* ── Try Asking label ─────────────────────────────── */
.try-label {
    font-family: 'Manrope', sans-serif !important;
    font-size: 12px !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: 0.2em;
    color: #7f7667 !important; text-align: center;
    margin: 28px 0 16px;
}

/* ── Suggestion pills ─────────────────────────────── */
div.stButton > button {
    background: rgba(255,255,255,0.3) !important;
    border: 1.5px solid #d1c5b4 !important;
    border-radius: 28px !important;
    padding: 12px 24px !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 15px !important; font-weight: 400 !important;
    color: #4e4639 !important; cursor: pointer;
    transition: all 0.25s ease; width: 100%;
    box-shadow: 0 1px 4px rgba(119,90,25,0.03);
}
div.stButton > button:hover {
    background: rgba(244,239,230,0.6) !important;
    border-color: #c5a059 !important;
    color: #775a19 !important;
    box-shadow: 0 4px 16px rgba(197,160,89,0.12) !important;
    transform: translateY(-1px);
}
div.stButton > button:active, div.stButton > button:focus {
    background: rgba(197,160,89,0.1) !important;
    border-color: #c5a059 !important;
    color: #775a19 !important;
    box-shadow: none !important;
}

/* ── Input ─────────────────────────────────────────── */
.stTextInput > div > div > input {
    border-radius: 20px !important;
    border: 1.5px solid #d1c5b4 !important;
    padding: 14px 20px !important;
    font-size: 15px !important;
    font-family: 'Manrope', sans-serif !important;
    background: #ffffff !important;
    color: #1b1c1a !important;
    box-shadow: 0 1px 6px rgba(119,90,25,0.03) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #7f7667 !important; font-style: italic;
}
.stTextInput > div > div > input:focus {
    border-color: #c5a059 !important;
    box-shadow: 0 0 0 3px rgba(197,160,89,0.15) !important;
}

/* ── Mic/Audio recorder overrides ─────────────────── */
iframe[title="audio_recorder_streamlit.audio_recorder"] {
    border: none !important;
}
/* Style the recorder container */
div[data-testid="column"]:last-child {
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ── Section Label ────────────────────────────────── */
.section-label {
    font-family: 'Manrope', sans-serif !important;
    font-size: 12px !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: #7f7667 !important; margin: 24px 0 10px;
}

/* ── Answer Card ──────────────────────────────────── */
.answer-card {
    background: rgba(255,255,255,0.5);
    backdrop-filter: blur(8px);
    border: 1.5px solid #d1c5b4;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(119,90,25,0.06);
    line-height: 1.75; font-size: 15px;
}
.answer-card p {
    color: #1b1c1a !important; font-size: 15px !important;
    line-height: 24px !important; margin-bottom: 6px;
}
.answer-card strong { color: #775a19 !important; font-weight: 600; }
.answer-card ul { padding-left: 16px; margin: 8px 0 0; list-style: none; }
.answer-card li {
    margin-bottom: 8px; line-height: 24px; font-size: 15px;
    color: #1b1c1a !important; position: relative; padding-left: 16px;
}
.answer-card li::before {
    content: ''; position: absolute; left: 0; top: 10px;
    width: 6px; height: 6px; border-radius: 50%; background: #c5a059;
}

/* ── Source Card ───────────────────────────────────── */
.source-card {
    background: rgba(255,255,255,0.4);
    border: 1.5px solid #d1c5b4;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    transition: all 0.2s;
}
.source-card:hover {
    box-shadow: 0 6px 24px rgba(197,160,89,0.12);
    border-color: #c5a059;
}
.source-header {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 8px;
}
.source-file {
    font-size: 12px !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: 0.05em;
    color: #775a19 !important;
}
.source-badge {
    font-size: 11px !important; font-weight: 700 !important;
    background: rgba(197,160,89,0.15);
    color: #5d4201 !important;
    padding: 3px 10px; border-radius: 20px;
}
.source-divider { width: 28px; height: 2px; background: #c5a059; margin: 6px 0 10px; }
.source-excerpt {
    font-family: 'Libre Caslon Text', serif !important;
    font-style: italic; font-size: 13px !important;
    line-height: 21px !important; color: #4e4639 !important;
}

/* ── History Card ─────────────────────────────────── */
.history-card {
    background: rgba(255,255,255,0.5);
    border: 1.5px solid #d1c5b4;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 14px;
    transition: all 0.2s;
    cursor: default;
}
.history-card:hover {
    box-shadow: 0 6px 24px rgba(197,160,89,0.12);
    border-color: #c5a059;
}
.history-card-header {
    display: flex; align-items: flex-start;
    justify-content: space-between; margin-bottom: 10px;
}
.history-card-icon {
    width: 40px; height: 40px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0; margin-right: 12px;
}
.history-q {
    font-family: 'Libre Caslon Text', serif !important;
    font-size: 17px !important; font-weight: 700 !important;
    color: #1b1c1a !important; margin: 0 0 2px; line-height: 24px;
}
.history-date {
    font-size: 12px !important; font-weight: 600 !important;
    color: #7f7667 !important; text-transform: uppercase;
    letter-spacing: 0.05em;
}
.history-excerpt {
    font-size: 14px !important; line-height: 22px !important;
    color: #4e4639 !important; margin: 6px 0 10px;
}
.history-tags { display: flex; gap: 6px; flex-wrap: wrap; }
.history-tag {
    font-size: 12px !important; font-weight: 600 !important;
    color: #4e4639 !important; background: rgba(244,239,230,0.6);
    border: 1px solid #d1c5b4; border-radius: 20px;
    padding: 3px 12px;
}
.history-empty {
    text-align: center; padding: 60px 24px;
    color: #7f7667 !important;
}
.history-empty-icon {
    font-size: 48px; margin-bottom: 16px; opacity: 0.4;
}
.history-empty-text {
    font-family: 'Libre Caslon Text', serif !important;
    font-size: 18px !important; font-style: italic;
    color: #7f7667 !important;
}

/* ── Footer ───────────────────────────────────────── */
.app-footer {
    background: #e4e2de; border: 1px solid #d1c5b4;
    border-radius: 16px; padding: 24px;
    margin-top: 40px; text-align: center;
}
.footer-brand {
    font-family: 'Manrope', sans-serif !important;
    font-size: 18px !important; font-weight: 600 !important;
    color: #775a19 !important; margin-bottom: 4px;
}
.footer-copy {
    font-size: 13px !important; color: #4e4639 !important; margin: 2px 0;
}

/* ── Streamlit overrides ──────────────────────────── */
.stSpinner > div { color: #775a19 !important; }
.stHorizontalBlock { align-items: center; }

/* ── Chat bubbles ────────────────────────────── */
.chat-window {
    max-height: 500px; overflow-y: auto;
    padding: 16px 0; margin-bottom: 12px;
}
.chat-bubble {
    padding: 14px 20px; margin-bottom: 10px;
    border-radius: 16px; max-width: 85%;
    line-height: 1.65; font-size: 15px;
}
.chat-user {
    background: rgba(197,160,89,0.15);
    border: 1.5px solid #c5a059;
    margin-left: auto; text-align: right;
    border-bottom-right-radius: 4px;
}
.chat-user p { color: #5d4201 !important; font-weight: 500; margin: 0; }
.chat-assistant {
    background: rgba(255,255,255,0.55);
    border: 1.5px solid #d1c5b4;
    margin-right: auto;
    border-bottom-left-radius: 4px;
}
.chat-assistant p { color: #1b1c1a !important; margin-bottom: 4px; }
.chat-assistant strong { color: #775a19 !important; }
.chat-assistant ul { padding-left: 16px; margin: 6px 0 0; list-style: none; }
.chat-assistant li {
    margin-bottom: 6px; position: relative; padding-left: 14px;
    font-size: 14px; line-height: 22px;
}
.chat-assistant li::before {
    content: ''; position: absolute; left: 0; top: 9px;
    width: 5px; height: 5px; border-radius: 50%; background: #c5a059;
}
.chat-role {
    font-size: 11px !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: 0.08em;
    color: #7f7667 !important; margin-bottom: 4px;
}
.chat-new-btn {
    text-align: center; margin: 8px 0;
}

/* ── Voice expander ───────────────────────────────── */
.streamlit-expanderHeader {
    font-family: 'Manrope', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #775a19 !important;
    background: rgba(255,255,255,0.3) !important;
    border: 1.5px solid #d1c5b4 !important;
    border-radius: 14px !important;
}
.streamlit-expanderHeader:hover {
    color: #775a19 !important;
    border-color: #c5a059 !important;
}
[data-testid="stExpander"] {
    border: 1.5px solid #d1c5b4 !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.3) !important;
}
[data-testid="stExpander"] details summary {
    padding: 12px 16px !important;
}
[data-testid="stExpander"] details summary p,
[data-testid="stExpander"] details summary span[data-testid="stMarkdownContainer"] p {
    color: #775a19 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
/* Hide the Material Symbols text fallback ("keyboard_arrow_right") */
[data-testid="stIconMaterial"] {
    font-size: 0px !important;
    display: inline-block;
    width: 18px !important; height: 18px !important;
    overflow: hidden;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23c5a059'%3E%3Cpath d='M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z'/%3E%3C/svg%3E") center/contain no-repeat;
    vertical-align: middle;
}
details[open] > summary [data-testid="stIconMaterial"] {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23c5a059'%3E%3Cpath d='M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z'/%3E%3C/svg%3E") !important;
}
[data-testid="stExpander"] details summary svg {
    color: #c5a059 !important;
    width: 20px !important;
    height: 20px !important;
}

/* ── Audio input widget ───────────────────────────── */
[data-testid="stAudioInput"] > div {
    border: 1.5px solid #d1c5b4 !important;
    border-radius: 12px !important;
    background: #ffffff !important;
}
[data-testid="stAudioInput"] button {
    color: #c5a059 !important;
    background: rgba(197,160,89,0.08) !important;
    border: 1px solid #d1c5b4 !important;
}
[data-testid="stAudioInput"] button:hover {
    background: rgba(197,160,89,0.2) !important;
    border-color: #c5a059 !important;
}
/* Force ALL icons inside audio input to gold — no black icons */
[data-testid="stAudioInput"] svg,
[data-testid="stAudioInput"] button svg,
[data-testid="stAudioInput"] svg path,
[data-testid="stAudioInput"] svg circle,
[data-testid="stAudioInput"] svg rect {
    fill: #c5a059 !important;
    color: #c5a059 !important;
    stroke: #c5a059 !important;
}
[data-testid="stAudioInput"] [data-testid="stIconMaterial"],
[data-testid="stExpander"] [data-testid="stIconMaterial"] {
    color: #c5a059 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load vector store ───────────────────────────────────────────
@st.cache_resource(show_spinner="Loading Ayurveda knowledge base...")
def load_vectorstore():
    return init()

vectorstore = load_vectorstore()

# ── Top Bar ─────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="#775a19"><path d="M12 2C9.5 5 7 7 7 10c0 2.2 1.3 4 3.3 4.8C9.5 15.5 9 16.7 9 18h6c0-1.3-.5-2.5-1.3-3.2C15.7 14 17 12.2 17 10c0-3-2.5-5-5-8z"/><path d="M11 18h2v4h-2z"/></svg>
    <h1 class="topbar-title">AI VAIDYA</h1>
</div>
""", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────
tab_consult, tab_history, tab_about = st.tabs(["🩺  Consult", "📜  History", "🪷  About"])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CONSULT TAB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_consult:

    # ── Hero ────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-icon"><svg width="36" height="36" viewBox="0 0 24 24" fill="#775a19"><path d="M12 2C9.5 5 7 7 7 10c0 2.2 1.3 4 3.3 4.8C9.5 15.5 9 16.7 9 18h6c0-1.3-.5-2.5-1.3-3.2C15.7 14 17 12.2 17 10c0-3-2.5-5-5-8z"/><circle cx="12" cy="9" r="2" fill="#c5a059"/></svg></div>
        <h2 class="hero-heading">Namaste. I am<br>your AI Vaidya.</h2>
        <p class="hero-subtitle">
            Ask me anything about Ayurveda. I will answer only from your provided knowledge base.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Suggestion Pills ────────────────────────────────────
    st.markdown('<div class="try-label">Try Asking:</div>', unsafe_allow_html=True)

    SUGGESTIONS = [
        "What are the three doshas?",
        "How does digestion work?",
        "What are the three Gunas?",
        "Herbs for cough and cold?",
        "What is Panchakarma?",
        "How does turmeric help in healing?",
    ]

    clicked_q = None
    for q in SUGGESTIONS:
        if st.button(q, key=f"pill_{q}", use_container_width=True):
            clicked_q = q

    # ── Voice Input (before text input so it can set state) ──
    st.markdown("---")

    with st.expander("Voice Input — Record your question", expanded=False):
        st.markdown(
            '<p style="font-size:13px; color:#7f7667 !important; margin:0 0 8px;">'
            'Record your question — it will auto-fill the search box and run.</p>',
            unsafe_allow_html=True,
        )
        audio_value = st.audio_input(
            "Record your question",
            label_visibility="collapsed",
            key="voice_input",
        )
        if audio_value is not None:
            # Hash the audio to avoid re-processing the same recording
            audio_bytes = audio_value.read()
            audio_hash = hash(audio_bytes)
            if audio_hash != st.session_state.get("last_audio_hash", None):
                try:
                    recognizer = sr.Recognizer()
                    audio_file = io.BytesIO(audio_bytes)
                    with sr.AudioFile(audio_file) as source:
                        audio_data = recognizer.record(source)
                    voice_text = recognizer.recognize_google(audio_data)
                    st.session_state.last_audio_hash = audio_hash
                    st.session_state.query_input = voice_text
                    st.rerun()
                except sr.UnknownValueError:
                    st.warning("Could not understand audio. Please try again.")
                except sr.RequestError:
                    st.warning("Speech service unavailable. Please type.")
                except Exception as e:
                    st.warning(f"Voice error: {e}")

    # ── Text Input ───────────────────────────────────────────
    if clicked_q:
        st.session_state.query_input = clicked_q

    query = st.text_input(
        "Ask a question about Ayurveda",
        placeholder="Ask a question about Ayurveda...",
        key="query_input",
        label_visibility="collapsed",
    )

    # ── Process new query ────────────────────────────────
    if query:
        # Avoid re-processing the same query on reruns
        last_user = None
        if st.session_state.chat_messages:
            last_user = st.session_state.chat_messages[-1 if st.session_state.chat_messages[-1]["role"] == "user" else -2].get("content") if len(st.session_state.chat_messages) >= 1 else None

        if query != last_user:
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": query, "sources": []})

            with st.spinner("Searching knowledge base..."):
                result = get_answer(query, vectorstore, chat_context=st.session_state.chat_messages[:-1])

            # Add assistant message
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": result["answer"],
                "sources": result["sources"],
            })

            # Save to history tab
            st.session_state.chat_history.insert(0, {
                "query": query,
                "answer": result["answer"],
                "sources": result["sources"],
                "timestamp": datetime.datetime.now().strftime("%B %d, %Y — %I:%M %p"),
            })

            # Clear input for next question
            st.session_state.query_input = ""
            st.rerun()

    # ── Chat Window ────────────────────────────────────
    if st.session_state.chat_messages:
        st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)

        # New conversation button
        if st.button("🗘 New Conversation", key="new_convo", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.query_input = ""
            st.rerun()

        st.markdown('<div class="chat-window">', unsafe_allow_html=True)

        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'''
                <div class="chat-bubble chat-user">
                    <div class="chat-role">You</div>
                    <p>{msg["content"]}</p>
                </div>
                ''', unsafe_allow_html=True)
            else:
                # Format assistant answer
                answer_text = msg["content"]
                lines = answer_text.split("\n")
                bullet_items = [l.lstrip("- ").lstrip("* ") for l in lines if l.strip().startswith(("- ", "* "))]
                non_bullets = [l for l in lines if not l.strip().startswith(("- ", "* ")) and l.strip()]

                html = ""
                for line in non_bullets:
                    line = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                    html += f"<p>{line}</p>"
                if bullet_items:
                    html += "<ul>"
                    for item in bullet_items:
                        item = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                        html += f"<li>{item}</li>"
                    html += "</ul>"

                st.markdown(f'''
                <div class="chat-bubble chat-assistant">
                    <div class="chat-role">AI Vaidya</div>
                    {html}
                </div>
                ''', unsafe_allow_html=True)

                # Show sources for this message
                if msg.get("sources"):
                    with st.expander(f"Sources ({len(msg['sources'])} citations)", expanded=False):
                        for src in msg["sources"]:
                            score_pct = f"{abs(src['relevance']) * 100:.0f}%"
                            excerpt = src["text"][:180] + "..." if len(src["text"]) > 180 else src["text"]
                            st.markdown(f'''
                            <div class="source-card">
                                <div class="source-header">
                                    <span class="source-file">{src['file']} — Page {src['page']}</span>
                                    <span class="source-badge">{score_pct} match</span>
                                </div>
                                <div class="source-divider"></div>
                                <div class="source-excerpt">{excerpt}</div>
                            </div>
                            ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HISTORY TAB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_history:

    st.markdown("""
    <div class="history-hero">
        <h2 class="history-heading">Sacred Consultations</h2>
        <p class="history-subtitle">
            Review the wisdom shared in your previous journeys toward holistic balance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="history-empty">
            <div class="history-empty-icon">📜</div>
            <p class="history-empty-text">No consultations yet.<br>Ask your first question to begin.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Summary stats ───────────────────────────────
        total = len(st.session_state.chat_history)
        st.markdown(f'<div class="section-label">{total} Consultation{"s" if total != 1 else ""}</div>', unsafe_allow_html=True)

        # ── History cards ───────────────────────────────
        ICONS = ["🪷", "🌿", "🍃", "☘", "🌾", "🌻"]

        for i, entry in enumerate(st.session_state.chat_history):
            icon_bg = ["#f5e6d8", "#e6f0e6", "#e8e4db", "#fef3e0", "#e8eed8", "#fdf6e3"][i % 6]
            icon = ICONS[i % len(ICONS)]

            # Extract a few key words as tags
            q_lower = entry["query"].lower()
            tags = []
            tag_keywords = {
                "dosha": "Doshas", "vata": "Vata", "pitta": "Pitta", "kapha": "Kapha",
                "digestion": "Digestion", "herb": "Herbs", "turmeric": "Turmeric",
                "panchakarma": "Panchakarma", "guna": "Gunas", "diet": "Diet",
                "ayurveda": "Ayurveda", "yoga": "Yoga", "meditation": "Meditation",
                "sleep": "Sleep", "cough": "Remedies", "cold": "Remedies",
                "healing": "Healing", "balance": "Balance", "energy": "Energy",
            }
            for kw, tag in tag_keywords.items():
                if kw in q_lower and tag not in tags:
                    tags.append(tag)
            if not tags:
                tags = ["Ayurveda"]

            # Truncate answer for excerpt
            excerpt = entry["answer"][:150].replace("**", "").replace("\n", " ").replace("- ", "")
            if len(entry["answer"]) > 150:
                excerpt += "..."

            num_sources = len(entry["sources"])
            tags_html = "".join(f'<span class="history-tag">{t}</span>' for t in tags[:3])

            st.markdown(f"""
            <div class="history-card">
                <div class="history-card-header">
                    <div style="display:flex; align-items:center;">
                        <div class="history-card-icon" style="background:{icon_bg};">{icon}</div>
                        <div>
                            <div class="history-q">{entry["query"]}</div>
                            <div class="history-date">{entry["timestamp"]}</div>
                        </div>
                    </div>
                    <span class="source-badge">{num_sources} Source{"s" if num_sources != 1 else ""}</span>
                </div>
                <p class="history-excerpt">{excerpt}</p>
                <div class="history-tags">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Clear history button ────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear History", key="clear_history", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ABOUT TAB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_about:

    st.markdown("""
    <div class="history-hero">
        <h2 class="history-heading">About AI Vaidya</h2>
        <p class="history-subtitle">
            Ancient wisdom, modern intelligence — your personal Ayurvedic consultant.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── What is AI Vaidya ───────────────────────────────
    st.markdown('<div class="section-label">What is AI Vaidya?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="answer-card">
        <p><strong>AI Vaidya</strong> is an intelligent Ayurvedic knowledge assistant that brings
        the ancient wisdom of Ayurveda to your fingertips. Powered by a <strong>Retrieval-Augmented
        Generation (RAG)</strong> pipeline, it answers your health and wellness questions using
        only verified Ayurvedic texts &mdash; never hallucinating or guessing.</p>
        <p>The name <em>"Vaidya"</em> (वैद्य) means a learned physician in Sanskrit. Just like a
        traditional Vaidya, AI Vaidya consults the source texts before offering guidance.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── How It Works ────────────────────────────────────
    st.markdown('<div class="section-label">How It Works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="answer-card">
        <ul>
            <li><strong>PDF Knowledge Base</strong> &mdash; Ayurvedic texts are ingested, chunked, and
            embedded into a vector database for fast semantic search.</li>
            <li><strong>Smart Retrieval</strong> &mdash; When you ask a question, the most relevant
            passages are retrieved using cosine similarity on sentence embeddings.</li>
            <li><strong>LLM Formatting</strong> &mdash; Google Gemini 2.0 Flash summarizes and formats
            the retrieved context into a clean, readable answer.</li>
            <li><strong>Offline Fallback</strong> &mdash; If the API is unavailable, answers are
            generated locally from the retrieved text &mdash; no internet required.</li>
            <li><strong>Voice Input</strong> &mdash; Speak your question and it will be transcribed
            and searched automatically.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Tech Stack ──────────────────────────────────────
    st.markdown('<div class="section-label">Technology Stack</div>', unsafe_allow_html=True)

    tech_items = [
        ("LangChain", "Document loading, text splitting, and RAG orchestration"),
        ("ChromaDB", "Persistent vector store for fast semantic search"),
        ("SentenceTransformers", "all-MiniLM-L6-v2 model for text embeddings"),
        ("Google Gemini 2.0 Flash", "LLM for intelligent answer formatting"),
        ("Streamlit", "Interactive web interface with custom Sacred Wisdom design"),
        ("SpeechRecognition", "Voice-to-text transcription for hands-free queries"),
    ]

    for name, desc in tech_items:
        st.markdown(f"""
        <div class="source-card">
            <div class="source-header">
                <span class="source-file">{name}</span>
            </div>
            <div class="source-divider"></div>
            <div class="source-excerpt">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Disclaimer ──────────────────────────────────────
    st.markdown('<div class="section-label">Disclaimer</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="answer-card" style="border-color:#c5a059;">
        <p style="font-style:italic; color:#775a19 !important;">
            AI Vaidya is an educational tool designed to make Ayurvedic knowledge accessible.
            It is <strong>not a substitute</strong> for professional medical advice, diagnosis,
            or treatment. Always consult a qualified healthcare provider for medical concerns.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div class="footer-brand">AI Vaidya</div>
    <p class="footer-copy">Offline RAG + Gemini · LangChain + ChromaDB + SentenceTransformers</p>
    <p class="footer-copy">Not a substitute for professional medical advice</p>
</div>
""", unsafe_allow_html=True)
