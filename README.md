# 🤖 LearnBot --- AI Knowledge Assistant

> A modular AI Knowledge Assistant that turns user-provided documents
> into a searchable knowledge base and uses Retrieval-Augmented
> Generation (RAG) to produce grounded answers.

## 📖 Overview

**LearnBot** is a Python-based AI Knowledge Assistant built as a
practical learning project for modern RAG and AI application
engineering.

The project has progressed from a basic LLM application to a **basic
end-to-end RAG system** with document ingestion, embeddings, ChromaDB
retrieval, relevance filtering, source-aware responses, and a
user-facing interface.

The current development is moving toward a **multi-user RAG
architecture**, where document ingestion and retrieval are associated
with a `user_id`. The project is also being evolved toward persistent
document metadata and a more production-oriented document lifecycle.

The application currently focuses on:

-   User-specific document ingestion.
-   PDF, DOCX, TXT, and Markdown document support.
-   Text chunking with overlap.
-   Sentence Transformer embeddings.
-   ChromaDB vector storage and similarity retrieval.
-   Retrieval distance/relevance filtering.
-   Strict RAG generation from retrieved document context.
-   Source information in generated answers.
-   Document deletion and vector cleanup.
-   Conversation management.
-   User-specific retrieval and ingestion boundaries.
-   Chainlit UI from the earlier application stage, with the project
    now evolving toward a multi-user application architecture.

------------------------------------------------------------------------

## ✨ Key Features

### 📚 Document Knowledge Base

Supported document formats include:

-   PDF
-   DOCX
-   TXT
-   Markdown

Documents are loaded, processed, chunked, embedded, and stored in the
vector database.

### 🧩 Document Chunking

The current chunking configuration uses:

-   **Chunk size:** 500 characters
-   **Chunk overlap:** 60 characters

The current chunker uses fixed character windows with overlap. Chunking
quality is being evaluated as part of the retrieval-quality stage.

### 🧠 Embeddings

Document chunks and user queries are converted into vector embeddings
using:

**`sentence-transformers/all-MiniLM-L6-v2`**

The current embedding model is kept as a baseline while retrieval
quality is being evaluated.

### 🗄️ ChromaDB Vector Store

ChromaDB is used as the vector retrieval layer.

The ingestion pipeline creates:

-   deterministic document identities
-   deterministic chunk IDs
-   embeddings
-   metadata
-   user ownership information

This allows repeated ingestion of the same content for the same user to
use stable vector identities.

### 👤 Multi-User RAG Foundation

The current RAG services accept a `user_id` during document ingestion
and question answering.

The ingestion pipeline associates chunks with:

-   `user_id`
-   `document_id`
-   `filename`
-   `source`

This provides the foundation for keeping each user's knowledge base
separate.

### 🔎 Semantic Retrieval

The retrieval flow is:

``` text
User Query
    ↓
Query Embedding
    ↓
ChromaDB Similarity Search
    ↓
Top-K Candidates
    ↓
Distance / Relevance Filtering
    ↓
Relevant Context
```

The current default retrieval configuration uses:

``` text
Top-K: 3
```

### 🎯 Relevance Filtering

Retrieved results are evaluated using a configurable relevance
threshold.

The current baseline is:

``` text
RAG_RELEVANCE_THRESHOLD = 1.5
```

The threshold is being evaluated using real retrieval examples rather
than being changed arbitrarily.

### 🛡️ Strict RAG Generation

The current RAG pipeline is intentionally **strict**.

The LLM is instructed to:

1.  Use only the supplied document context.
2.  Avoid general knowledge.
3.  Avoid guessing or inventing information.
4.  State when the required information is not available in the provided
    documents.
5.  Only attribute information to documents when the context supports
    it.

If no relevant document context passes the current relevance check, the
system returns:

> I couldn't find information about this in the provided documents.

This keeps the current application focused on **grounded document-based
answers**.

### 📑 Source-Aware Responses

When relevant documents are used, the response can include source
filenames and their best retrieval distances.

Example:

``` text
Sources:

[1] IntelligentAgents_info.pdf
```

### 🧹 Document Deletion

Document deletion removes the document's associated vector data from the
knowledge base and removes the uploaded file from local storage.

This has been tested as part of the current document lifecycle.

### 💬 Conversation Management

The application supports conversation-oriented interaction, including:

-   Starting conversations.
-   Continuing conversations.
-   Viewing saved conversations.
-   Opening previous chats.
-   Deleting conversations.

------------------------------------------------------------------------

## 🔄 RAG Pipeline

The current RAG flow is:

``` text
                 DOCUMENT INGESTION
                         │
                         ▼
                  Document Loader
                         │
                         ▼
                    Document
                         │
                         ▼
                  Text Chunking
                         │
                         ▼
              Sentence Transformer
                         │
                         ▼
                    Embeddings
                         │
                         ▼
                     ChromaDB
                         │
                         │
                   User Knowledge
                         │
                         ▼
                      User Query
                         │
                         ▼
                   Query Embedding
                         │
                         ▼
                  Similarity Search
                         │
                         ▼
                 Top-K Candidates
                         │
                         ▼
                Relevance Filtering
                         │
              ┌──────────┴──────────┐
              │                     │
         Relevant Context      No Relevant Context
              │                     │
              ▼                     ▼
        Context Builder       Grounded fallback
              │               message returned
              ▼
              LLM
              │
              ▼
       Grounded Answer
              │
              ▼
        Source Information
```

