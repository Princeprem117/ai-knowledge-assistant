from embeddings.sentence_transformer import SentenceTransformerEmbedding
from vectordb.chroma_db import ChromaVectorStore


def test_chroma_search_isolates_users(tmp_path):
    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory=str(tmp_path / "chroma"),
        collection_name="multi_user_test",
    )

    documents = [
        "Python is a programming language.",
        "Python supports object-oriented programming.",
        "Java is commonly used for enterprise applications.",
    ]

    ids = [
        "user_a_python_001",
        "user_a_python_002",
        "user_b_java_001",
    ]

    metadatas = [
        {
            "source": "python.txt",
            "filename": "python.txt",
            "user_id": "user_a",
        },
        {
            "source": "python_oop.txt",
            "filename": "python_oop.txt",
            "user_id": "user_a",
        },
        {
            "source": "java.txt",
            "filename": "java.txt",
            "user_id": "user_b",
        },
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

    # User A searches for Python.
    user_a_query = embedder.embed(
        "What is Python?"
    )

    user_a_results = store.search(
        query_embedding=user_a_query,
        top_k=3,
        user_id="user_a",
    )

    user_a_ids = user_a_results["ids"][0]

    # User A must only receive User A's chunks.
    assert user_a_ids
    assert all(
        "user_a" in result_id
        for result_id in user_a_ids
    )

    assert "user_b_java_001" not in user_a_ids

    # User B searches for Java.
    user_b_query = embedder.embed(
        "What is Java?"
    )

    user_b_results = store.search(
        query_embedding=user_b_query,
        top_k=3,
        user_id="user_b",
    )

    user_b_ids = user_b_results["ids"][0]

    # User B must only receive User B's chunks.
    assert user_b_ids
    assert all(
        "user_b" in result_id
        for result_id in user_b_ids
    )

    assert "user_a_python_001" not in user_b_ids
    assert "user_a_python_002" not in user_b_ids