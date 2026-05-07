import streamlit as st
from chatbot_logic import get_answer

st.set_page_config(page_title="Biotech Q&A Chatbot", page_icon="🧬")

st.title("🧬 Biotech Q&A Chatbot")
st.caption("Database + AI Powered Biotechnology Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
# User input box (chat-style)
user_input = st.chat_input("Ask a biotechnology question...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    bot_reply = get_answer(user_input)

    # Show bot message
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
    with st.chat_message("assistant"):
        st.markdown(bot_reply)