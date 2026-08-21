import shutil
from pathlib import Path

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding
from ingestion.pipeline import IngestionPipeline
from ingestion.service import DocumentIngestionService
from knowledge.base_knowledge import BaseKnowledge
from retrieval.retriever import Retriever
from vectordb.chroma_db import ChromaVectorStore


def test_real_knowledge_base():

    # Clean up persistent test directory
    test_dir = Path("data/test_knowledge_base")

    if test_dir.exists():
        shutil.rmtree(test_dir)

    # 1. Embedding model
    embedder = SentenceTransformerEmbedding()

    # 2. Vector store
    store = ChromaVectorStore(
        persist_directory="data/test_knowledge_base"
    )

    # 3. Chunker
    chunker = RecursiveChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    # 4. Ingestion pipeline
    ingestion_pipeline = IngestionPipeline(
        chunker=chunker,
        embedding_model=embedder,
        vector_store=store,
    )

    # 5. Ingestion service
    ingestion_service = DocumentIngestionService(
        ingestion_pipeline=ingestion_pipeline
    )

    # 6. Retriever
    retriever = Retriever(
        embedding_model=embedder,
        vector_store=store,
    )

    # 7. Knowledge base
    knowledge_base = BaseKnowledge(
        ingestion_service=ingestion_service,
        retriever=retriever,
    )

    # 8. Ingest real document
    chunk_count = knowledge_base.ingest_file(
        "data/sample.txt",
        user_id="test_user",
    )

    print("\nChunks ingested:", chunk_count)

    assert chunk_count > 0

    # 9. Search knowledge base
    results = knowledge_base.search(
        query="What is Python?",
        top_k=1,
    )

    print("\nSearch results:")
    print(results)

    # 10. Validate
    assert len(results["ids"][0]) == 1

    assert (
        results["ids"][0][0]
        == "7c0e51aedc9650b5c06208047300af0121383d3a3c2c690e71b7407a74f2b11e_chunk_000"
    )

    assert (
        "Python"
        in results["documents"][0][0]
    )