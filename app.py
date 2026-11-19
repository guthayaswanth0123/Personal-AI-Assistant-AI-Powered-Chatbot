
import streamlit as st
from chatbot import ask_question

st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Personal AI Assistant")

st.caption(
    "Ask questions about your documents or anything else. "
    "I can help with both!"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Clear chat
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
question = st.chat_input("Ask me anything...")


if question:

    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)


    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                answer = ask_question(question)

            except Exception as e:
                answer = (
                    "Something went wrong. "
                    "Please check your API key, database "
                    "and terminal error.\n\n"
                    f"Error: {str(e)}"
                )

        st.markdown(answer)


    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
