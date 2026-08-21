import shutil
from pathlib import Path

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding
from ingestion.pipeline import IngestionPipeline
from ingestion.service import DocumentIngestionService
from knowledge.base_knowledge import BaseKnowledge
from retrieval.retriever import Retriever
from vectordb.chroma_db import ChromaVectorStore


def test_real_pdf_knowledge_base():

    # Clean up persistent test directory
    test_dir = Path("data/test_pdf_knowledge")

    if test_dir.exists():
        shutil.rmtree(test_dir)

    pdf_path = Path("data/sample.pdf")

    embedder = SentenceTransformerEmbedding()

    vector_store = ChromaVectorStore(
        persist_directory="data/test_pdf_knowledge"
    )

    chunker = RecursiveChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    ingestion_pipeline = IngestionPipeline(
        chunker=chunker,
        embedding_model=embedder,
        vector_store=vector_store,
    )

    ingestion_service = DocumentIngestionService(
        ingestion_pipeline=ingestion_pipeline,
    )

    retriever = Retriever(
        embedding_model=embedder,
        vector_store=vector_store,
    )

    knowledge = BaseKnowledge(
        ingestion_service=ingestion_service,
        retriever=retriever,
    )

    # Ingest PDF
    chunk_count = knowledge.ingest_file(
        str(pdf_path),
        user_id="test_user",
    )

    print("\nChunks ingested:", chunk_count)

    assert chunk_count > 0

    # Search the PDF knowledge
    results = knowledge.search(
        query="What is Python?",
        top_k=1,
    )

    print("\nSearch results:")
    print(results)

    assert len(results["ids"][0]) == 1
    assert len(results["documents"][0]) == 1

    assert "Python" in results["documents"][0][0]