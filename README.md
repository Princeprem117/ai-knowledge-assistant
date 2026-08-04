# 🤖 AI Knowledge Assistant

A terminal-based AI chatbot built with **Python** and the **Groq API**. This project marks the beginning of my journey into AI application development, with a focus on building practical, real-world AI systems from scratch.

---

## 📖 Overview

The AI Knowledge Assistant is a command-line chatbot that interacts with a Large Language Model (LLM) using the Groq API. It maintains conversation history, securely manages API keys, and demonstrates the core concepts of integrating AI models into Python applications.

---

## ✨ Features

* 💬 Interactive terminal-based AI chatbot
* 🚀 Fast AI responses powered by the Groq API
* 🔐 Secure API key management using `.env`
* 📝 Persistent conversation history stored in JSON
* 📂 Automatic creation of the chat history directory
* ⚙️ Clean and beginner-friendly project structure

---

## 🛠️ Tech Stack

* Python
* Groq API
* python-dotenv
* JSON
* Git
* GitHub

---

## 📁 Project Structure

```text
AI-Knowledge-Assistant/
│
├── First_Chatbot.py
├── Requirements.txt
├── README.md
├── .gitignore
├── .env
│
└── chat_history/
    └── conversation_history.json
```

---

## ⚙️ Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Knowledge-Assistant.git
```

### Navigate to the project

```bash
cd AI-Knowledge-Assistant
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r Requirements.txt
```

### Configure your API key

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_groq_api_key
```

### Run the chatbot

```bash
python First_Chatbot.py
```

---

## 📂 Conversation History

All conversations are saved locally in JSON format inside the `chat_history` folder, allowing previous interactions to be preserved between sessions.

---

## 📚 What I Learned

Through this project, I gained hands-on experience with:

* Integrating an LLM using the Groq Python SDK
* Managing API keys securely with `python-dotenv`
* Reading and writing JSON files
* Maintaining conversation history
* Structuring a Python project
* Using Git and GitHub for version control

---

## 🚀 Current Status

✅ Terminal AI Chatbot

✅ Groq API Integration

✅ Environment Variable Management

✅ Conversation History

✅ JSON Storage

✅ GitHub Repository

---

## 🚀 Future Development

The following features are planned for future versions of the AI Knowledge Assistant:

### Core Improvements
- Better prompt engineering
- Multiple chat sessions
- SQLite database for chat storage

### Knowledge Retrieval
- PDF document reader
- Text chunking
- Embeddings

###   RAG
- Retrieval-Augmented Generation (RAG)

###  Web Application
- FastAPI backend
- Streamlit frontend
- Chat history management
- File upload interface

###   Advanced AI
-  LangChain integration
-  LangGraph workflows
-  AI agents

###  Deployment
- Docker support
- Cloud deployment
---
## 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Prince Prem**


