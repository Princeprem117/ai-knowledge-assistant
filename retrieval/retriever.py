from embeddings.base_embedding import BaseEmbedding
from vectordb.base_db import BaseVectorStore


class Retriever:
    """
    Retrieves relevant documents from the vector store
    using semantic similarity.
    """

    def __init__(
        self,
        embedding_model: BaseEmbedding,
        vector_store: BaseVectorStore,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        max_distance: float | None = None,
        user_id: str | None = None,
    ):
        """
        Retrieve relevant document chunks.

        Args:
            query: User's search query.
            top_k: Maximum number of chunks to retrieve.
            max_distance: Optional maximum allowed distance.
        """

        print("\n--- Retrieval Debug ---")
        print(f"Query: {query}")
        print(f"Top-K: {top_k}")
        print(f"user_id: {user_id}")

        query_embedding = self.embedding_model.embed(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            user_id=user_id,
        )

        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        filtered_ids = []
        filtered_distances = []
        filtered_documents = []
        filtered_metadatas = []

        for index, (
            result_id,
            distance,
            document,
            metadata,
        ) in enumerate(
            zip(
                ids,
                distances,
                documents,
                metadatas,
            ),
            start=1,
        ):

            source = metadata.get(
                "source",
                "unknown",
            )

            preview = document[:100].replace(
                "\n",
                " ",
            )

            print(
                f"{index}. distance={distance:.4f} "
                f"|source=\n{source}"
            )

            print(
                f" Document = {preview}"
            )

            if (
                max_distance is None
                or distance <= max_distance
            ):
                filtered_ids.append(result_id)
                filtered_distances.append(distance)
                filtered_documents.append(document)
                filtered_metadatas.append(metadata)

        print("-----------------------\n")

        return {
            **results,
            "ids": [filtered_ids],
            "distances": [filtered_distances],
            "documents": [filtered_documents],
            "metadatas": [filtered_metadatas],
        }