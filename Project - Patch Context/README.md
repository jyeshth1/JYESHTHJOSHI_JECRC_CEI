# 🚀 Patch_Context

## 📌 Overview

Patch Context is a Retrieval-Augmented Generation (RAG) application that enables users to ask natural language questions about the FastAPI GitHub repository. Instead of relying on general AI knowledge, the system retrieves relevant commits, pull requests, and issues from the repository and generates answers grounded in that information.

The project combines semantic search with Large Language Models (LLMs) to help developers understand repository history, design decisions, and implementation details.

---

## ✨ Features

- 🔍 Semantic search over GitHub repository data
- 📄 Retrieval of relevant commits, pull requests, and issues
- 🤖 AI-powered question answering using Groq Llama 3.1
- 📚 FAISS vector database for efficient similarity search
- 🧩 LangChain-based RAG pipeline
- 💻 Interactive Streamlit web interface
- 🔐 Secure API key management using environment variables

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- Sentence Transformers (BAAI/bge-small-en-v1.5)
- Groq API (Llama 3.1)
- GitHub API
- Python Dotenv

---

## 📂 Project Structure

```
Patch_Context/
│
├── app.py
├── config.py
├── ingest.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── commits.json
│   ├── prs.json
│   └── issues.json
│
├── src/
│   ├── __init__.py
│   ├── loader.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── retriever.py
│   ├── llm.py
│   ├── metadata.py
│   ├── prompt.py
│   └── utils.py
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/jyeshth1/JYESHTHJOSHI_JECRC_CEI.git
```

### Navigate to the project

```bash
cd Patch_Context
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GITHUB_TOKEN=your_github_token
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Running the Project

### Step 1: Collect repository data

```bash
python ingest.py
```

### Step 2: Create vector embeddings

```bash
python src/embedder.py
```

### Step 3: Launch the application

```bash
streamlit run app.py
```

---

## 💡 Sample Questions

- What is dependency injection in FastAPI?
- Which pull request introduced the QUERY HTTP method?
- What changes were made in the latest release notes?
- Explain Issue #15764.
- Summarize PR #15956.
- What recent commits modified translations?

---

## 🔄 RAG Pipeline

```
User Question
        │
        ▼
Retriever (FAISS)
        │
        ▼
Relevant Chunks
        │
        ▼
Groq Llama 3.1
        │
        ▼
Generated Answer
        │
        ▼
Source References
```

---

## 📈 Future Improvements

- Maximal Marginal Relevance (MMR) retrieval
- Clickable GitHub source links
- Chat history support
- Better prompt engineering
- Repository analytics dashboard
- Evaluation using RAGAs


## 📄 License

This project is developed for learning and educational purposes as part of the Celebal Technologies Internship Program.
