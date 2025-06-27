# 🌐 Universal Offline AI Chatbot

> Build your own domain-specific chatbot — offline, modular, and blazing fast.

The **Universal Offline AI Chatbot** is a privacy-respecting, offline-ready assistant that can chat over **any set of PDFs**. It’s ideal for legal, cybersecurity, academic, enterprise, or technical domains.

It uses a **locally hosted LLM** (`mistral:instruct` via [Ollama](https://ollama.com)) and **semantic search** powered by HuggingFace embeddings and FAISS. You get **fast, accurate responses**, without sending anything to the cloud.

---

## ✨ Highlights

* 🔐 Fully **offline-capable** with local LLM (via Ollama)
* 📄 Works out-of-the-box with your **PDFs**
* 🧠 **Semantic vector search** using `all-MiniLM-L6-v2`
* ⚡️ Fast and responsive using **FAISS** backend
* 🧩 Modular, extendable architecture (streamlit frontend + CLI)
* 🐳 Docker-ready for deployment

---

## 🧱 Tech Stack

| Layer        | Stack                                       |
| ------------ | ------------------------------------------- |
| LLM          | `mistral:instruct` via Ollama               |
| Embeddings   | `all-MiniLM-L6-v2` via SentenceTransformers |
| Vector Store | FAISS (in-memory + disk)                    |
| Framework    | LangChain (v0.2+)                           |
| Language     | Python 3.11+                                |
| UI           | Streamlit                                   |
| Container    | Docker                                      |

> ⚠️ HuggingFace Token is required to fetch the embedding model once. It's cached locally afterward.

---

## 💡 Use Cases

| Chatbot Type        | Add These PDFs                     |
| ------------------- | ---------------------------------- |
| 👨‍⚖️ LawyerBot     | Legal, Constitution, HR documents  |
| 🧬 ResearchBot      | Whitepapers, scientific papers     |
| 🛡️ CyberSecBot     | SOC2, GDPR, ISO27001, NIST docs    |
| 📚 EdTechBot        | Notes, textbooks, question banks   |
| 🧑‍💼 HR/CompanyBot | SOPs, onboarding docs, HR policies |

---

## 📁 Project Structure

```
Universal-Offline-AI-Chatbot/
│
├── data/                   # Place your PDF documents here
│   └── Try.pdf
│
├── Screenshots/           # UI snapshots
│   ├── Loading_Screen.png
│   └── Running_the_Model.png
│
├── src/                   # Modular source code
│   ├── chunker.py
│   ├── config.py
│   ├── embedding.py
│   ├── loader.py
│   ├── model_loader.py
│   ├── prompts.py
│   ├── qa_chain.py
│   ├── utils.py
│   └── vectorstore.py
│
├── vectorstore/           # Local FAISS vector index
│   └── db_faiss/
│
├── Bot.py                 # CLI script
├── Bot.ipynb              # Jupyter notebook version
├── main.py                # Entry-point (optional)
├── streamlit_app.py       # Frontend UI (Streamlit)
├── requirements.txt       # Python dependencies
├── setup.ps1              # PowerShell setup script
├── Dockerfile             # Docker image definition
├── .dockerignore
├── .env                   # Contains HF_TOKEN
├── README.md
└── LICENSE
```

---

## 🧰 Setup Instructions

### 🖥️ One-Click Setup (Windows Only)

```powershell
.\setup.ps1
```

This will:

* Create virtual env
* Install dependencies
* Pull Mistral via Ollama
* Ask for Hugging Face token
* Build Docker image

---

### 🛠 Manual Setup

1. **Install Python Requirements**

```bash
pip install -r requirements.txt
```

2. **Install & Pull Ollama Model**

```bash
ollama pull mistral:instruct
```

3. **Set HuggingFace Token (First Time Only)**

```bash
export HUGGINGFACEHUB_API_TOKEN=your_token      # macOS/Linux
set HUGGINGFACEHUB_API_TOKEN=your_token         # Windows CMD
```

4. **Run the CLI Bot**

```bash
python Bot.py
```

---

## 🌐 Run with Streamlit Frontend

```bash
streamlit run streamlit_app.py
```

### 📸 Streamlit Preview

#### ⏳ Loading Screen
![Loading Screen](./Screenshots/Loading_Screen.png)

#### 🤖 Chat in Action
![Running the Model](./Screenshots/Running_the_Model.png)

#### Features:

* Clean UI
* Type queries directly
* Works with your uploaded PDFs
* Handles PDF loading, chunking, indexing, and querying under the hood

---

## 🐳 Docker Support

### Prerequisites

* Docker installed & running

### Build & Run

```bash
# Build the image
docker build -t ai-chatbot .

# Run the container (ensure .env has HF_TOKEN)
docker run --env-file .env ai-chatbot
```

Example `.env`:

```
HF_TOKEN=your_huggingface_token_here
```

---

## 🔄 Using Your Own PDFs

```bash
# Replace default file(s)
mv your_files/*.pdf ./data/

# Re-run the bot or restart Streamlit
python Bot.py
```

Automatically re-indexes your new documents using FAISS.

---

## 🧪 Sample Interaction

```
🧠 You: What does Article 21 state?

🤖 Bot: Article 21 of the Indian Constitution guarantees the protection of life and personal liberty...
```

---

## 🧑‍💻 Author

**Aditya Bhatt** <br/>
Cybersecurity Specialist | VAPT Expert | OSS Contributor<br/>
[GitHub](https://github.com/AdityaBhatt3010) | [Medium](https://medium.com/@adityabhatt3010)<br/>

---