------------------------------------------------------------------------

## 👤 Multi-User RAG Flow

The current ingestion and query services pass a `user_id` through the
RAG stack.

``` text
                    Authenticated User
                           │
                           ▼
                        user_id
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
        Document Upload             User Question
             │                           │
             ▼                           ▼
      Ingestion Service              RAG Service
             │                           │
             ▼                           ▼
     Ingestion Pipeline            RAG Pipeline
             │                           │
             ▼                           ▼
       user_id metadata          user_id-aware retrieval
             │                           │
             └─────────────┬─────────────┘
                           ▼
                       ChromaDB
```

The goal is to ensure that retrieval is scoped to the appropriate user's
knowledge rather than treating the vector database as one global
knowledge base.

------------------------------------------------------------------------

## 🏗️ High-Level Architecture

``` text
AI Knowledge Assistant
│
├── UI / Application Layer
│   └── Chainlit (current development direction)
│
├── Application Services
│   ├── RAGService
│   ├── DocumentIngestionService
│   └── Document lifecycle services (in progress)
│
├── RAG
│   ├── RAGPipeline
│   ├── Retriever
│   └── ContextBuilder
│
├── Document Processing
│   ├── LoaderFactory
│   ├── PDF Loader
│   ├── DOCX Loader
│   ├── Markdown Loader
│   ├── Text Loader
│   └── Chunking
│
├── Embeddings
│   └── Sentence Transformers
│
├── Vector Store
│   └── ChromaDB
│
├── LLM
│   └── Groq / configured LLM provider
│
├── Persistence
│   ├── Local uploaded files
│   └── PostgreSQL/Supabase document metadata (development in progress)
│
└── Tests
    ├── Unit tests
    └── Integration / RAG tests
```

------------------------------------------------------------------------

## 🛠️ Tech Stack

  Area              Technology
  ----------------- ----------------------------------------------------------------
  Language          Python
  LLM               Groq / configured LLM provider
  Embeddings        Sentence Transformers
  Embedding Model   `all-MiniLM-L6-v2`
  Vector Database   ChromaDB
  RAG               Custom modular RAG pipeline
  UI                Chainlit (current development direction)
  Database          PostgreSQL / Supabase (document lifecycle in progress)
  Configuration     `python-dotenv`
  Testing           Pytest
  Version Control   Git / GitHub

------------------------------------------------------------------------

## 📁 Project Structure

The exact project structure continues to evolve as the application moves
toward a multi-user architecture.

``` text
AI-Knowledge-Assistant/
│
├── app/
│
├── chat/
│
├── loaders/
│   ├── loader_factory.py
│   └── ...
│
├── models/
│
├── chunkers/
│
├── embeddings/
│
├── vectordb/
│   ├── base_db.py
│   └── chroma_db.py
│
├── retrieval/
│   ├── retriever.py
│   └── context_builder.py
│
├── rag/
│   └── pipeline.py
│
├── ingestion/
│   ├── pipeline.py
│   └── service.py
│
├── services/
│   └── ...
│
├── repositories/
│   └── ...
│
├── ui/
│   └── ...
│
├── tests/
│
├── data/
│   └── uploads/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

## ⚙️ Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/<your-github-username>/AI-Knowledge-Assistant.git
cd AI-Knowledge-Assistant
```

### 2. Create a virtual environment

``` bash
python -m venv .venv
```

Windows:

``` powershell
.venv\Scripts\activate
```

Linux/macOS:

``` bash
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

For example:

``` env
GROQ_API_KEY=your_groq_api_key
```

Add the database/environment variables required by the current
application configuration when using the multi-user persistence layer.

**Never commit API keys, database credentials, or `.env` files to
GitHub.**

### 5. Run the application

Use the entry point defined by the current project version.


For the current Chainlit development version:

``` bash
chainlit run <chainlit_entry_file>.py
```

------------------------------------------------------------------------

## 🧪 Testing and Verification

The project follows a deliberate development cycle:

``` text
Implement
    ↓
Test
    ↓
Verify
    ↓
Fix
    ↓
Measure
    ↓
