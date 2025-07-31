# streamlit_app.py

import streamlit as st
from src.config import DATA_PATH, DB_FAISS_PATH
from src.utils import stylish_heading
from src.loader import load_pdf_files
from src.chunker import create_chunks
from src.embedding import get_embedding_model
from src.vectorstore import build_vector_db, load_vector_db
from src.model_loader import load_llm
from src.prompts import CUSTOM_PROMPT_TEMPLATE, set_custom_prompt
from src.qa_chain import setup_qa_chain
import os

# Page config
st.set_page_config(page_title="Universal AI Chatbot", page_icon="🧠", layout="centered")

# Header
stylish_heading()
st.markdown("<h2 style='text-align: center;'>🧠 Ask Me Anything From Your PDFs</h2>", unsafe_allow_html=True)
st.markdown("✅ Powered by **Offline Mistral** + **FAISS**. Upload `.pdf` files below to update knowledge base automatically.")

st.divider()

# 📅 PDF Upload Section
uploaded_files = st.file_uploader("Upload your PDFs here", type=["pdf"], accept_multiple_files=True)

# Auto-refresh Knowledge Base on Upload
if uploaded_files:
    os.makedirs(DATA_PATH, exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = os.path.join(DATA_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success("Files uploaded successfully! Updating Knowledge Base...")

    with st.spinner("Processing uploaded documents..."):
        documents = load_pdf_files(DATA_PATH)
        chunks = create_chunks(documents)
        embedding_model = get_embedding_model()
        build_vector_db(chunks, embedding_model, DB_FAISS_PATH)
    st.success("Knowledge Base Updated! You can now ask questions.")

# 📂 Show Uploaded PDFs List
uploaded_files_list = os.listdir(DATA_PATH) if os.path.exists(DATA_PATH) else []
if uploaded_files_list:
    st.markdown("### 📂 Uploaded Documents:")
    for file_name in uploaded_files_list:
        st.markdown(f"- {file_name}")
else:
    st.info("No documents uploaded yet.")

st.divider()

# Load pipeline once (cached but will reload if FAISS DB is rebuilt)
@st.cache_resource(show_spinner="Warming up the brain... 🧠⚙️")
def load_pipeline():
    embedding_model = get_embedding_model()
    db = load_vector_db(DB_FAISS_PATH, embedding_model)
    llm = load_llm()
    qa_chain = setup_qa_chain(llm, db, set_custom_prompt(CUSTOM_PROMPT_TEMPLATE))
    return qa_chain

# Clear cache and reload pipeline if new PDFs uploaded
if uploaded_files:
    st.cache_resource.clear()
qa_chain = load_pipeline()

# Start chat session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input/output loop
st.chat_message("assistant").markdown("👋 Hello! I'm your AI assistant. Ask me anything about your uploaded documents.")

user_input = st.chat_input("Type your question here...")

if user_input:
    # Store user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🧠"):
            try:
                response = qa_chain.invoke({"query": user_input})
                answer = response['result']
                source_docs = response.get('source_documents', [])

                st.markdown(f"🤖 {answer}")

                if source_docs:
                    st.markdown("\ud83d\udd17 **Source Document(s):**")
                    for doc in source_docs:
                        source_name = doc.metadata.get("source", "Unknown Document")
                        st.markdown(f"- {source_name}")

                st.session_state.chat_history.append(("bot", answer))
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Optionally: show previous messages
if st.session_state.chat_history:
    st.divider()
    st.markdown("🕓 **Conversation History**", help="Scroll back through your past questions and answers.")
    for sender, msg in st.session_state.chat_history:
        icon = "🧠" if sender == "user" else "🤖"
        st.markdown(f"**{icon} {sender.capitalize()}**: {msg}")
