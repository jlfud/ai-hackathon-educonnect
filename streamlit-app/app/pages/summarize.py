# pages/summarize.py
import streamlit as st
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_base = os.getenv("OPENAI_BASE_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("Missing OpenAI API Key! Make sure it's set in your .env file.")
    st.stop()

client = openai.OpenAI(api_key=openai.api_key)

st.title("Summary of Requests")

if "messages" not in st.session_state or not st.session_state.messages:
    st.write("No messages to summarize yet.")
else:
    # Build conversation text including both the assistant's prompts and the user's responses.
    conversation_text = ""
    for msg in st.session_state.messages:
        if msg["role"] in ["assistant", "user"]:
            role_label = "Assistant" if msg["role"] == "assistant" else "User"
            conversation_text += f"{role_label}: {msg['content']}\n"

    placeholder = st.empty()
    placeholder.write("Loading summary...")

    try:
        response = client.chat.completions.create(
            model="anthropic.claude-3.5-haiku",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant whose sole purpose is to match schools and students in need with nonprofit organizations that can help them. "
                        "Your task is to ask only relevant questions to collect essential information from the school. "
                        "Focus on asking for details such as the school's location, school size, and what specific kind of help they need. "
                        "Now, based on the following conversation—which includes both your prompts and the user's responses—provide a concise summary that captures the essential details needed for matching schools and students with nonprofit organizations."
                    )
                },
                {"role": "user", "content": conversation_text}
            ],
        )
        summary = response.choices[0].message.content
        placeholder.empty()
        st.subheader("Summary:")
        st.write(summary)
    except Exception as e:
        placeholder.empty()
        st.error(f"Error summarizing conversation: {str(e)}")