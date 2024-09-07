from langchain_community.chat_message_histories import ChatMessageHistory
import streamlit as st

def get_session_history(session_id):
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]
