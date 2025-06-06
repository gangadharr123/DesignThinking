import streamlit as st
import os

from utils import load_css, check_authentication, render_sidebar, format_currency
from voice_assistant import (
    record_audio,
    transcribe_audio,
    generate_response,
    text_to_speech,
    ResponseGenerationError,
)

st.set_page_config(page_title="Voice Assistant", page_icon="🎙️", layout="wide")

load_css()
check_authentication()

if st.session_state.get("logged_in", False):
    render_sidebar()

st.markdown(
    """
    <div class="breadcrumb">
        <span>🎓 StudyAbroad Platform</span> > <span>Voice Assistant</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("🎙️ Voice Assistant")
st.markdown("Talk to the assistant for quick answers to your questions.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

default_key = os.environ.get("GEMINI_API_KEY", "")
try:
    default_key = st.secrets.get("GEMINI_API_KEY", default_key)
except Exception:
    pass
gemini_key = st.session_state.get("gemini_key", default_key)
gemini_key_input = st.text_input(
    "Gemini API Key", type="password", value=gemini_key or "", help="Required for generating responses."
)
if gemini_key_input:
    st.session_state.gemini_key = gemini_key_input

# Build context from budget and expenses if available
context = ""
if "budget" in st.session_state:
    total_budget = sum(st.session_state.budget.values())
    total_spent = 0.0
    if "expenses" in st.session_state:
        total_spent = sum(exp.get("amount", 0) for exp in st.session_state.expenses)
    remaining = total_budget - total_spent
    context = (
        "Budget summary: "
        f"Total budget {format_currency(total_budget)}, "
        f"total spent {format_currency(total_spent)}, "
        f"remaining balance {format_currency(remaining)}."
    )

if st.button("Start Listening", use_container_width=True):
    with st.spinner("Listening..."):
        try:
            audio_data = record_audio()
            text = transcribe_audio(audio_data)
        except Exception as e:
            text = ""
            st.error(f"Error capturing audio: {e}")
            if "No default input device" in str(e):
                st.info("Please connect a microphone and ensure it is set as the default input device.")
    if text:
        st.session_state.conversation.append({"speaker": "You", "text": text})
        try:
            response = generate_response(
                text,
                api_key=st.session_state.get("gemini_key"),
                context=context,
            )
        except ResponseGenerationError as e:
            st.error(f"Error generating response: {e}")
            response = None

        if response:
            audio_bytes = text_to_speech(response)
            st.session_state.conversation.append(
                {"speaker": "Assistant", "text": response, "audio": audio_bytes}
            )
    else:
        st.warning("Could not understand audio.")

st.markdown("---")

st.subheader("Conversation")
for i, msg in enumerate(st.session_state.conversation):
    st.markdown(f"**{msg['speaker']}:** {msg['text']}")
    if msg["speaker"] == "Assistant" and msg.get("audio"):
        if st.button("Play Response", key=f"play_{i}"):
            st.audio(msg["audio"].getvalue(), format="audio/mp3")
