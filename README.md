# 🤖 AI Knowledge Assistant

> A modular AI-powered knowledge assistant built with Python, evolving step by step from a basic AI chatbot toward a complete Retrieval-Augmented Generation (RAG) and agentic AI system.

---

## 📖 Overview

**AI Knowledge Assistant** is a Python-based project focused on learning and building modern AI applications from the ground up.

The project started as a terminal-based AI chatbot and is gradually evolving into a knowledge-based AI assistant.

The current implementation focuses on building the **document processing and embedding pipeline**, including document loaders, a common document model, recursive text chunking, and local vector embeddings.

The project is intentionally being developed incrementally to understand the underlying concepts and architecture rather than relying entirely on high-level frameworks.

---

## ✨ Current Features

### 🤖 AI Chatbot

* Interactive terminal-based AI chatbot
* Groq API integration
* Secure API key management using environment variables
* Conversation history
* JSON-based local chat storage

### 📄 Document Processing

* Modular document loader architecture
* Base loader interface
* Document loading
* Common `Document` data model
* Recursive text chunking using `RecursiveChunker`

### 🧠 Embeddings

* Local Sentence Transformer embedding model
* Converts document chunks into numerical vector representations
* Local embedding generation without depending on an external embedding API

### 🏗️ Project Architecture

* Modular Python project structure
* Separation of responsibilities between components
* Reusable base classes and interfaces
* Component-level testing during development
* Architecture designed to support future semantic search and RAG functionality

---

## 🛠️ Tech Stack

| Category             | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| LLM API              | Groq                  |
| Embeddings           | Sentence Transformers |
| Configuration        | python-dotenv         |
| Data Storage         | JSON                  |
| Version Control      | Git & GitHub          |

---

## 📁 Project Structure

```text
AI-Knowledge-Assistant/
│
├── loaders/
│   ├── base_loader.py
│   └── ...
│
├── models/
│   └── document.py
│
├── chunking/
│   └── recursive_chunker.py
│
├── embeddings/
│   └── ...
│
├── tests/
│   └── ...
│
├── data/
│   └── ...
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> The project structure is evolving as new components are implemented.

---

## 🔄 Current Processing Pipeline

The current document-processing pipeline works through the following stages:

```text
Documents
    │
    ▼
Document Loaders
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
```

The next stage is to store and retrieve these embeddings using a **Vector Database**.

---

## 🚧 Current Development

### 🗄️ Vector Database — In Progress

The project is currently implementing the **Vector Database layer**.

The planned implementation uses **ChromaDB** for:

* Storing document embeddings
* Storing document metadata
* Performing similarity search
* Retrieving relevant document chunks

The Vector Database layer is **not yet fully implemented** and therefore is not listed as a completed feature.

Current development includes designing a reusable vector-store abstraction that can later support ChromaDB.

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

### 7. Run the project

Run the appropriate application or test module according to the current project structure.

---

## 🧪 Testing

The project includes tests for validating individual components during development.

Current testing focuses on components such as:

* Document loaders
* Document model
* Text chunking
* Embedding generation

Example:

```bash
python -m tests.test_embedding
```

---

## 📚 What I Have Learned

Through this project, I have gained practical experience with:

* Integrating LLMs using APIs
* Managing API keys securely
* Using environment variables
* Reading and writing JSON data
* Designing modular Python applications
* Creating reusable loader interfaces
* Designing a common document representation
* Understanding document chunking
* Implementing recursive text splitting
* Generating local vector embeddings
* Understanding how embeddings represent semantic information
* Structuring components for future vector database integration
* Testing individual components during development
* Using Git and GitHub for version control

---

## 🚀 Future Development

The project will continue evolving toward a complete AI Knowledge Assistant.

### 🗄️ Vector Database

* [ ] Complete ChromaDB integration
* [ ] Store document embeddings
* [ ] Store document metadata
* [ ] Implement similarity search
* [ ] Implement metadata filtering

### 🔎 Semantic Search

* [ ] Retrieve relevant document chunks
* [ ] Improve retrieval quality
* [ ] Evaluate search results

### 🧠 Retrieval-Augmented Generation

* [ ] Build the complete RAG pipeline
* [ ] Connect retrieval with the LLM
* [ ] Generate answers from retrieved knowledge
* [ ] Add source references and citations
* [ ] Improve retrieval and generation quality

### 💬 Assistant Features

* [ ] Multiple conversation sessions
* [ ] Persistent session management
* [ ] Improved conversation memory
* [ ] Context-aware responses

### ⚡ Modern AI Technologies

* [ ] LangChain integration where appropriate
* [ ] LangGraph workflows
* [ ] Tool calling
* [ ] AI agents
* [ ] Multi-agent workflows

### 🌐 Application & Deployment

* [ ] FastAPI backend
* [ ] Web interface
* [ ] File upload functionality
* [ ] Docker support
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
├── ✅ Modular Loader Architecture
├── ✅ Document Model
├── ✅ Document Loaders
├── ✅ Recursive Chunking
├── ✅ Sentence Transformer Embeddings
│
├── 🔄 Vector Database / ChromaDB
│
├── ⏳ Semantic Search
├── ⏳ RAG Pipeline
├── ⏳ Source Citations
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
