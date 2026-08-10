# 🤖 AI Knowledge Assistant

> A modular AI-powered knowledge assistant built from scratch with Python, evolving from a basic LLM chatbot into a Retrieval-Augmented Generation (RAG) application.

---

## 📖 Overview

**AI Knowledge Assistant** is a Python-based AI application designed to answer questions using information from a custom knowledge base.

The project started as a simple terminal-based chatbot and has progressively evolved into a **basic end-to-end RAG application**.

The current system can process knowledge documents, split them into chunks, generate vector embeddings, store them in a vector database, retrieve relevant information, and use the retrieved context to generate responses with an LLM.

The project is being developed incrementally to understand the underlying concepts and architecture behind modern AI applications.

---

## ✨ Current Features

### 🤖 AI Chatbot

* Interactive terminal-based chatbot
* Groq API integration
* Configurable LLM parameters
* Secure API key management using environment variables
* Conversation history
* JSON-based conversation storage
* Chat commands and conversation management

### 📄 Document Processing

* Modular document loader architecture
* Base loader abstraction
* Text document loading
* Common `Document` data model
* Metadata support
* Recursive text chunking
* Configurable chunk size and chunk overlap

### 🧠 Embeddings

* Local Sentence Transformer embedding model
* Converts document chunks into vector representations
* Query embedding generation
* Local embedding generation without requiring an external embedding API

### 🗄️ Vector Database

* ChromaDB integration
* Persistent vector storage
* Document and embedding storage
* Metadata storage
* Similarity search
* Document deletion
* Vector-store abstraction for maintainability

### 🔎 Retrieval

* Query-to-vector conversion
* Similarity-based document retrieval
* Top-K relevant chunk retrieval
* Retrieved context prepared for LLM generation

### 🧠 RAG

* Basic end-to-end Retrieval-Augmented Generation pipeline
* Knowledge-base initialization
* Document processing and indexing
* Query embedding
* Relevant context retrieval
* Context-aware LLM generation

---

## 🔄 RAG Pipeline

The current application follows this general flow:

```text
                    KNOWLEDGE INGESTION
                           │
                           ▼
                      Documents
                           │
                           ▼
                    Document Loader
                           │
                           ▼
                    Document Model
                           │
                           ▼
                   Recursive Chunker
                           │
                           ▼
                Sentence Transformer
                           │
                           ▼
                    Vector Embeddings
                           │
                           ▼
                       ChromaDB
                           │
                           │
                           ▼
                    VECTOR DATABASE
                           │
                           │
                    USER QUESTION
                           │
                           ▼
                Query Embedding
                           │
                           ▼
                    ChromaDB Search
                           │
                           ▼
                 Relevant Documents
                           │
                           ▼
                  Retrieved Context
                           │
                           ▼
                       Groq LLM
                           │
                           ▼
                    Final Response
```

This represents the basic RAG architecture currently implemented in the project.

---

## 🏗️ Architecture

The project follows a modular architecture instead of putting the complete application logic into a single file.

```text
AI Knowledge Assistant
│
├── Chat Layer
│   ├── ChatBot
│   ├── Commands
│   └── Prompts
│
├── LLM Layer
│   └── Groq Client
│
├── Document Layer
│   ├── Document Model
│   └── Loaders
│
├── Chunking Layer
│   ├── Base Chunker
│   └── Recursive Chunker
│
├── Embedding Layer
│   └── Sentence Transformer
│
├── Vector Database Layer
│   ├── Base Vector Store
│   └── ChromaDB
│
├── Knowledge Base
│   └── RAG Pipeline
│
├── Storage
│   └── Conversation History
│
└── Tests
```

---

## 🛠️ Tech Stack

| Category        | Technology            |
| --------------- | --------------------- |
| Language        | Python                |
| LLM             | Groq                  |
| Embeddings      | Sentence Transformers |
| Vector Database | ChromaDB              |
| Configuration   | python-dotenv         |
| Data Storage    | JSON                  |
| Testing         | Python testing tools  |
| Version Control | Git & GitHub          |

---

## 📁 Project Structure

