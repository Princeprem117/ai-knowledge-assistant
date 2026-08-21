from embeddings.sentence_transformer import SentenceTransformerEmbedding
from ingestion.pipeline import IngestionPipeline
from ingestion.service import DocumentIngestionService
from chunkers.recursive_chunker import RecursiveChunker
from vectordb.chroma_db import ChromaVectorStore


def test_real_file_ingestion():

    # 1. Create components
    chunker = RecursiveChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory="data/test_service_ingestion"
    )

    # 2. Create ingestion pipeline
    pipeline = IngestionPipeline(
        chunker=chunker,
        embedding_model=embedder,
        vector_store=store,
    )

    # 3. Create document ingestion service
    service = DocumentIngestionService(
        ingestion_pipeline=pipeline
    )

    # 4. Ingest real file
    chunk_count = service.ingest_file(
        "data/sample.txt",
        user_id="test_user",
    )

    print("\nChunks ingested:", chunk_count)

    assert chunk_count > 0

    # 5. Search the stored knowledge
    query_embedding = embedder.embed(
        "What is Python?"
    )

    results = store.search(
        query_embedding=query_embedding,
        top_k=1,
        user_id="test_user",
    )

    print("\nRetrieved IDs:")
    print(results["ids"])

    print("\nRetrieved documents:")
    print(results["documents"])

    print("\nRetrieved metadata:")
    print(results["metadatas"])

    # 6. Validate
    assert len(results["ids"][0]) == 1

    assert results["ids"][0][0].endswith(
        "_chunk_000"
    )

    assert (
        results["metadatas"][0][0]["source"]
        == "data/sample.txt"
    )