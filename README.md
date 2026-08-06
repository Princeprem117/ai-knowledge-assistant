
# 🤖 AI Knowledge Assistant

> A modular AI chatbot built with Python and the Groq API. This project is being developed step by step to learn modern AI engineering practices and build a production-ready AI knowledge assistant.

---

## 📖 Overview

AI Knowledge Assistant is a Python-based AI chatbot that interacts with a Large Language Model (LLM) through the Groq API. The project focuses on clean architecture, modular design, and maintainability while gradually evolving into a complete AI-powered knowledge assistant.

The current version provides a terminal-based chatbot with persistent conversation history and a scalable project structure that supports future enhancements.

---

## ✨ Current Features

* 💬 Interactive terminal-based AI chatbot
* 🚀 Fast responses using the Groq API
* 🔐 Secure API key management with `.env`
* 📝 Persistent conversation history stored in JSON
* 📂 Automatic creation and management of chat history
* 🏗️ Modular project architecture
* 🧩 Base Loader architecture for scalable loader management
* 📦 Organized codebase for easier maintenance and future expansion
* ⚙️ Clean separation of responsibilities between project modules

---

## 🛠️ Tech Stack

| Category        | Technology    |
| --------------- | ------------- |
| Language        | Python        |
| AI Model        | Groq API      |
| Configuration   | python-dotenv |
| Data Storage    | JSON          |
| Version Control | Git & GitHub  |

---

## 📁 Project Structure

```text
AI-Knowledge-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── chat_history/
│
├── loaders/
│   ├── base_loader.py
│   └── ...
│
├── utils/
│
├── config/
│
└── ...
```

---

## ⚙️ Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-github-username>/AI-Knowledge-Assistant.git
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
pip install -r requirements.txt
```

### Configure the API Key

Create a `.env` file in the project root and add:

```env
GROQ_API_KEY=your_groq_api_key
```

### Run the Application

```bash
python app.py
```

---

## 📚 What I Learned

This project helped me gain practical experience in:

* Integrating Large Language Models using the Groq API
* Secure configuration management with environment variables
* Reading and writing JSON data
* Maintaining persistent chat history
* Designing modular Python applications
* Refactoring code for better maintainability
* Implementing a Base Loader architecture
* Organizing scalable project structures
* Using Git and GitHub for version control

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

# 👨‍💻 About the Author

**Prince**

Aspiring AI Engineer passionate about building real-world AI applications and mastering modern AI technologies through hands-on projects.

### Connect with Me

* GitHub: https://github.com/<your-github-username>
* LinkedIn: https://linkedin.com/in/<your-linkedin-username>

---

⭐ If you found this project useful or interesting, consider giving it a star on GitHub!
