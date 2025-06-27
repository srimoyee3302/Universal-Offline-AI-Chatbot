# 🧠 Universal Offline AI Chatbot

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/release/python-3110/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/github/license/AdityaBhatt3010/Universal-Offline-AI-Chatbot)](./LICENSE)
[![CI](https://github.com/AdityaBhatt3010/Universal-Offline-AI-Chatbot/actions/workflows/python-ci.yml/badge.svg)](https://github.com/AdityaBhatt3010/Universal-Offline-AI-Chatbot/actions/workflows/python-ci.yml)

> Build your own domain-specific chatbot — offline-capable, fast, and privacy-aware.

**Universal Offline AI Chatbot** is a lightweight, extensible local assistant that answers questions based on your **own PDFs** — legal, technical, scientific, educational, or enterprise documents. It uses a fast, locally hosted LLM via **Ollama**, and processes your files using **semantic search** to provide meaningful answers.

---

## ✨ Highlights

- Universal PDF support — just drop in any document
- Entirely offline with `Ollama` + `FAISS`
- HuggingFace embeddings (`all-MiniLM-L6-v2`)
- Streamlit + CLI Interface
- Docker-ready for portability

---

## 🧱 Tech Stack

| Layer         | Stack                                       |
| ------------- | ------------------------------------------- |
| LLM           | `mistral:instruct` via Ollama               |
| Embeddings    | `all-MiniLM-L6-v2` via SentenceTransformers |
| Vector Store  | FAISS (fast, local)                         |
| Framework     | LangChain                                   |
| Interface     | CLI + Streamlit                             |
| Language      | Python 3.11+                                |

---

## 📂 Project Structure

```
Universal-Offline-AI-Chatbot/
│
├── data/                     # Your PDF files here
├── vectorstore/             # FAISS DB
├── src/                     # Modular pipeline code
├── streamlit_app.py         # Streamlit frontend
├── Bot.py / Bot.ipynb       # CLI and Notebook versions
├── setup.ps1                # PowerShell auto-setup script
├── Dockerfile               # Docker support
├── .env / .dockerignore     # Environment config
└── README.md
```

---

## ⚙️ Setup Instructions

### ✅ One-Click Setup (Windows)
```powershell
./setup.ps1
```

This installs dependencies, activates venv, pulls Ollama model, and runs the chatbot.

### 🐧 Manual Setup (Linux/macOS)
```bash
pip install -r requirements.txt
ollama pull mistral:instruct
export HUGGINGFACEHUB_API_TOKEN=your_token_here
python Bot.py
```

---

## 🚀 Run Options

### CLI Version
```bash
python Bot.py
```

### Notebook Version
```bash
jupyter notebook Bot.ipynb
```

### Streamlit Version
```bash
streamlit run streamlit_app.py
```

### 📸 Streamlit Preview

#### ⏳ Loading Screen
![Loading Screen](./Screenshots/Loading_Screen.png)

#### 🤖 Chat in Action
![Running the Model](./Screenshots/Running_the_Model.png)

---

## 🐋 Docker Support

```bash
docker build -t ai-chatbot .
docker run --env-file .env ai-chatbot
```

> `.env` must contain:
```
HF_TOKEN=your_token_here
```

---

## 🧠 Sample Chat
```
🧠 You: What is Article 21?
🤖 Bot: Article 21 ensures the protection of life and personal liberty...
```

---

## 🛠️ Customize with Your Data

Just replace contents of `/data/` with your PDFs:
```bash
rm data/*
cp my_docs/*.pdf data/
python Bot.py
```

---

## 🧪 CI/CD Pipeline (GitHub Actions)

A `python-ci.yml` workflow is included:
```
.github/workflows/python-ci.yml
```
It:
- Installs Python + requirements
- Runs `flake8` linting
- Can be extended for testing or Docker builds

---

## 🧑‍💻 Author

**Aditya Bhatt**  
Cybersecurity Specialist • AI + VAPT • OSS Contributor  
[GitHub](https://github.com/AdityaBhatt3010) • [Medium](https://medium.com/@adityabhatt3010)

---