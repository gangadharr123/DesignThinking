import streamlit as st

from utils import load_css, check_authentication, render_sidebar
from voice_assistant import (
    record_audio,
    transcribe_audio,
    generate_response,
    text_to_speech,
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

gemini_key = st.session_state.get("gemini_key", st.secrets.get("GEMINI_API_KEY"))
gemini_key_input = st.text_input(
    "Gemini API Key", type="password", value=gemini_key or "", help="Required for generating responses."
)
if gemini_key_input:
    st.session_state.gemini_key = gemini_key_input

if st.button("Start Listening", use_container_width=True):
    with st.spinner("Listening..."):
        try:
            audio_data = record_audio()
            text = transcribe_audio(audio_data)
        except Exception as e:
            text = ""
            st.error(f"Error capturing audio: {e}")
    if text:
        st.session_state.conversation.append({"speaker": "You", "text": text})
        response = generate_response(text, api_key=st.session_state.get("gemini_key"))
        audio_bytes = text_to_speech(response)
        st.session_state.conversation.append({"speaker": "Assistant", "text": response, "audio": audio_bytes})
    else:
        st.warning("Could not understand audio.")

st.markdown("---")

st.subheader("Conversation")
for i, msg in enumerate(st.session_state.conversation):
    st.markdown(f"**{msg['speaker']}:** {msg['text']}")
    if msg["speaker"] == "Assistant" and msg.get("audio"):
        if st.button("Play Response", key=f"play_{i}"):
            st.audio(msg["audio"].getvalue(), format="audio/mp3")
