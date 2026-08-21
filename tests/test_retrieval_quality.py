from pathlib import Path

from chunkers.recursive_chunker import RecursiveChunker
from embeddings.sentence_transformer import SentenceTransformerEmbedding
from ingestion.pipeline import IngestionPipeline
from ingestion.service import DocumentIngestionService
from vectordb.chroma_db import ChromaVectorStore


def test_retrieval_quality():

    # --------------------------------------------------
    # 1. Components
    # --------------------------------------------------

    fixture_path = Path(
        "tests/fixtures/intelligent_agents.txt"
    )

    assert fixture_path.exists(), (
        f"Test fixture not found: {fixture_path}"
    )

    chunker = RecursiveChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    embedder = SentenceTransformerEmbedding()

    store = ChromaVectorStore(
        persist_directory="data/test_retrieval_quality"
    )

    # --------------------------------------------------
    # 2. Ingestion pipeline
    # --------------------------------------------------

    pipeline = IngestionPipeline(
        chunker=chunker,
        embedding_model=embedder,
        vector_store=store,
    )

    service = DocumentIngestionService(
        ingestion_pipeline=pipeline
    )

    # --------------------------------------------------
    # 3. Ingest test fixture
    # --------------------------------------------------

    chunk_count = service.ingest_file(
        str(fixture_path),
        user_id="test_user",
    )

    print(
        f"\nChunks ingested: {chunk_count}"
    )

    # --------------------------------------------------
    # 4. Inspect stored chunks
    # --------------------------------------------------

    results = store.collection.get(
        include=[
            "documents",
            "metadatas",
        ]
    )

    documents = results.get(
        "documents",
        []
    )

    metadatas = results.get(
        "metadatas",
        []
    )

    print("\n--- Stored Chunks ---")

    for index, (document, metadata) in enumerate(
    zip(documents[:10], metadatas[:10]),
    start=1,
):

        print(f"\n--- Chunk {index} ---")
        print(document)
        print(f"Length: {len(document)}")
        print(f"Metadata: {metadata}")

    print("\n---------------------")

    assert chunk_count > 0

    # --------------------------------------------------
    # 5. Retrieval experiment
    # --------------------------------------------------


    relevant_queries = [
        "What is an agent?",
        "What is a rational agent?",
        "What is a simple reflex agent?",
        "What is a model-based reflex agent?",
        "What is a goal-based agent?",
        "What is a utility-based agent?",
        "What are the four basic types of agents?",
    ]

    unrelated_queries = [
        "What is the capital of France?",
        "What is quantum computing?",
        "Who invented the telephone?",
        "What is the capital of Japan?",
        "How does photosynthesis work?",
        "What is machine translation?",
    ]

    print("\n--- Retrieval Experiment ---")

    for query in relevant_queries:

        query_embedding = embedder.embed(query)

        results = store.search(
            query_embedding=query_embedding,
            top_k=3,
        )

        retrieved_documents = results["documents"][0]
        distances = results["distances"][0]
        retrieved_metadatas = results["metadatas"][0]

        print(f"\nQuery: {query}")

        for index, (
            document,
            distance,
            metadata,
        ) in enumerate(
            zip(
                retrieved_documents,
                distances,
                retrieved_metadatas,
            ),
            start=1,
        ):

            preview = document[:150].replace(
                "\n",
                " ",
            )

            print(
                f"{index}. distance={distance:.4f}"
            )

            print(
                f"   source={metadata.get('source')}"
            )

            print(
                f"   document={preview}"
            )

    print("\n-----------------------------")

    # --------------------------------------------------
    # 6. Distance statistics
    # --------------------------------------------------

    relevant_distances = []
    unrelated_distances = []

    for query in relevant_queries:

        query_embedding = embedder.embed(query)

        results = store.search(
            query_embedding=query_embedding,
            top_k=1,
        )

        distance = results["distances"][0][0]

        relevant_distances.append(distance)

    for query in unrelated_queries:

        query_embedding = embedder.embed(query)

        results = store.search(
            query_embedding=query_embedding,
            top_k=1,
        )

        distance = results["distances"][0][0]

        unrelated_distances.append(distance)

    print("\n--- Distance Statistics ---")

    print("\nRelevant queries:")

    print(
        f"Minimum: {min(relevant_distances):.4f}"
    )

    print(
        f"Maximum: {max(relevant_distances):.4f}"
    )

    print(
        f"Average: {sum(relevant_distances) / len(relevant_distances):.4f}"
    )

    print("\nUnrelated queries:")

    print(
        f"Minimum: {min(unrelated_distances):.4f}"
    )

    print(
        f"Maximum: {max(unrelated_distances):.4f}"
    )

    print(
        f"Average: {sum(unrelated_distances) / len(unrelated_distances):.4f}"
    )

    # --------------------------------------------------
    # 7. Threshold evaluation
    # --------------------------------------------------

    candidate_thresholds = [
        0.7,
        0.8,
        0.9,
        1.0,
        1.1,
        1.2,
    ]

    print("\n--- Threshold Evaluation ---")

    for threshold in candidate_thresholds:

        relevant_correct = sum(
            distance <= threshold
            for distance in relevant_distances
        )

        unrelated_correct = sum(
            distance > threshold
            for distance in unrelated_distances
        )

        total_correct = (
            relevant_correct
            + unrelated_correct
        )

        total_queries = (
            len(relevant_distances)
            + len(unrelated_distances)
        )

        accuracy = (
            total_correct / total_queries
        )

        print(
            f"\nThreshold: {threshold:.1f}"
        )

        print(
            f"Relevant accepted: "
            f"{relevant_correct}/{len(relevant_distances)}"
        )

        print(
            f"Unrelated rejected: "
            f"{unrelated_correct}/{len(unrelated_distances)}"
        )

        print(
            f"Accuracy: "
            f"{accuracy:.2%}"
        )

    print("\n-----------------------------")

    # --------------------------------------------------
    # 8. Top-K evaluation
    # --------------------------------------------------

    top_k_values = [1, 2, 3, 4, 5]

    print("\n--- Top-K Evaluation ---")

    for query in relevant_queries:

        query_embedding = embedder.embed(query)

        print(f"\nQuery: {query}")

        for k in top_k_values:

            results = store.search(
                query_embedding=query_embedding,
                top_k=k,
            )

            documents = results["documents"][0]
            distances = results["distances"][0]

            relevant_count = sum(
                distance <= 1.0
                for distance in distances
            )

            print(
                f"Top-K={k} | "
                f"Retrieved={len(documents)} | "
                f"Relevant={relevant_count}"
            )

    print("\n-----------------------------")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_retrieval_quality())