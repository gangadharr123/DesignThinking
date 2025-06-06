import io
from typing import Optional

import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai


def record_audio(timeout: int = 5, phrase_time_limit: int = 10) -> sr.AudioData:
    """Record audio from the default microphone.

    Raises
    ------
    RuntimeError
        If no default input device is available.
    """
    recognizer = sr.Recognizer()
    try:
        if not sr.Microphone.list_microphone_names():
            raise RuntimeError("No default input device available")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return audio
    except OSError as e:
        raise RuntimeError("No default input device available") from e


def transcribe_audio(audio: sr.AudioData) -> str:
    """Convert recorded audio to text using Google's free API."""
    recognizer = sr.Recognizer()
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""


def generate_response(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "gemini-pro",
    context: Optional[str] = None,
) -> str:
    """Generate a response using the Gemini API.

    Parameters
    ----------
    prompt: str
        The user's prompt.
    api_key: Optional[str]
        API key for Gemini. If provided, it overrides environment configuration.
    model: str
        Gemini model name.
    context: Optional[str]
        Additional context prepended to the prompt to help the model generate
        informed answers.
    """

    if context:
        prompt = f"{context}\n{prompt}"

    if api_key:
        genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


def text_to_speech(text: str) -> io.BytesIO:
    """Convert text to speech and return audio bytes."""
    tts = gTTS(text)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes
