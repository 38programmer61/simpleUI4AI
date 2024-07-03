
import streamlit as st

def send_message_to_ai(chain, chat_history, message):

    # chat_history.add_user_message(message)
    response = chain.invoke({"messages": st.session_state.messages})
    # chat_history.add_ai_message(response.content)
    return response.content
