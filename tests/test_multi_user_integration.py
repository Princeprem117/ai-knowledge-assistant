from models.document import Document

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding
from ingestion.pipeline import IngestionPipeline
from retrieval.retriever import Retriever
from vectordb.chroma_db import ChromaVectorStore


def test_complete_multi_user_isolation(tmp_path):

    store = ChromaVectorStore(
        persist_directory=str(tmp_path / "chroma"),
        collection_name="integration",
    )

    embedder = SentenceTransformerEmbedding()

    pipeline = IngestionPipeline(
        chunker=RecursiveChunker(
            chunk_size=200,
            chunk_overlap=50,
        ),
        embedding_model=embedder,
        vector_store=store,
    )

    retriever = Retriever(
        embedding_model=embedder,
        vector_store=store,
    )

    prince_doc = Document(
        content="A rational agent chooses the best action.",
        metadata={
            "source": "agents.pdf",
            "type": "pdf",
        },
    )

    alice_doc = Document(
        content="Python supports object-oriented programming.",
        metadata={
            "source": "python.pdf",
            "type": "pdf",
        },
    )

    pipeline.ingest(
        [prince_doc],
        user_id="prince",
    )

    pipeline.ingest(
        [alice_doc],
        user_id="alice",
    )

    prince_results = retriever.retrieve(
        query="What is Python?",
        top_k=3,
        user_id="prince",
    )

    alice_results = retriever.retrieve(
        query="What is Python?",
        top_k=3,
        user_id="alice",
    )

    # Prince should only receive Prince's chunks.
    assert all(
        metadata["user_id"] == "prince"
        for metadata in prince_results["metadatas"][0]
    )

    assert all(
        "Python supports object-oriented programming."
        != document
        for document in prince_results["documents"][0]
    )

    # Alice should only receive Alice's chunks.
    assert all(
        metadata["user_id"] == "alice"
        for metadata in alice_results["metadatas"][0]
    )

    assert any(
        "Python supports object-oriented programming."
        == document
        for document in alice_results["documents"][0]
    )