```text
AI-Knowledge-Assistant/
│
├── app/
│   └── ...
│
├── chat/
│   ├── chatbot.py
│   ├── commands.py
│   └── prompts.py
│
├── llms/
│   └── groq_client.py
│
├── loaders/
│   ├── base_loader.py
│   └── text_loader.py
│
├── models/
│   └── document.py
│
├── chunkers/
│   ├── base_chunker.py
│   └── recursive_chunker.py
│
├── embeddings/
│   └── ...
│
├── vectordb/
│   ├── base_vector_store.py
│   └── chroma_db.py
│
├── tests/
│   └── ...
│
├── data/
│   └── ...
│
├── config.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> The structure may continue to evolve as new capabilities are added.

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-github-username>/AI-Knowledge-Assistant.git
```

### 2. Navigate to the project

```bash
cd AI-Knowledge-Assistant
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

### 7. Run the application

```bash
python -m app.app
```

---

## 🧪 Testing

The project contains component-level tests for validating individual parts of the system.

Current tests cover areas including:

* Document processing
* Chunking
* Embeddings
* ChromaDB vector storage
* Vector similarity search
* Vector deletion

For example:

```bash
python -m tests.test_embedding
```

---

## 📚 What I Have Learned

Through this project, I have gained hands-on experience with:

* Integrating Large Language Models
* Working with the Groq API
* Secure environment configuration
* Conversation management
* JSON persistence
* Modular Python architecture
* Abstract base classes and interfaces
* Document loading
* Document metadata
* Text chunking
* Recursive chunking
* Vector embeddings
* Sentence Transformers
* Vector databases
* ChromaDB
* Similarity search
* Knowledge-base construction
* Retrieval-Augmented Generation
* Connecting retrieved context with an LLM
* Component-level testing
* Git and GitHub

---

## 🚀 Future Development

The current implementation is a **basic RAG application**. The project will continue to evolve toward a more capable AI Knowledge Assistant.

### 📄 Knowledge Ingestion

* [ ] Support additional document formats
* [ ] PDF loading
* [ ] DOCX loading
* [ ] Improved metadata handling
* [ ] Better document preprocessing

### 🔎 Advanced Retrieval

* [ ] Improved retrieval strategies
* [ ] Metadata filtering
* [ ] Hybrid search
* [ ] Reranking
* [ ] Retrieval evaluation

### 🧠 Advanced RAG

* [ ] Improved prompt engineering
* [ ] Source citations
* [ ] Context compression
* [ ] Query transformation
* [ ] Conversational RAG
* [ ] RAG evaluation

### ⚡ Modern AI Frameworks

* [ ] LangChain integration where appropriate
* [ ] LangGraph workflows
* [ ] Tool calling
* [ ] AI agents
* [ ] Multi-agent workflows

### 💬 Application Improvements

* [ ] Multiple chat sessions
* [ ] Better conversation memory
* [ ] User/session management
* [ ] File upload interface

### 🌐 Deployment

* [ ] FastAPI backend
* [ ] Web interface
* [ ] Docker
* [ ] Cloud deployment
* [ ] CI/CD
* [ ] Monitoring and logging

---

## 🗺️ Development Progress

```text
AI Knowledge Assistant
│
├── ✅ Basic AI Chatbot
├── ✅ Groq API Integration
├── ✅ Environment Configuration
├── ✅ Conversation History
├── ✅ JSON Storage
│
├── ✅ Modular Architecture
├── ✅ Base Loader
├── ✅ Document Model
├── ✅ Text Loader
├── ✅ Recursive Chunking
├── ✅ Sentence Transformer Embeddings
│
├── ✅ ChromaDB Vector Store
├── ✅ Vector Similarity Search
├── ✅ Vector Store Tests
│
├── ✅ Basic End-to-End RAG
│
├── ⏳ Advanced Retrieval
├── ⏳ RAG Evaluation
├── ⏳ Source Citations
├── ⏳ Conversational RAG
├── ⏳ LangChain
├── ⏳ LangGraph
├── ⏳ AI Agents
├── ⏳ FastAPI
└── ⏳ Deployment
```

### Status Legend

* ✅ **Completed**
* 🔄 **In Progress**
* ⏳ **Planned**

---

## 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 About the Author

## Prince Prem

Aspiring **AI Engineer** focused on building practical AI systems and learning modern AI technologies through hands-on development.

This project represents my journey from building basic LLM applications toward developing advanced systems involving **embeddings, vector databases, RAG, LangChain, LangGraph, and AI agents**.

---
