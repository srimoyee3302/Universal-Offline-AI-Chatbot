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
st.set_page_config(page_title="Universal AI Chatbot", page_icon="\U0001F9E0", layout="centered")

# Header
stylish_heading()
st.markdown("<h2 style='text-align: center;'>\U0001F9E0 Ask Me Anything From Your PDFs</h2>", unsafe_allow_html=True)
st.markdown("✅ Powered by **Offline Mistral** + **FAISS**. Upload `.pdf` files below to update knowledge base automatically.")

st.divider()

# PDF Upload Section
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

# Show Uploaded PDFs List with Remove Option
uploaded_files_list = os.listdir(DATA_PATH) if os.path.exists(DATA_PATH) else []
if uploaded_files_list:
    st.markdown("### 📂 Uploaded Documents:")
    for file_name in uploaded_files_list:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown(f"- {file_name}")
        with col2:
            if st.button("Remove", key=f"remove_{file_name}"):
                os.remove(os.path.join(DATA_PATH, file_name))
                st.success(f"Removed {file_name}. Please upload new files or refresh the app.")
                st.experimental_rerun()
else:
    st.info("No documents uploaded yet.")

# Load pipeline once (cached but will reload if FAISS DB is rebuilt)
@st.cache_resource(show_spinner="Warming up the brain... \U0001F9E0⚙️")
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
llm_model = load_llm()

# Start chat session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input/output loop
st.chat_message("assistant").markdown(f"{chr(0x1F44B)} Hello! I'm your AI assistant. Ask me anything about your uploaded documents.")

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... \U0001F9E0"):
            try:
                retriever = qa_chain.retriever
                docs_with_scores = retriever.vectorstore.similarity_search_with_score(user_input, k=3)

                SIMILARITY_THRESHOLD = 0.6
                filtered_docs = []

                for doc, score in docs_with_scores:
                    if score >= SIMILARITY_THRESHOLD:
                        filtered_docs.append(doc)

                if not filtered_docs:
                    st.warning("I couldn't find relevant information in the uploaded documents for your query.")
                else:
                    context = "\n\n".join([getattr(doc, 'page_content', str(doc)) for doc in filtered_docs])

                    prompt = f"Use the following context to answer:\n{context}\n\nQ: {user_input}\nA:"

                    answer_response = llm_model(prompt)
                    if isinstance(answer_response, str):
                        answer = answer_response.strip()
                    else:
                        answer = answer_response.get('response', '').strip()

                    st.markdown(f"{chr(0x1F916)} {answer}")

                    st.markdown(f"{chr(0x1F517)} **Source Document(s):**")
                    for doc in filtered_docs:
                        source_name = doc.metadata.get("source", "Unknown Document")
                        st.markdown(f"- {source_name}")

                    st.session_state.chat_history.append(("bot", answer))

            except Exception as e:
                st.error(f"{chr(0x274C)} Error: {e}")

# Toggle to Show/Hide Conversation History
if st.session_state.chat_history:
    st.divider()
    show_history = st.toggle("Show Conversation History", value=False)
    if show_history:
        st.markdown(f"{chr(0x1F553)} **Conversation History**", help="Scroll back through your past questions and answers.")
        for sender, msg in st.session_state.chat_history:
            icon = chr(0x1F9E0) if sender == "user" else chr(0x1F916)
            st.markdown(f"**{icon} {sender.capitalize()}**: {msg}")