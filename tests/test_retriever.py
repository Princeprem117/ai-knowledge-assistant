import pytest
from embeddings.sentence_transformer import SentenceTransformerEmbedding
from retrieval.retriever import Retriever
from vectordb.chroma_db import ChromaVectorStore


def test_retriever():
    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory="data/test_retriever"
    )

    documents = [
        "Python is a programming language.",
        "Java is used for enterprise applications.",
        "Python supports object-oriented programming.",
    ]

    ids = [
        "retriever_python_001",
        "retriever_java_001",
        "retriever_python_002",
    ]

    metadatas = [
        {"source": "python.txt"},
        {"source": "java.txt"},
        {"source": "python.txt"},
    ]

    embeddings = [
        embedder.embed(document)
        for document in documents
    ]

    store.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    retriever = Retriever(
        embedding_model=embedder,
        vector_store=store,
    )

    results = retriever.retrieve(
        query="What is Python?",
        top_k=2,
        user_id=None
    )

    print("Retrieved IDs:", results["ids"])
    print("Retrieved documents:", results["documents"])
    print("Distances:", results["distances"])

    assert len(results["ids"][0]) == 2


def test_retriever_filters_by_distance():
    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory="data/test_retriever_threshold"
    )

    documents = [
        "Python is a programming language.",
        "Java is used for enterprise applications.",
        "Python supports object-oriented programming.",
    ]

    ids = [
        "threshold_python_001",
        "threshold_java_001",
        "threshold_python_002",
    ]

    metadatas = [
        {"source": "python.txt"},
        {"source": "java.txt"},
        {"source": "python.txt"},
    ]

    embeddings = [
        embedder.embed(document)
        for document in documents
    ]

    store.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    retriever = Retriever(
        embedding_model=embedder,
        vector_store=store,
    )

    results = retriever.retrieve(
        query="What is Python?",
        top_k=3,
        max_distance=0.8,
        user_id=None
    )

    print(
        "Filtered documents:",
        results["documents"],
    )

    print(
        "Filtered distances:",
        results["distances"],
    )

    assert len(results["documents"][0]) >= 1

    assert all(
        distance <= 0.8
        for distance in results["distances"][0]
    )