Continue
```

The project has been tested across areas such as:

-   Document loaders
-   Document ingestion
-   Embedding generation
-   ChromaDB operations
-   Retrieval
-   Distance filtering
-   Context construction
-   RAG pipeline
-   LLM integration
-   Document deletion
-   User-specific ingestion/retrieval behavior

### Current verified baseline

The latest established baseline included:

``` text
30 tests passed
1 dependency warning
```

The warning came from a ChromaDB/OpenTelemetry dependency and did not
cause a project test failure.

The test suite is used as a safety net before making retrieval or
architecture changes.

------------------------------------------------------------------------

## 📊 Current Project Status

### ✅ Completed / Verified

-   Basic LLM integration
-   Document loading
-   PDF/DOCX/TXT/Markdown support
-   Text chunking
-   Sentence Transformer embeddings
-   ChromaDB vector storage
-   Semantic retrieval
-   Top-K retrieval
-   Distance-based relevance filtering
-   Context construction
-   Strict RAG generation
-   Source-aware responses
-   Document deletion and vector cleanup
-   Basic conversation management
-   Modular RAG services
-   User ID propagation through ingestion and RAG services
-   Deterministic document and chunk identities for user-scoped
    ingestion
-   Test-driven verification of core components

### 🔄 Current Development

The project is currently evolving from the basic RAG application toward
a **multi-user, production-oriented RAG architecture**.

Current areas include:

-   User-scoped knowledge bases
-   User-aware retrieval
-   Persistent document metadata
-   Document lifecycle management
-   Duplicate document detection
-   Processing status tracking
-   PostgreSQL/Supabase integration
-   Application/service/repository separation
-   Chainlit-based application development
-   Retrieval-quality evaluation
-   Better reliability and error handling

Some of these production-oriented components are **in progress and
should not yet be considered fully completed**.

### ⏳ Planned

-   Complete document lifecycle synchronization
-   PostgreSQL/ChromaDB consistency handling
-   Safer document replacement/versioning
-   Better retrieval evaluation
-   Chunking experiments
-   Threshold tuning based on measured data
-   Top-K evaluation
-   Advanced retrieval strategies
-   Reranking
-   Hybrid search
-   Query transformation
-   Improved observability and logging
-   Production API architecture
-   Authentication/authorization hardening
-   Cloud object storage
-   Deployment
-   Monitoring

------------------------------------------------------------------------

## 🧭 Development Roadmap

``` text
✅ Basic AI / LLM Application
        ↓
✅ Document Processing
        ↓
✅ Embeddings
        ↓
✅ ChromaDB
        ↓
✅ Semantic Retrieval
        ↓
✅ Basic End-to-End RAG
        ↓
🔄 Retrieval Quality & Evaluation
        ↓
🔄 Multi-User RAG Architecture
        ↓
🔄 Production-Oriented RAG
        ↓
⏳ Advanced Retrieval
        ↓
⏳ LangChain / LangGraph
        ↓
⏳ AI Agents
        ↓
⏳ Multi-Agent Systems
        ↓
⏳ Production Agentic AI
        ↓
⏳ Deployment / Monitoring / Scaling
```

The project intentionally builds the underlying RAG architecture first
before introducing advanced agent frameworks.

------------------------------------------------------------------------

## 📚 Learning Outcomes

This project is being used to gain practical experience with:

-   Python application architecture
-   Modular service design
-   LLM integration
-   Prompt design
-   Document ingestion
-   File loaders
-   Text chunking
-   Embeddings
-   Vector databases
-   ChromaDB
-   Semantic retrieval
-   Distance-based relevance
-   Retrieval-Augmented Generation
-   Strict grounding
-   Source-aware responses
-   User-scoped knowledge bases
-   Document lifecycle concepts
-   Testing with Pytest
-   Debugging and verification
-   Git/GitHub
-   Multi-user RAG architecture

------------------------------------------------------------------------

## 🔮 Future Development

The long-term goal is to evolve LearnBot into a reliable,
production-oriented AI knowledge system and eventually an agentic AI
platform.

Potential future capabilities include:

-   Advanced RAG evaluation
-   Reranking
-   Hybrid retrieval
-   Query transformation
-   Multi-document reasoning
-   Conversational RAG
-   Document comparison
-   Summarization
-   Tool calling
-   Web search tools
-   LangChain
-   LangGraph
-   Agent workflows
-   Stateful agents
-   Multi-agent orchestration
-   FastAPI services
-   Cloud object storage
-   Production deployment
-   Monitoring and tracing
-   Evaluation pipelines
-   Security and access control
-   Scalable infrastructure

------------------------------------------------------------------------

## ⚠️ Project Status Disclaimer

This repository represents an **actively developed learning and
engineering project**.

The basic end-to-end RAG application is implemented, but the system is
still being evolved toward production readiness.

In particular, the multi-user persistence, document lifecycle, advanced
retrieval, deployment, monitoring, and agentic capabilities should be
considered **development stages rather than fully production-hardened
features**.

------------------------------------------------------------------------

## 📜 License

This project is licensed under the **MIT License**.

------------------------------------------------------------------------

## 👨‍💻 About the Author

### Prince Prem

Aspiring **AI Engineer** focused on building practical AI systems and
understanding the engineering foundations behind modern RAG and Agentic
AI applications.

**LearnBot --- AI Knowledge Assistant** represents the progression from
a basic LLM application to an end-to-end RAG system and now toward
multi-user, production-oriented AI architecture.

The project is being developed incrementally with an emphasis on:

``` text
Understand
   ↓
Implement
   ↓
Test
   ↓
Verify
   ↓
Improve
   ↓
Scale
```

------------------------------------------------------------------------

## ⭐ Project

If you find the project useful or interesting, consider giving the
repository a ⭐ on GitHub.

**GitHub:**
`https://github.com/<your-github-username>/AI-Knowledge-Assistant`
