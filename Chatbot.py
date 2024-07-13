import numpy as np
import pandas as pd
import openai
import streamlit as st


openai_api_key = 'sk-proj-kmBbNZMCqVEBfXNHQJZ4T3BlbkFJpV4IBfkl9QIXWf8kxGnZ'

st.title("WELCOME TO MY CHATBOT... 🧑‍💻💬 ")
"""
Note: This chatbot will give a warning if you put any sensitive information
"""

# Function to check for personal information using OpenAI's content filter
def check_for_personal_info(prompt,openai_api_key):
    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a highly intelligent assistant. Your task is to determine if the following message contains any personal information such as names, email addresses, phone numbers, or any other details that could be used to identify an individual.Please Classify it only as 1 or 0 where 1 means it contains personal information and 0 means it doesnt contain any personal information"},
                {"role": "user", "content": prompt}
            ]
        )
        
        # The response from GPT-3.5-turbo will be in the `choices` list, usually with detailed information.
        # You need to interpret the response to decide if it indicates personal information is present.
        # This might require parsing the text of the response for specific keywords or phrases.
        ai_response = response['choices'][0]['message']['content'].strip()  # Adjusted based on correct API usage
        return ai_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are an AI assistant."}
    ]

# Display previous messages
for message in st.session_state["messages"]:
    # Check the role to determine how to display the message
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    elif message["role"] == "assistant":
        st.chat_message("assistant").write(message["content"])
    else:  # Default case, for system messages or any other type
        st.text(message["content"])  # Using st.text for system messages or other roles

if prompt := st.chat_input():
    openai.api_key = openai_api_key
    if check_for_personal_info(prompt,openai_api_key)=='1':
        st.warning("Warning: Please do not share personal information.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Assuming this function call is correctly displaying the user's message in your setup
        st.chat_message("user").write(prompt)
    
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=st.session_state.messages)
        msg = response.choices[0].message
        st.session_state.messages.append({"role": "assistant", "content": msg.content})
    
    # Display the assistant's response immediately after getting it
        st.chat_message("assistant").write(msg.content)

if st.button('Clear Conversation'):
    st.session_state.messages = [
        {"role": "system", "content": ""}
    ]
    st.experimental_rerun()
