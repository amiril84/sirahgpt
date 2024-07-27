from openai import OpenAI
import streamlit as st
import requests
import os

# Retrieve the API key and assistant ID from environment variables
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

client = OpenAI(api_key=api_key)
ASSISTANT_ID = assistant_id

st.title("💬 Chatbot")
st.caption("🚀 Sirah GPT powered by OpenAI")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Assalamualaikum, silahkan bertanya tentang sejarah Nabi Muhammad."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id, 
        role="user", 
        content=prompt
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, 
        assistant_id=ASSISTANT_ID
    )

    if run.status == "completed":
        msg = client.beta.threads.messages.list(thread_id=thread.id)
    else:
        msg = run.status
    
    ready_to_print_msg = msg.data[0].content[0].text.value
    
    st.session_state.messages.append({"role": "assistant", "content": ready_to_print_msg})
    st.chat_message("assistant").write(ready_to_print_msg)
