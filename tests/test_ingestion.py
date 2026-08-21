from pathlib import Path

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding
from ingestion.pipeline import IngestionPipeline
from models.document import Document
from vectordb.chroma_db import ChromaVectorStore


def test_ingestion_pipeline():

    # 1. Read sample document
    file_path = Path("data/sample.txt")

    content = file_path.read_text(
        encoding="utf-8"
    )

    document = Document(
        content=content,
        metadata={
            "source": str(file_path)
        },
    )

    # 2. Create components
    chunker = RecursiveChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory="data/test_ingestion"
    )

    # 3. Create ingestion pipeline
    ingestion = IngestionPipeline(
        chunker=chunker,
        embedding_model=embedder,
        vector_store=store,
    )

    # 4. Ingest document
    chunk_count = ingestion.ingest(
        [document],
        user_id="test_user",
    )

    print("\nChunks stored:", chunk_count)

    assert chunk_count > 0

    query_embedding = embedder.embed(
        "What is Python?"
    )

    results = store.search(
        query_embedding=query_embedding,
        top_k=1,
    )

    print("\nStored IDs:")
    print(results["ids"])

    print("\nStored metadata:")
    print(results["metadatas"])

    assert len(results["ids"][0]) == 1

    assert results["ids"][0][0] == (
        "7c0e51aedc9650b5c06208047300af0121383d3a3c2c690e71b7407a74f2b11e_chunk_000"
    )