---
title: DesignThinking
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
pinned: false
short_description: Prototype for Design Thinking group project
---

# Welcome to Streamlit!

Edit `/src/streamlit_app.py` to customize this app to your heart's desire. :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

## Voice Assistant

The app includes a simple voice assistant powered by the Gemini API. Navigate to
**Voice Assistant** from the sidebar or dashboard to start a conversation. You
will need a valid Gemini API key for generating responses. Install the
`google-generativeai` package listed in `requirements.txt` to enable the Gemini
client.

1. Enter your API key when prompted.
2. Click **Start Listening** to record your question.
3. After processing, play back the synthesized answer with the **Play Response**
   button.
