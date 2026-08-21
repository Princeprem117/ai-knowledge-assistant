from vectordb.chroma_db import ChromaVectorStore


def test_chroma_store_add():
    store = ChromaVectorStore(
        persist_directory="data/test_chroma"
    )

    documents = [
        "Python is a programming language.",
        "Python supports object-oriented programming.",
    ]

    embeddings = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    metadatas = [
        {"source": "test.txt"},
        {"source": "test.txt"},
    ]

    ids = [
        "test_chunk_001",
        "test_chunk_002",
    ]

    store.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    assert store.collection.count() == 2

from vectordb.chroma_db import ChromaVectorStore


def test_chroma_store_search():
    store = ChromaVectorStore(
        persist_directory="data/test_chroma_search"
    )

    documents = [
        "Python is a programming language.",
        "Java is used for enterprise applications.",
        "Python supports object-oriented programming.",
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.9, 0.1, 0.0],
    ]

    metadatas = [
        {"source": "python.txt"},
        {"source": "java.txt"},
        {"source": "python.txt"},
    ]

    ids = [
        "python_001",
        "java_001",
        "python_002",
    ]

    store.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=2,
    )

    print("Search results ids:", results["ids"])
    print("Search results distances:", results.get("distances"))
    print("Search results metadatas:", results.get("metadatas"))

    assert len(results["ids"][0]) == 2

def test_chroma_store_delete():
    store = ChromaVectorStore(
        persist_directory="data/test_chroma_delete"
    )

    documents = [
        "Python is a programming language.",
        "Java is used for enterprise applications.",
        "C++ is a compiled programming language.",
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]

    metadatas = [
        {"source": "python.txt"},
        {"source": "java.txt"},
        {"source": "cpp.txt"},
    ]

    ids = [
        "python_001",
        "java_001",
        "cpp_001",
    ]

    store.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    assert store.collection.count() == 3

    store.delete(["java_001"])

    assert store.collection.count() == 2

    results = store.collection.get()

    assert "java_001" not in results["ids"]

def test_chroma_store_delete_by_source_with_full_path():
    store = ChromaVectorStore(
        persist_directory="data/test_chroma_source_delete"
    )

    documents = [
        "Agent rationality information.",
        "More information about rational agents.",
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
    ]

    metadatas = [
        {
            "source": "IntelligentAgents_info.pdf"
        },
        {
            "source": (
                "C:/Python/AI Knowledge Assistant/"
                "data/uploads/"
                "IntelligentAgents_info.pdf"
            )
        },
    ]

    ids = [
        "old_style_chunk_000",
        "new_style_chunk_000",
    ]

    store.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    found_ids = store.get_ids_by_source(
        "data/uploads/IntelligentAgents_info.pdf"
    )

    assert set(found_ids) == set(ids)

    store.delete(found_ids)

    assert store.collection.count() == 0