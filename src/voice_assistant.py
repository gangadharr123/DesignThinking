import io
from typing import Optional

import speech_recognition as sr
from gtts import gTTS
import openai


def record_audio(timeout: int = 5, phrase_time_limit: int = 10) -> sr.AudioData:
    """Record audio from the default microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return audio


def transcribe_audio(audio: sr.AudioData) -> str:
    """Convert recorded audio to text using Google's free API."""
    recognizer = sr.Recognizer()
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""


def generate_response(prompt: str, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo") -> str:
    """Generate a response using the OpenAI API."""
    if api_key:
        openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error: {e}"


def text_to_speech(text: str) -> io.BytesIO:
    """Convert text to speech and return audio bytes."""
    tts = gTTS(text)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes
