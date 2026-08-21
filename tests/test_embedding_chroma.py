from embeddings.sentence_transformer import SentenceTransformerEmbedding
from vectordb.chroma_db import ChromaVectorStore


def test_real_embedding_with_chroma():
    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory="data/test_real_embeddings"
    )

    documents = [
        "Python is a programming language.",
        "Java is used for enterprise applications.",
        "Python supports object-oriented programming.",
    ]

    ids = [
        "real_python_001",
        "real_java_001",
        "real_python_002",
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

    query = "What is Python?"

    query_embedding = embedder.embed(query)

    results = store.search(
        query_embedding=query_embedding,
        top_k=2,
    )

    print("Query:", query)
    print("Results:", results["ids"])
    print("Distances:", results["distances"])

    assert len(results["ids"][0]) == 2