# 🌐 Universal Offline AI Chatbot

> 🧠 Build your own domain-specific chatbot — offline-capable, flexible, and privacy-aware.

**Universal Offline AI Chatbot** is a lightweight, extensible local assistant that answers questions based on your **own PDFs** — legal, technical, scientific, educational, or enterprise documents. It uses a fast, locally hosted LLM via **Ollama**, and processes your files using **semantic search** to provide meaningful answers.

Although the example setup features a **LawyerBot** trained on human rights and constitutional documents, you can easily replace the PDFs to create your **own chatbot in any domain** — all without relying on cloud-based inference.

---

## ✨ Highlights

* 🌍 **Universal Domain Support** — just drop in any PDFs
* 🔐 **Offline-Capable** — inference is local via Ollama
* 🧠 **Semantic Search** with HuggingFace embeddings
* 📄 **PDF-first** design — no need for manual data entry
* 🧪 Comes preconfigured with a working **LawyerBot**

---

## 🧱 Tech Stack

| Layer         | Stack                                       |
| ------------- | ------------------------------------------- |
| LLM           | `mistral:instruct` (served via Ollama)      |
| Embeddings    | `all-MiniLM-L6-v2` via SentenceTransformers |
| Vector Store  | FAISS (fast, local)                         |
| RAG Framework | LangChain                                   |
| Language      | Python 3.11+                                |

> **Note:** This setup uses HuggingFace’s `sentence-transformers/all-MiniLM-L6-v2`, which still requires a HuggingFace token to fetch the model the first time. After that, it's cached and used locally.

---

## 🤔 Can it be 100% Offline?

Yes — but with tradeoffs.

To make this chatbot **completely offline**, including embeddings:

* You’d need to **host your own embedding model** (like `MiniLM`, `Instructor-XL`, etc.) using ONNX or quantized PyTorch
* This requires significant **RAM/VRAM**, slow initial load times, and custom wrappers
* You’ll lose the simplicity and efficiency provided by `sentence-transformers`

**This repo uses the HuggingFace version to balance practicality and performance.**

---

## 💡 Use Cases

| Use Case                 | Just Add These PDFs             |
| ------------------------ | ------------------------------- |
| 👨‍⚖️ LawyerBot          | Legal/Constitutional Docs       |
| 🧑‍🏫 EdTechBot          | Academic Notes, Books           |
| 🛡️ CyberSecBot          | SOC2, GDPR, ISO27001 PDFs       |
| 🧬 ResearchBot           | Scientific Papers, Whitepapers  |
| 🧑‍💼 HRBot / CompanyBot | Onboarding Docs, Policies, SOPs |

---

## 📂 Folder Structure

```

📁 data/                  ← Drop your PDFs here
├── Universal\_Human\_Rights.pdf
├── Constitution\_of\_India.pdf

🧠 Bot.py                ← Main CLI chatbot script
📓 Bot.ipynb             ← Jupyter Notebook with sample output
📁 vectorstore/db\_faiss/ ← FAISS-generated local vector DB
🔧 requirements.txt
🔧 setup.ps1             ← PowerShell script for setup (Windows)
📄 README.md

````

---

## 📦 Clone the Repository

```bash
git clone https://github.com/AdityaBhatt3010/Universal-Offline-AI-Chatbot.git
cd Universal-Offline-AI-Chatbot
````

---

## ⚙️ Setup Instructions

### 1. Use the One-Click PowerShell Script (Windows)

```powershell
.\setup.ps1
```

This installs Python dependencies, sets up the environment, and pulls the Ollama model.

### OR follow the manual steps:

#### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Pull the Ollama Model

```bash
ollama pull mistral:instruct
```

Make sure `ollama` is installed and running.

#### 3. Set Your HF Token (first-time only)

```bash
export HUGGINGFACEHUB_API_TOKEN=your_token_here      # macOS/Linux
set HUGGINGFACEHUB_API_TOKEN=your_token_here         # Windows CMD
```

---

## 🚀 Running the Chatbot

```bash
python Bot.py
```

or try the notebook version:

```bash
jupyter notebook Bot.ipynb
```

---

## 💬 Sample Interaction

```
🧠 You: What is Article 19 about?

🤖 Bot: Article 19 states that everyone has the right to freedom of opinion and expression...
```

---

## 🛠️ Customize the Knowledge Base

To use your own data:

```bash
# Replace files in data/
rm data/*
mv your_pdfs/*.pdf data/

# Re-run the bot
python Bot.py
```

The bot will automatically embed and index your custom data using FAISS.

---

## 🧑‍💻 Author

**Aditya Bhatt** <br/>
Cybersecurity Specialist • AI + VAPT • OSS Contributor <br/>
[GitHub](https://github.com/AdityaBhatt3010) • [Medium](https://medium.com/@adityabhatt3010) <br/>

---
