import streamlit as st
from scripts.config import load_config
from scripts.pdf_processing import process_pdfs
from scripts.retrieval import create_rag_chain
from scripts.history import get_session_history
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load environment variables
load_config()

# Set up Streamlit
st.set_page_config(page_title="PDF Query App", page_icon="📄", layout="wide")
st.title("🔍 Querying the PDF 📚")
st.write("Upload PDFs and chat with their content. Let the AI assist you in extracting valuable information from your documents.")

# Input the Groq API Key
api_key = st.sidebar.text_input("Enter your Groq API key:", type="password", placeholder="Your Groq API Key")

if api_key:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Upload PDFs")
    # File uploader for PDFs
    uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        retriever = process_pdfs(uploaded_files)

        # Initialize the LLM and RAG chain with the retriever
        llm = ChatGroq(groq_api_key=api_key, model_name="Gemma2-9b-It")
        rag_chain = create_rag_chain(llm, retriever)

        # Manage session state for chat history
        if 'store' not in st.session_state:
            st.session_state.store = {}

        # Chat interface
        st.sidebar.markdown("---")
        session_id = st.sidebar.text_input("Session ID", value="default_session")
        user_input = st.text_input("Your question:", placeholder="Type your question here...")

        if user_input:
            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain, get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )

            session_history = get_session_history(session_id)
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={
                    "configurable": {"session_id": session_id}
                },  # constructs a key "abc123" in `store`.
            )

            # Display results in a more visually appealing way
            st.markdown(f"<h2 style='color: #4CAF50;'>Assistant:</h2>", unsafe_allow_html=True)
            st.write(response['answer'])
            st.markdown(f"<h3 style='color: #FFC107;'>Chat History:</h3>", unsafe_allow_html=True)
            for message in session_history.messages:
                st.markdown(f"<p style='color: #2196F3;'>{message}</p>", unsafe_allow_html=True)
else:
    st.sidebar.warning("Please enter the Groq API Key to get started.")
